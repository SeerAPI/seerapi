from collections import defaultdict
from collections.abc import Mapping, MutableMapping, Sequence
import inspect
from pathlib import Path
from typing import (
	Any,
	Literal,
	Protocol,
	TypeAlias,
	TypeVar,
	cast,
	overload,
)

from openapi_pydantic import Operation, Parameter, PathItem, Reference, Schema
from pydantic import BaseModel, Field
from pydantic.json_schema import GenerateJsonSchema, model_json_schema
from seerapi_models.build_model import BaseResModel
from seerapi_models.common import (
	ApiResourceList,
	BaseGeneralModel,
	NamedData,
	NamedResourceRef,
	ResourceRef,
)
from seerapi_models.metadata import ApiMetadata
from tqdm import tqdm

from solaris.analyze.typing_ import AnalyzeResult, NameGenerator, TResModelRequiredId
from solaris.analyze.utils import to_json
from solaris.typing import JSONObject
from solaris.utils import join_url

from .db import DBManager
from .openapi_builder import (
	OpenAPIBuilder,
	build_ref_string,
	create_model_name_string,
)
from .openapi_comments import APIComment, get_api_comment
from .schema_generate import (
	JsonSchemaGenerator,
	OpenAPISchemaGenerator,
	OpenAPIShrinkOnlyNonRoot,
	ShrinkOnlyNonRoot,
	create_extra_schema,
	create_generator,
)


class HashPartial(BaseGeneralModel):
	hash: str = Field(
		description='数据哈希值，目前 pydantic 不支持对 key 进行排序，'
		'所以哈希值变化可能意味着数据结构变化而非数据值变化',
		examples=['abb7l9d6'],
	)

	@classmethod
	def schema_path(cls) -> str:
		return 'analyzer_custom/hash_partial/'


DataMap: TypeAlias = Mapping[int, TResModelRequiredId]


def _calc_hash(data: str | bytes) -> str:
	import anycrc

	crc32 = anycrc.Model('CRC32')
	if isinstance(data, str):
		data = data.encode('utf-8')

	hash_value = crc32.calc(data)
	return format(hash_value, 'x')


def _create_index_model(name: str, data: dict[str, Any]) -> type[BaseModel]:
	from pydantic import Field, create_model

	return create_model(
		name,
		**{
			k: (str, Field(field_title_generator=lambda k, __: f'{k} Path'))
			for k in data.keys()
		},  # type: ignore
	)


def _generate_api_resource_list(data: DataMap[TResModelRequiredId]) -> ApiResourceList:
	refs: list[NamedResourceRef] = []
	for i in data.values():
		refs.append(
			NamedResourceRef.from_res_name(
				id=i.id,
				resource_name=i.resource_name(),
				name=getattr(i, 'name', None),
			)
		)

	return ApiResourceList(count=len(refs), results=refs)


def _generate_named_data_json_schema(resource_ref_path: str, common_ref_path: str):
	return {
		'$schema': 'https://json-schema.org/draft/2020-12/schema',
		'type': 'object',
		'properties': {
			'data': {
				'$ref': common_ref_path,
			}
		},
		'$defs': {
			'TResModel': {
				'$dynamicAnchor': 'TResModel',
				'type': 'object',
				'$ref': resource_ref_path,
			}
		},
		'required': ['data'],
	}


def _generate_named_data_oas_schema(resource_ref_path: str):
	"""生成名称到数据的映射表的 Schema"""
	return {
		'type': 'object',
		'properties': {
			'data': {
				'type': 'object',
				'patternProperties': {'^[0-9]+$': Reference(ref=resource_ref_path)},  # type: ignore
				'additionalProperties': False,
			}
		},
		'required': ['data'],
	}


_GT = TypeVar('_GT', bound=GenerateJsonSchema)


def get_name_fields(model: type) -> list[str]:
	"""获取模型中用于表示名称的字段名列表

	查找模型定义的 ``__name_fields__`` 属性，
	默认值为 `['name']`
	"""
	return getattr(model, '__name_fields__', ['name'])


def get_primary_name_field(model: type) -> str:
	"""获取模型的主要名称字段名（第一个）"""
	return get_name_fields(model)[0]


def is_named_model(model: type) -> bool:
	return any(field in model.model_fields for field in get_name_fields(model))


