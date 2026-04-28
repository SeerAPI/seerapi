from collections import Counter, defaultdict
from collections.abc import Callable
from functools import partial
import importlib
import re
from typing import TYPE_CHECKING, Any, TypedDict, TypeVar, cast
from typing_extensions import TypeIs, Unpack

from openapi_pydantic import Schema
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import (
	GenerateJsonSchema,
	JsonRef,
	JsonSchemaMode,
	JsonSchemaValue,
	model_json_schema,
)
from pydantic_core import CoreSchema
from seerapi_models.build_model import BaseGeneralModel

from .openapi_builder import build_ref_string, create_model_name_string

if TYPE_CHECKING:
	from pydantic._internal._core_utils import CoreSchemaOrField

from seerapi_models.common import ApiResourceList, NamedData, ResourceRef

from solaris.utils import join_url

seerapi_models = importlib.import_module('seerapi_models')
seerapi_common_models = importlib.import_module('seerapi_models.common')
all_models = seerapi_common_models.__dict__ | seerapi_models.__dict__


ROOT_MARK = type('RootMark', (), {})()
ROOT_MARK_KEY = type('RootMarkKey', (), {})()


def _mark_in_schema(core_schema) -> bool:
	return core_schema.get(ROOT_MARK_KEY) is ROOT_MARK


def _add_mark_to_schema(schema):
	"""
	重写根级别 schema 生成，
	将非根模型的 BaseGeneralModel schema 省略为 $ref 引用
	"""
	cls = _get_cls_from_schema(schema)

	if cls is not None and is_base_general_model(cls):
		# 标记为根模型以输出完整 schema
		new_core_schema = schema.copy()
		new_core_schema[ROOT_MARK_KEY] = ROOT_MARK
	else:
		new_core_schema = schema

	return new_core_schema


def _get_cls_from_schema(core_schema: CoreSchema) -> type | None:
	return core_schema.get('cls')


class _ExtraSchemaField(TypedDict):
	model_name: str


def create_extra_schema(**kwargs: Unpack[_ExtraSchemaField]) -> dict[str, object]:
	"""创建额外的 JSON Schema 字段，使用 x- 前缀符合 JSON Schema 规范

	Args:
		**kwargs: 额外字段的键值对，key 会自动添加 x- 前缀并转换为连字符格式

	Returns:
		包含 x- 前缀字段的字典，例如 {'x-model-name': 'Pet'}
	"""
	return {f'x-{key.replace("_", "-")}': value for key, value in kwargs.items()}


def _get_model_name(cls: type) -> str:
	cls_name: str = cls.__name__
	bracket_matches = re.findall(r'\[([^\]]+)\]', cls_name)
	if len(bracket_matches) == 0:
		raise ValueError(f'无效的模型名称：{cls_name}，该模型不是泛型模型')

	model_cls_name = bracket_matches[0]
	if (model := all_models.get(model_cls_name)) is None:
		raise ValueError(
			f'无效的模型名称：{cls_name}，找不到泛型参数{model_cls_name}对应的模型'
		)

	return model.resource_name()


def is_base_general_model(cls: type) -> TypeIs['type[BaseGeneralModel]']:
	return issubclass(cls, BaseGeneralModel)


injected_func = Callable[[CoreSchema, GetJsonSchemaHandler], JsonSchemaValue]
_TCoreSchemaOrField = TypeVar('_TCoreSchemaOrField', bound='CoreSchemaOrField')


