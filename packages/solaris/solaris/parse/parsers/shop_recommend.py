from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ShopRecommendItem(TypedDict):
    atlas: str
    jump: str
    name: str
    poster: str
    id: int
    show: int
    sort: int


class _ShopRecommendData(TypedDict):
    item: list[ShopRecommendItem]


class ShopRecommendParser(BaseParser[_ShopRecommendData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'shop_recommend.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'shopRecommend.json'

    def parse(self, data: bytes) -> _ShopRecommendData:
        reader = BytesReader(data)
        result: _ShopRecommendData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ShopRecommendItem = {
                'atlas': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'jump': reader.ReadUTFBytesWithLength(),
                'name': reader.ReadUTFBytesWithLength(),
                'poster': reader.ReadUTFBytesWithLength(),
                'show': reader.ReadSignedInt(),
                'sort': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