class DataOutputterProtocol(Protocol):
	"""输出器协议"""

	def run(self, results: Sequence[AnalyzeResult]):
		"""执行输出流程"""
		pass


class SchemaOutputterProtocol(Protocol):
	"""Schema 输出器协议"""

	def run(
		self,
		res_models: Sequence[type[BaseResModel]],
		common_models: Sequence[type[BaseGeneralModel]],
		*,
		output_named_data: bool = False,
	) -> None:
		pass


class SchemaOutputter(SchemaOutputterProtocol):
	"""负责将分析结果输出为 Schema 的类"""

	def __init__(
		self,
		*,
		metadata: ApiMetadata,
		base_output_dir: str | Path = '.',
		schema_output_dir: str | Path,
		base_schema_url: str | None = None,
	) -> None:
		"""初始化 Schema 输出器

		Args:
			metadata: API 元数据
			base_output_dir: 基础目录
			schema_output_dir: Schema 输出目录（相对于版本目录）
			base_schema_url: Schema 基础 URL（可选），用于定义 Schema 的引用路径，
			如果未指定，则使用 metadata.api_url 和 metadata.api_version 拼接生成。
		"""
		self.metadata = metadata

		# 计算 URL
		version = metadata.api_version
		base_url = metadata.api_url
		self.schema_url = base_schema_url or join_url(
			base_url, version, str(schema_output_dir)
		)

		# 计算输出目录
		self.schema_output_dir = Path().joinpath(
			base_output_dir,
			version,
			schema_output_dir,
		)

		# 创建输出目录
		self.schema_output_dir.mkdir(parents=True, exist_ok=True)

		self.shrink_generator = self._create_generator(ShrinkOnlyNonRoot)
		self.normal_generator = self._create_generator(JsonSchemaGenerator)

	def _merge_to_schema(self, *schemas: JSONObject) -> JSONObject:
		return {'allOf': list(schemas)}

	def _create_generator(self, schema_generator: type[_GT]) -> type[_GT]:
		return create_generator(schema_generator, base_url=self.schema_url)

	def _dump_schema(self, schema: JSONObject, path: Path | str) -> None:
		path = self.schema_output_dir.joinpath(path)
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_bytes(to_json(schema))

	def _generate_named_data_schema(self, resource_name: str) -> dict[str, JSONObject]:
		named_schema = _generate_named_data_json_schema(
			join_url(self.schema_url, resource_name, '$id'),
			join_url(self.schema_url, 'common', 'named_data'),
		)
		named_path = str(Path(resource_name) / '$name' / 'index.json')
		# 名称映射 schema 不添加 hash 字段
		return {named_path: named_schema}

	def generate_schemas(
		self,
		res_models: Sequence[type[BaseResModel]],
		common_models: Sequence[type[BaseGeneralModel]],
		*,
		output_named_data: bool = False,
	) -> dict[str, JSONObject]:
		"""生成所有 Schema 并返回，不写入文件系统

		Args:
			res_models: 资源模型序列
			common_models: 通用模型序列
			output_named_data: 是否输出名称映射

		Returns:
			字典，key 为相对路径，value 为 schema 内容
		"""
		schemas: dict[str, JSONObject] = {}

		common_models = [*common_models, HashPartial]  # 暂时先这样处理，后续需要优化
		# 生成通用模型 Schema
		for model in common_models:
			if not issubclass(model, BaseGeneralModel) or inspect.isabstract(model):
				continue

			schema_path = model.schema_path()
			schema = model_json_schema(model, schema_generator=self.shrink_generator)
			path_key = str(Path(schema_path) / 'index.json')
			schemas[path_key] = schema

		hash_schema = model_json_schema(
			HashPartial, schema_generator=self.normal_generator
		)
		index_data: dict[str, str] = {}
		for res_model in res_models:
			resource_name = res_model.resource_name()
			index_data[resource_name] = ''

			schema = model_json_schema(
				res_model, schema_generator=self.shrink_generator
			)

			# 生成 ID 模式 schema
			schema_path = str(Path(resource_name) / '$id' / 'index.json')
			schemas[schema_path] = self._merge_to_schema(schema, hash_schema)

			# ApiResourceList schema
			api_resource_list_schema = model_json_schema(
				ApiResourceList,
				schema_generator=self.normal_generator,
			) | create_extra_schema(model_name=resource_name)
			api_list_path = str(Path(resource_name) / 'index.json')
			schemas[api_list_path] = self._merge_to_schema(
				api_resource_list_schema, hash_schema
			)

			# 生成名称映射 schema
			if output_named_data and is_named_model(res_model):
				named_schema = self._generate_named_data_schema(resource_name)
				# 名称映射 schema 不添加 hash 字段
				schemas.update(named_schema)

		# metadata schema
		metadata_schema = model_json_schema(
			type(self.metadata), schema_generator=self.normal_generator
		)
		schemas['metadata.json'] = self._merge_to_schema(metadata_schema, hash_schema)

		index_model = _create_index_model('Index', index_data)
		index_schema = model_json_schema(index_model)
		schemas['index.json'] = self._merge_to_schema(index_schema, hash_schema)

		return schemas

	def run(
		self,
		res_models: Sequence[type[BaseResModel]],
		common_models: Sequence[type[BaseGeneralModel]],
		*,
		output_named_data: bool = False,
	) -> None:
		"""执行 Schema 输出流程，将生成的 schema 写入文件系统

		Args:
			res_models: 资源模型序列
			common_models: 通用模型序列
			output_named_data: 是否输出名称映射
		"""
		# 生成所有 schema
		schemas = self.generate_schemas(
			res_models, common_models, output_named_data=output_named_data
		)

		# 将所有 schema 写入文件系统
		for path, schema in (pbar_schemas := tqdm(schemas.items(), leave=False)):
			pbar_schemas.set_description(f'正在输出 Schema|{path}', refresh=True)
			# 注意：schema 已经包含了额外字段（hash 等），不需要再次添加
			self._dump_schema(schema, path)


