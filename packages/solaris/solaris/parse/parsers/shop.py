from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ShopItem(TypedDict):
    discountprice: int
    exchange_id: int
    id: int
    item_id: int
    limittype: int
    product_id: int
    usenew: int


class _ShopData(TypedDict):
    item: list[ShopItem]


class ShopParser(BaseParser[_ShopData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'shop.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'shop.json'

    def parse(self, data: bytes) -> _ShopData:
        reader = BytesReader(data)
        result: _ShopData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ShopItem = {
                'discountprice': reader.ReadSignedInt(),
                'exchange_id': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'item_id': reader.ReadSignedInt(),
                'limittype': reader.ReadSignedInt(),
                'product_id': reader.ReadSignedInt(),
                'usenew': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result


class BaseShopItem(TypedDict):
    cost: str
    name: str
    id: int
    max: int
    num: int
    type: int
    vip_only: int


class _BaseShopData(TypedDict):
    item: list[BaseShopItem]


class BaseShopParser(BaseParser[_BaseShopData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'baseShop.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'baseShop.json'

    def parse(self, data: bytes) -> _BaseShopData:
        reader = BytesReader(data)
        result: _BaseShopData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: BaseShopItem = {
                'cost': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'max': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
                'num': reader.ReadSignedInt(),
                'type': reader.ReadSignedInt(),
                'vip_only': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
