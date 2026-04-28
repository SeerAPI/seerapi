from collections.abc import AsyncGenerator
from typing import cast
from typing_extensions import Self

from hishel.httpx import AsyncCacheClient
from httpx import URL
from httpx._urls import QueryParams
from seerapi_models.common import NamedData, ResourceRef

from seerapi._model_map import (
    MODEL_MAP,
    ModelName,
)
from seerapi._models import PagedResponse, PageInfo
from seerapi._typing import (
    NamedResourceArg,
    ResourceArg,
    T_ModelInstance,
    T_NamedModelInstance,
)


def _parse_url_params(url: str) -> QueryParams:
    return URL(url=url).params


def _parse_url_page_info(url: str) -> PageInfo | None:
    if url is None:
        return None

    params = _parse_url_params(url)
    if 'offset' not in params or 'limit' not in params:
        return None

    return PageInfo(
        offset=int(params['offset']),
        limit=int(params['limit']),
    )


class SeerAPI:
    def __init__(
        self,
        *,
        scheme: str = 'https',
        hostname: str = 'api.seerapi.com',
        version_path: str = 'v1',
    ) -> None:
        self.scheme: str = scheme
        self.hostname: str = hostname
        self.version_path: str = version_path
        self.base_url: URL = URL(url=f'{scheme}://{hostname}/{version_path}')
        self._client = AsyncCacheClient(base_url=self.base_url)

    async def __aenter__(self) -> Self:
        """进入异步上下文管理器"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """退出异步上下文管理器，关闭客户端连接"""
        await self.aclose()

    async def aclose(self) -> None:
        """关闭客户端连接并释放资源"""
        await self._client.aclose()

    def _get_resource_name_from_ref(self, ref: ResourceRef[T_ModelInstance]) -> str:
        ref_url = URL(ref.url)
        relative_path = ref_url.path.removeprefix(self.base_url.path)
        return relative_path.strip('/').split('/')[0]

    def _get_resource_name(
        self, resource_name: ResourceArg[T_ModelInstance]
    ) -> ModelName:
        if isinstance(resource_name, str):
            name = resource_name
        elif isinstance(resource_name, ResourceRef):
            name = self._get_resource_name_from_ref(resource_name)
        elif isinstance(resource_name, type):
            name = resource_name.resource_name()
        if name not in MODEL_MAP:
            raise ValueError(f'Invalid resource name: {name}')

        return name

    async def get(
        self,
        resource_name: ResourceArg[T_ModelInstance],
        id: int | None = None,
    ) -> T_ModelInstance:
        if id is None and not isinstance(resource_name, ResourceRef):
            raise ValueError('id is required')

        res_name = self._get_resource_name(resource_name)
        if isinstance(resource_name, ResourceRef):
            id = resource_name.id

        model_type = MODEL_MAP[res_name]
        response = await self._client.get(f'/{res_name}/{id}')
        response.raise_for_status()
        return cast(T_ModelInstance, model_type.model_validate(response.json()))

    async def paginated_list(
        self,
        resource_name: ResourceArg[T_ModelInstance],
        page_info: PageInfo,
    ) -> PagedResponse[T_ModelInstance]:
        res_name = self._get_resource_name(resource_name)

        async def create_generator(
            data: list[dict],
        ) -> AsyncGenerator[T_ModelInstance, None]:
            for item in data:
                yield await self.get(res_name, item['id'])

        response = await self._client.get(
            f'/{res_name}/',
            params={'offset': page_info.offset, 'limit': page_info.limit},
        )
        response.raise_for_status()
        response_json = response.json()
        return PagedResponse(
            count=response_json['count'],
            results=create_generator(response_json['results']),
            next=_parse_url_page_info(response_json['next']),
            previous=_parse_url_page_info(response_json['previous']),
            first=_parse_url_page_info(response_json['first']),
            last=_parse_url_page_info(response_json['last']),
        )

    async def list(
        self, resource_name: ResourceArg[T_ModelInstance]
    ) -> AsyncGenerator[T_ModelInstance, None]:
        """获取所有资源的异步生成器，自动处理分页"""
        res_name = self._get_resource_name(resource_name)

        async def create_generator(page_info: PageInfo):
            while True:
                paged_response = await self.paginated_list(res_name, page_info)

                # 生成当前页的所有结果
                async for item in paged_response.results:
                    yield item

                # 检查是否还有下一页
                if paged_response.next is None:
                    break

                # 更新到下一页
                page_info = paged_response.next

        return create_generator(PageInfo(offset=0, limit=10))

    async def get_by_name(
        self, resource_name: NamedResourceArg[T_NamedModelInstance], name: str
    ) -> NamedData[T_NamedModelInstance]:
        res_name = self._get_resource_name(resource_name)
        model_type = MODEL_MAP[res_name]
        response = await self._client.get(f'/{res_name}/{name}')
        response.raise_for_status()
        return NamedData.model_validate(
            {
                'data': {
                    id: model_type.model_validate(item)
                    for id, item in response.json()['data'].items()
                }
            }
        )