class OpenAPISchemaOutputter(SchemaOutputterProtocol):
	"""负责将分析结果输出为 OpenAPI Schema 的类"""

	def __init__(
		self,
		metadata: ApiMetadata,
		*,
		openapi_builder: OpenAPIBuilder,
		base_output_dir: str | Path = '.',
		output_filepath: str | Path,
	) -> None:
		"""初始化 OpenAPI Schema 输出器

		Args:
			metadata: API 元数据
			openapi_builder: OpenAPI 构建器
			base_output_dir: 基础目录
			output_filepath: 输出路径
		"""
		self.version_path = metadata.api_version
		self.output_filepath = Path().joinpath(
			base_output_dir, self.version_path, output_filepath
		)
		self.output_filepath.parent.mkdir(parents=True, exist_ok=True)

		self.metadata = metadata
		self.openapi_builder = openapi_builder
		self.shrink_generator = self._create_generator(OpenAPIShrinkOnlyNonRoot)
		self.normal_generator = self._create_generator(OpenAPISchemaGenerator)

	def _create_generator(self, schema_generator: type[_GT]) -> type[_GT]:
		return create_generator(schema_generator, base_url='#/components/schemas/')

	@property
	def _hash_partial_ref_str(self) -> str:
		return 'hash_partial'

	def _merge_hash_partial_schema(self, schema: JSONObject) -> JSONObject:
		return {
			'allOf': [
				{'$ref': build_ref_string(Schema, name=self._hash_partial_ref_str)},
				schema,
			],
		}

	def _init_hash_partial_schema(self) -> None:
		self.openapi_builder.add_ref(
			HashPartial.model_json_schema(),
			name=self._hash_partial_ref_str,
		)

	def _create_list_schema(self, resource_name: str):
		return {
			'allOf': [
				{
					'$ref': build_ref_string(Schema, name='common_api_resource_list'),
					**create_extra_schema(model_name=resource_name),
				},
			],
		}

	def _name_ref_str(self, resource_name: str) -> str:
		return f'{resource_name}_NamedData'

	def _list_ref_str(self, resource_name: str) -> str:
		return f'{resource_name}_List'

	def _id_ref_str(self, resource_name: str) -> str:
		return resource_name

	def _build_path(self, resource_name: str) -> str:
		return join_url(self.version_path, resource_name)

	def _add_path_to_openapi(
		self,
		type_: Literal['id', 'name', 'paginated'],
		comment: APIComment,
		*,
		resource_name: str,
		schema: JSONObject,
	) -> None:
		builder = self.openapi_builder
		p: str
		path_item: PathItem
		schema_ref: str
		operation_id: str
		tags = comment.tags
		description = comment.description
		title: str
		match type_:
			case 'id':
				p = self._build_path(resource_name) + '/{id}'
				schema_ref = self._id_ref_str(resource_name)
				title = f'{comment.name_cn}资源'
				operation_id = f'get_{resource_name}_by_id'
				path_item = PathItem(
					get=Operation(
						parameters=[builder.create_ref(Parameter, name='id')],
						responses=builder.create_responses(schema_ref),
						tags=tags,
						operationId=operation_id,
						summary=f'获取{comment.name_cn}资源',
						description=description,
					),
				)
			case 'name':
				p = self._build_path(resource_name) + '/{name}'
				schema_ref = self._name_ref_str(resource_name)
				title = f'名称映射{comment.name_cn}资源'
				operation_id = f'get_{resource_name}_by_name'
				path_item = PathItem(
					get=Operation(
						parameters=[builder.create_ref(Parameter, name='name')],
						responses=builder.create_responses(schema_ref),
						tags=tags,
						operationId=operation_id,
						summary=f'通过名称获取{comment.name_cn}资源',
						description=description,
					),
				)
			case 'paginated':
				p = self._build_path(resource_name) + '/'
				schema_ref = self._list_ref_str(resource_name)
				title = f'{comment.name_cn}资源列表'
				operation_id = f'get_{resource_name}_list'
				path_item = PathItem(
					get=Operation(
						parameters=[
							builder.create_ref(Parameter, name='offset'),
							builder.create_ref(Parameter, name='limit'),
						],
						responses=builder.create_responses(schema_ref),
						tags=tags,
						operationId=operation_id,
						summary=f'获取{comment.name_cn}资源列表',
						description=description,
					),
				)
			case _:
				raise ValueError(f'Invalid type: {type_}')

		builder.paths[p] = path_item
		schema_obj = Schema.model_validate(schema)
		schema_obj.examples = comment.examples
		schema_obj.title = title
		builder.add_ref(schema_obj, name=schema_ref)

	def run(
		self,
		res_models: Sequence[type[BaseResModel]],
		common_models: Sequence[type[BaseGeneralModel]],
		*,
		output_named_data: bool = False,
	) -> None:
		"""执行 OpenAPI Schema 输出流程"""
		self._init_hash_partial_schema()
		for model in common_models:
			schema = model_json_schema(model, schema_generator=self.shrink_generator)
			self.openapi_builder.add_ref(schema, name=create_model_name_string(model))

		for res_model in res_models:
			resource_name = res_model.resource_name()
			comment = get_api_comment(res_model)
			# 生成 ID 映射 schema
			schema = model_json_schema(
				res_model, schema_generator=self.shrink_generator
			)
			schema = self._merge_hash_partial_schema(schema)
			self._add_path_to_openapi(
				'id',
				comment,
				resource_name=resource_name,
				schema=schema,
			)

			# 生成名称映射 schema
			if output_named_data and is_named_model(res_model):
				named_schema = _generate_named_data_oas_schema(
					build_ref_string(Schema, name=resource_name),
				)
				named_schema = self._merge_hash_partial_schema(named_schema)
				self._add_path_to_openapi(
					'name',
					comment,
					resource_name=resource_name,
					schema=named_schema,
				)

			# 生成 ApiResourceList schema
			api_resource_list_schema = self._create_list_schema(resource_name)
			self._add_path_to_openapi(
				'paginated',
				comment,
				resource_name=resource_name,
				schema=cast(JSONObject, api_resource_list_schema),
			)

		# metadata schema
		metadata_schema = model_json_schema(
			type(self.metadata), schema_generator=self.normal_generator
		)
		metadata_schema = self._merge_hash_partial_schema(metadata_schema)
		self.openapi_builder.add_ref(metadata_schema, name='api_metadata')

		index_data: dict[str, str] = {}
		for res_model in res_models:
			index_data[res_model.resource_name()] = ''

		if index_data:
			index_model = _create_index_model('Index', index_data)
			index_schema = model_json_schema(index_model)
			index_schema = self._merge_hash_partial_schema(index_schema)
			self.openapi_builder.add_ref(index_schema, name='root_index')

		openapi = self.openapi_builder.build()
		with open(self.output_filepath, 'w') as f:
			f.write(openapi.model_dump_json(by_alias=True, exclude_none=True, indent=2))


