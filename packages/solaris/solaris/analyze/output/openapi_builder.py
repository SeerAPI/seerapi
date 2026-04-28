from collections import defaultdict
from collections.abc import Mapping
from typing import TypeVar

from openapi_pydantic import (
	Components,
	DataType,
	Example,
	Header,
	Info,
	Link,
	MediaType,
	OpenAPI,
	Parameter,
	PathItem,
	Reference,
	RequestBody,
	Response,
	Schema,
	SecurityScheme,
	Server,
)
from seerapi_models.build_model import BaseGeneralModel

Obj = (
	Schema
	| Parameter
	| Response
	| Example
	| RequestBody
	| Header
	| SecurityScheme
	| Link
	| Mapping
)

PART_MAP = {
	Schema: 'schemas',
	Parameter: 'parameters',
	Response: 'responses',
	Example: 'examples',
	RequestBody: 'requestBodies',
	Header: 'headers',
	SecurityScheme: 'securitySchemes',
	Link: 'links',
	Mapping: 'schemas',
}

T = TypeVar('T', bound=Obj)


def _get_part(obj_type: type[Obj]) -> str:
	for key in PART_MAP.keys():
		if issubclass(obj_type, key):
			return PART_MAP[key]

	raise ValueError(f'Invalid object: {obj_type}')


def build_ref_string(obj_type: type[Obj], *, name: str) -> str:
	prefix = '#/components'
	part = _get_part(obj_type)
	return f'{prefix}/{part}/{name}'


def create_model_name_string(type_: type[BaseGeneralModel]) -> str:
	path = type_.schema_path()
	path = path.removesuffix('/')
	path = path.replace('/', '_')
	return path


class OpenAPIBuilder:
	def __init__(
		self, *, title: str, version: str, description: str, servers: list[Server] = []
	):
		self.title = title
		self.version = version
		self.description = description
		self.refs: dict[str, Obj] = {}
		self.servers: list[Server] = servers
		self.paths: dict[str, PathItem] = {}
		self.openapi = OpenAPI(
			info=Info(
				title=title,
				version=version,
				description=description,
			),
			servers=self.servers,
			paths=self.paths,
		)
		self.add_ref(Response(description='Not Modified'), name='NotModified')
		for name, parameter in self._components().items():
			self.add_ref(parameter, name=name)

	def _components(self) -> dict[str, Obj]:
		return {
			# Path 参数组件
			'id': Parameter(
				name='id',
				required=True,
				param_in='path',  # type: ignore
				description='资源 ID',
				schema=Schema(type=DataType.INTEGER),
			),
			'name': Parameter(
				name='name',
				required=True,
				param_in='path',  # type: ignore
				description='资源名称',
				schema=Schema(type=DataType.STRING),
			),
			'limit': Parameter(
				name='limit',
				required=False,
				param_in='query',  # type: ignore
				description='每页返回的最大结果数',
				schema=Schema(type=DataType.INTEGER, default=20),
			),
			'offset': Parameter(
				name='offset',
				required=False,
				param_in='query',  # type: ignore
				description='从哪个位置开始返回结果',
				schema=Schema(type=DataType.INTEGER, default=0),
			),
			# 响应组件
			'304_NotModified': Response(description='Not Modified'),
			# 响应头组件
			'Etag': Header(
				description='Entity tag，用于缓存控制',
				schema=Schema(type=DataType.STRING, example='"ed5go907"'),
			),
			'Link': Header(
				description='RFC 标准的 Link 头，提供分页和Schema信息',
				schema=Schema(
					type=DataType.STRING,
					example='<https://api.seerapi.com/v1/pet?offset=10&limit=10>;'
					'rel="next"',
				),
			),
		}

	def build(self) -> OpenAPI:
		new_openapi = self.openapi.model_copy()
		dict_refs = defaultdict(dict)
		for ref_string, obj in self.refs.items():
			part = _get_part(type(obj))
			ref_name = ref_string.split('/')[-1]
			dict_refs[part][ref_name] = obj

		new_openapi.components = Components.model_validate(dict_refs)
		new_openapi.paths = self.paths
		return new_openapi

	def add_ref(self, obj: Obj, *, name: str) -> None:
		self.refs[build_ref_string(type(obj), name=name)] = obj

	def create_ref(self, obj_type: type[Obj], *, name: str) -> Reference:
		ref_string = build_ref_string(obj_type, name=name)
		if ref_string not in self.refs:
			raise ValueError(f'Reference {ref_string} not found')

		return Reference(ref=ref_string)  # type: ignore

	def create_200_response(self, schema_ref: str) -> Response:
		ref_string = build_ref_string(Schema, name=schema_ref)
		media_type = MediaType(schema=Reference(ref=ref_string))  # type: ignore
		return Response(
			description='OK',
			content={
				'application/json': media_type,
				'application/schema-instance+json': media_type,
			},
			headers={
				'ETag': self.create_ref(Header, name='Etag'),
				'Link': self.create_ref(Header, name='Link'),
			},
		)

	def create_responses(
		self, response_schema_ref: str
	) -> dict[str, Response | Reference]:
		return {
			'200': self.create_200_response(response_schema_ref),
			'304': self.create_ref(Response, name='304_NotModified'),
		}