class PydanticJsFunctionInjector:
	"""JSON Schema 自定义函数注入器

	提供集中式的机制来为特定类型批量注册 JSON Schema 生成函数，
	避免在每个模型类上重复实现 __get_pydantic_json_schema__。

	工作原理：
	1. 通过 @register 装饰器将自定义函数与目标类型关联
	2. 在 schema 生成时，inject_functions 将注册的函数注入到 CoreSchema 的 metadata 中
	3. Pydantic 在生成 JSON Schema 时会自动调用
	   metadata['pydantic_js_functions'] 中的所有函数

	使用场景：
	- 为多个相似类型统一添加额外的 JSON Schema 字段（如 ResourceRef 和 ApiResourceList）
	- 实现跨模型的 JSON Schema 增强逻辑，而无需修改模型定义

	Example:
		>>>
		injector = PydanticJsFunctionInjector()
		@injector.register(ResourceRef, ApiResourceList)
		... def add_model_name(schema, handler):
		...     json_schema = handler(schema)
		...     json_schema['extra'] = {'model_name': 'example'}
		...     return json_schema
	"""

	def __init__(self):
		self.injected_functions: defaultdict[type, list[injected_func]] = defaultdict(
			list
		)

	def register(self, *types: type):
		"""装饰器工厂：将函数注册到指定的类型

		注册的函数会在对应类型生成 JSON Schema 时被调用，
		允许对 JSON Schema 进行自定义修改。

		Args:
			*types: 需要应用此函数的目标类型（支持多个）

		Returns:
			装饰器函数，接收并返回 injected_func 类型的函数
		"""

		def decorator(func: injected_func) -> injected_func:
			for type_ in types:
				self.injected_functions[type_].append(func)

			return func

		return decorator

	def inject_functions(self, schema: _TCoreSchemaOrField) -> _TCoreSchemaOrField:
		"""将已注册的函数注入到 CoreSchema 的 metadata 中

		遍历所有已注册的类型，如果 schema 对应的类是某个注册类型的子类，
		则将对应的函数列表注入到 metadata['pydantic_js_functions'] 中。
		Pydantic 内部会在 JSON Schema 生成过程中自动调用这些函数。

		Args:
			schema: 待注入的 CoreSchema 或 CoreSchemaField

		Returns:
			注入后的 schema（原地修改）
		"""
		model_cls = schema.get('cls')
		if model_cls is None:
			return schema
		if (metadata := schema.get('metadata')) is None:
			return schema

		# 遍历注册表，匹配第一个符合的类型
		for type_, functions in self.injected_functions.items():
			if issubclass(model_cls, type_):
				metadata['pydantic_js_functions'].extend(functions)
				break

		return schema


json_schema_injector = PydanticJsFunctionInjector()
openapi_injector = PydanticJsFunctionInjector()


@openapi_injector.register(ResourceRef, ApiResourceList)
@json_schema_injector.register(ResourceRef, ApiResourceList)
def ref_get_pydantic_json_schema(schema, handler):
	cls = schema.get('cls')
	json_schema = handler(schema)
	try:
		model_name = _get_model_name(cls)
	except ValueError:
		return json_schema

	return json_schema | create_extra_schema(model_name=model_name)


@openapi_injector.register(NamedData)
@json_schema_injector.register(NamedData)
def named_data_get_pydantic_json_schema(schema, handler):
	json_schema = {
		'$schema': 'https://json-schema.org/draft/2020-12/schema',
		'title': 'NamedData',
		'type': 'object',
		'properties': {
			'data': {
				'type': 'object',
				'patternProperties': {'^[0-9]+$': {'$dynamicRef': '#TResModel'}},
				'additionalProperties': False,
			}
		},
		'required': ['data'],
		'$defs': {'TResModel': {'$dynamicAnchor': 'TResModel'}},
	}
	return json_schema


def _get_all_json_refs(item: Any) -> set[JsonRef]:
	"""Get all the definitions references from a JSON schema."""
	refs: set[JsonRef] = set()
	stack = [item]

	while stack:
		current = stack.pop()
		if isinstance(current, dict):
			for key, value in current.items():
				if key == 'examples' and isinstance(value, list):
					continue
				if key == '$ref' and isinstance(value, str):
					if value.startswith('#/components/schemas/'):
						continue
					refs.add(JsonRef(value))
				elif isinstance(value, dict):
					stack.append(value)
				elif isinstance(value, list):
					stack.extend(value)
		elif isinstance(current, list):
			stack.extend(current)

	return refs


def remove_defs_and_refs(schema: dict):
	# 来自：https://stackoverflow.com/questions/79215270/how-to-remove-defs-and-ref-when-creating-a-nested-json-schema-using-pydantic
	schema = schema.copy()
	defs = schema.pop('$defs', {})

	def resolve(subschema):
		if isinstance(subschema, dict):
			ref = subschema.get('$ref', None)
			if ref and not ref.startswith('#/components/schemas/'):
				_def = ref.split('/')[-1]
				return resolve(defs[_def])
			return {_def: resolve(_ref) for _def, _ref in subschema.items()}
		if isinstance(subschema, list):
			return [resolve(ss) for ss in subschema]
		return subschema

	return resolve(schema)