class JsonOutputter(DataOutputterProtocol):
	"""负责将分析结果输出为 JSON 文件的类"""

	def __init__(
		self,
		*,
		metadata: ApiMetadata,
		base_output_dir: str | Path = '.',
		data_output_dir: str | Path,
		base_data_url: str | None = None,
	) -> None:
		"""初始化 JSON 输出器

		Args:
			metadata: API 元数据
			base_output_dir: 基础输出目录
			data_output_dir: 数据输出目录（相对于版本目录）
			base_data_url: 数据基础 URL（可选）
		"""
		self.metadata = metadata

		# 计算 URL
		version = metadata.api_version
		base_url = metadata.api_url
		self.data_url = base_data_url or join_url(
			base_url, version, str(data_output_dir)
		)

		# 设置全局资源 URL
		ResourceRef.base_data_url = self.data_url

		# 计算输出目录
		self.data_output_dir = Path().joinpath(
			base_output_dir,
			version,
			data_output_dir,
		)

		# 创建输出目录
		self.data_output_dir.mkdir(parents=True, exist_ok=True)

	def _dump_data(self, data: Any, path: Path | str) -> None:
		if isinstance(data, BaseModel):
			data = data.model_dump(by_alias=True)
		if not isinstance(data, MutableMapping):
			raise ValueError(f'Invalid data type: {type(data)}')

		data['hash'] = _calc_hash(to_json(data, indent=None))

		path = self.data_output_dir.joinpath(path)
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_bytes(to_json(data))

	def _output_merged_json(
		self,
		resource_name: str,
		data: Any,
	) -> None:
		"""输出合并模式的 JSON（所有数据在一个文件中）

		Args:
			resource_name: 资源名称
			data: 要输出的数据
		"""
		self._dump_data(data, f'{resource_name}.json')

	def _generate_name_data(
		self,
		data: DataMap[TResModelRequiredId],
		*,
		name_generator: NameGenerator,
	) -> Mapping[str, NamedData[TResModelRequiredId]]:
		"""生成名称到数据的映射表

		Args:
			data: 分析结果数据
		"""
		name_data: defaultdict[str, NamedData[TResModelRequiredId]] = defaultdict(
			lambda: NamedData(data={})
		)
		for id, model in data.items():
			if name := name_generator(model):
				name_data[str(name)].data[id] = model

		return name_data

	def _output_named_json(
		self,
		name_data: Mapping[str, NamedData[TResModelRequiredId]],
		resource_name: str,
	) -> None:
		"""以名称作为 key，将数据输出为 JSON 文件

		Args:
			name_data: 名称到数据的映射表
			resource_name: 资源名称
		"""
		# 批量输出数据文件
		for name, res_data in name_data.items():
			res_path = Path(resource_name).joinpath(name, 'index.json')
			self._dump_data(res_data, res_path)

	def _output_individual_json(
		self,
		data: DataMap[TResModelRequiredId],
		resource_name: str,
	) -> None:
		"""输出按 ID 分散的 JSON 数据

		将数据按资源 ID 分散到不同的文件中，每个资源 ID 对应一个独立的 JSON 文件。
		同时输出 API 资源列表。

		Args:
			data: 分析出的数据，键为资源 ID，值为资源模型实例
			resource_name: 资源名称，用于构建输出路径
		"""
		# 输出 ApiResourceList
		self._output_api_resource_list(data, resource_name)

		# 批量输出数据文件
		for res_id, res_data in data.items():
			res_path = Path(resource_name).joinpath(str(res_id), 'index.json')
			self._dump_data(res_data, res_path)

	def _output_api_resource_list(
		self,
		data: DataMap[TResModelRequiredId],
		resource_name: str,
	) -> None:
		"""输出 ApiResourceList

		Args:
			data: 分析结果数据
			resource_name: 资源名称
		"""
		api_resource_list = _generate_api_resource_list(data)
		self._dump_data(
			api_resource_list,
			Path(resource_name) / 'index.json',
		)

	def _process_single_result(
		self,
		result: AnalyzeResult[TResModelRequiredId],
		*,
		merge_json_table: bool,
		output_name_data: bool,
	) -> tuple[str, str] | None:
		"""处理单个分析结果

		Args:
			result: 分析结果
			merge_json_table: 是否合并为单个 JSON 文件
			output_name_data: 是否输出名称映射
		Returns:
			如果需要输出，返回 (resource_name, resource_url)，否则返回 None
		"""
		# 检查是否需要输出到 JSON
		if result.output_mode not in ('json', 'all'):
			return None

		# 提取基本信息
		model = result.model
		resource_name = model.resource_name()
		data = result.data

		# 根据模式输出
		if merge_json_table:
			self._output_merged_json(resource_name, data)
		else:
			self._output_individual_json(data, resource_name)
			# 输出名称映射
			if output_name_data and is_named_model(model):
				# 遍历所有定义的名称字段
				for name_field in get_name_fields(model):

					def _name_generator(
						m: TResModelRequiredId, field: str = name_field
					) -> str | None:
						return getattr(m, field, None)

					name_data = self._generate_name_data(
						data, name_generator=_name_generator
					)
					self._output_named_json(name_data, resource_name)

		# 返回索引信息
		return resource_name, join_url(self.data_url, resource_name)

	def _output_metadata(self) -> None:
		"""输出 metadata 文件"""
		self._dump_data(self.metadata, 'metadata.json')

	def _output_root_index(self, index_data: dict[str, str]) -> None:
		"""输出根目录的 index.json

		Args:
			index_data: 索引数据
		"""
		self._dump_data(index_data, 'index.json')

	def run(
		self,
		results: Sequence[AnalyzeResult],
		*,
		merge_json_table: bool = False,
		output_named_data: bool = False,
	) -> None:
		"""执行 JSON 输出流程

		Args:
			results: 分析结果序列
			merge_json_table: 是否合并为单个 JSON 文件
			output_named_data: 是否输出名称映射
		"""
		# 处理所有结果
		root_index_data: dict[str, str] = {}
		for result in (pbar_result := tqdm(results, leave=False)):
			resource_name = result.model.resource_name()
			pbar_result.set_description(
				f'正在输出 JSON 数据 | 输出{resource_name}',
				refresh=True,
			)

			# 处理单个结果
			result_info = self._process_single_result(
				result,
				merge_json_table=merge_json_table,
				output_name_data=output_named_data,
			)
			if result_info is not None:
				resource_name, resource_url = result_info
				root_index_data[resource_name] = resource_url

		# 输出 metadata
		self._output_metadata()

		# 输出根目录 index（仅在非合并模式）
		if not merge_json_table:
			self._output_root_index(root_index_data)


class DBOutputter(DataOutputterProtocol):
	"""负责将分析结果输出到数据库的类"""

	@overload
	def __init__(self, metadata: ApiMetadata, *, db_manager: DBManager) -> None: ...

	@overload
	def __init__(
		self,
		metadata: ApiMetadata,
		*,
		db_url: str,
		echo: bool = False,
		**kwargs,
	) -> None: ...

	def __init__(self, metadata: ApiMetadata, **kwargs) -> None:
		self.metadata = metadata
		if 'db_manager' in kwargs:
			self.db_manager = kwargs['db_manager']
		elif 'db_url' in kwargs and 'echo' in kwargs:
			self.db_manager = DBManager(**kwargs)
		else:
			raise ValueError('Invalid arguments')

	def init(self) -> None:
		if not self.db_manager.initialized:
			self.db_manager.init()

	@property
	def initialized(self) -> bool:
		return self.db_manager.initialized

	def run(self, results: Sequence[AnalyzeResult]) -> None:
		"""执行数据库输出流程

		Args:
			results: 分析结果序列
		"""
		if not self.initialized:
			raise RuntimeError('Database not initialized')

		for result in (pbar_result := tqdm(results, leave=False)):
			name = result.model.resource_name()
			pbar_result.set_description(
				f'正在输出数据库数据 | 输出{name}',
				refresh=True,
			)
			data = result.data
			output_mode = result.output_mode

			if output_mode not in ('db', 'all'):
				continue

			with self.db_manager.get_session() as session:
				from .db import write_result_to_db

				write_result_to_db(session, data)

		# 保存元数据
		with self.db_manager.get_session() as session:
			session.add(self.metadata.to_orm())
			session.commit()