class JsonSchemaGenerator(GenerateJsonSchema):
	base_url: str

	def generate_inner(self, schema):
		json_schema_injector.inject_functions(schema)
		return super().generate_inner(schema)

	def model_schema(self, schema):
		if not hasattr(self, 'base_url'):
			raise ValueError('base_url is not set')

		json_schema = super().model_schema(schema)
		cls = _get_cls_from_schema(schema)
		if cls is None or not is_base_general_model(cls) or _mark_in_schema(schema):
			return json_schema

		return {'$ref': join_url(self.base_url, cls.schema_path())}

	def generate(self, schema, mode: JsonSchemaMode = 'serialization'):
		json_schema = super().generate(schema, mode)
		json_schema['$schema'] = self.schema_dialect
		return json_schema


class ShrinkOnlyNonRoot(JsonSchemaGenerator):
	def generate(self, schema, mode: JsonSchemaMode = 'serialization'):
		new_core_schema = _add_mark_to_schema(schema)
		json_schema = super().generate(new_core_schema, mode)
		return json_schema


class OpenAPISchemaGenerator(GenerateJsonSchema):
	def get_json_ref_counts(self, json_schema: JsonSchemaValue) -> dict[JsonRef, int]:
		"""Get all values corresponding to the key '$ref' anywhere in the json_schema."""
		json_refs: dict[JsonRef, int] = Counter()

		def _add_json_refs(schema: Any) -> None:
			if isinstance(schema, dict):
				if '$ref' in schema:
					json_ref = JsonRef(schema['$ref'])
					if not isinstance(json_ref, str):
						# in this case, '$ref' might have been the name of a property
						return
					if json_ref.startswith('#/components/schemas/'):
						return
					already_visited = json_ref in json_refs
					json_refs[json_ref] += 1
					if already_visited:
						# prevent recursion on a definition that was already visited
						return
					try:
						defs_ref = self.json_to_defs_refs[json_ref]
						if defs_ref in self._core_defs_invalid_for_json_schema:
							raise self._core_defs_invalid_for_json_schema[defs_ref]
						_add_json_refs(self.definitions[defs_ref])
					except KeyError:
						if not json_ref.startswith(('http://', 'https://')):
							raise

				for k, v in schema.items():
					if k == 'examples' and isinstance(v, list):
						# Skip examples that may contain arbitrary values and references
						# (see the comment in `_get_all_json_refs` for more details).
						continue
					_add_json_refs(v)
			elif isinstance(schema, list):
				for v in schema:
					_add_json_refs(v)

		_add_json_refs(json_schema)
		return json_refs

	def _garbage_collect_definitions(self, schema: JsonSchemaValue) -> None:
		visited_defs_refs = set()
		unvisited_json_refs = _get_all_json_refs(schema)
		while unvisited_json_refs:
			next_json_ref = unvisited_json_refs.pop()
			try:
				next_defs_ref = self.json_to_defs_refs[next_json_ref]
				if next_defs_ref in visited_defs_refs:
					continue
				visited_defs_refs.add(next_defs_ref)
				unvisited_json_refs.update(
					_get_all_json_refs(self.definitions[next_defs_ref])
				)
			except KeyError:
				if not next_json_ref.startswith(('http://', 'https://')):
					raise

		self.definitions = {
			k: v for k, v in self.definitions.items() if k in visited_defs_refs
		}

	def generate_inner(self, schema):
		openapi_injector.inject_functions(schema)
		return super().generate_inner(schema)

	def model_schema(self, schema):
		json_schema = super().model_schema(schema)
		cls = _get_cls_from_schema(schema)
		if cls is None or not is_base_general_model(cls) or _mark_in_schema(schema):
			return json_schema

		return {'$ref': build_ref_string(Schema, name=create_model_name_string(cls))}

	def generate(self, schema, mode: JsonSchemaMode = 'serialization'):
		json_schema = super().generate(schema, mode)
		return cast(JsonSchemaValue, remove_defs_and_refs(json_schema))


class OpenAPIShrinkOnlyNonRoot(OpenAPISchemaGenerator):
	def generate(self, schema, mode: JsonSchemaMode = 'serialization'):
		new_core_schema = _add_mark_to_schema(schema)
		json_schema = super().generate(new_core_schema, mode)
		return json_schema


_GT = TypeVar('_GT', bound=GenerateJsonSchema)


def create_generator(model_type: type[_GT], *, base_url: str) -> type[_GT]:
	"""
	为给定的 GenerateJsonSchema 类型动态创建子类，
	并将 base_url 注入为子类的类属性
	"""
	return cast(
		type[_GT],
		type(
			model_type.__name__,
			(model_type,),
			{'base_url': base_url},
		),
	)


model_json_schema = partial(
	model_json_schema,
	mode='serialization',
)
