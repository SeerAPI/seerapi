from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PvpShopItem(TypedDict):
    commodity: str
    petinfo: str
    bag_limit: int
    consumeitemid: int
    discount: int
    id: int
    limit: int
    price: int
    producttype: int
    quantity: int
    sort: int
    suit: int
    type: int
    userinfo: int


class _PvpShopData(TypedDict):
    item: list[PvpShopItem]


class PvpShopParser(BaseParser[_PvpShopData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'pvp_shop.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'pvpShop.json'

    def parse(self, data: bytes) -> _PvpShopData:
        reader = BytesReader(data)
        result: _PvpShopData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: PvpShopItem = {
                'bag_limit': reader.ReadSignedInt(),
                'commodity': reader.ReadUTFBytesWithLength(),
                'consumeitemid': reader.ReadSignedInt(),
                'discount': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'limit': reader.ReadSignedInt(),
                'petinfo': reader.ReadUTFBytesWithLength(),
                'price': reader.ReadSignedInt(),
                'producttype': reader.ReadSignedInt(),
                'quantity': reader.ReadSignedInt(),
                'sort': reader.ReadSignedInt(),
                'suit': reader.ReadSignedInt(),
                'type': reader.ReadSignedInt(),
                'userinfo': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result


class PvpShopBisaifuItem(TypedDict):
    commodity: str
    petinfo: str
    bag_limit: int
    consumeitemid: int
    discount: int
    id: int
    limit: int
    price: int
    producttype: int
    quantity: int
    sort: int
    suit: int
    type: int
    userinfo: int


class _PvpShopBisaifuData(TypedDict):
    item: list[PvpShopBisaifuItem]


class PvpShopBisaifuParser(BaseParser[_PvpShopBisaifuData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'pvp_shop_bisaifu.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'pvpShopBisaifu.json'

    def parse(self, data: bytes) -> _PvpShopBisaifuData:
        reader = BytesReader(data)
        result: _PvpShopBisaifuData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: PvpShopBisaifuItem = {
                'bag_limit': reader.ReadSignedInt(),
                'commodity': reader.ReadUTFBytesWithLength(),
                'consumeitemid': reader.ReadSignedInt(),
                'discount': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'limit': reader.ReadSignedInt(),
                'petinfo': reader.ReadUTFBytesWithLength(),
                'price': reader.ReadSignedInt(),
                'producttype': reader.ReadSignedInt(),
                'quantity': reader.ReadSignedInt(),
                'sort': reader.ReadSignedInt(),
                'suit': reader.ReadSignedInt(),
                'type': reader.ReadSignedInt(),
                'userinfo': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result


class PvpQuizshopItem(TypedDict):
    name: str
    consumeitemid: int
    id: int
    limit: int
    price: int
    product: int
    productnum: int
    producttype: int
    quantity: int


class _PvpQuizshopData(TypedDict):
    item: list[PvpQuizshopItem]


class PvpQuizshopParser(BaseParser[_PvpQuizshopData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'pvp_quizshop.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'pvpQuizshop.json'

    def parse(self, data: bytes) -> _PvpQuizshopData:
        reader = BytesReader(data)
        result: _PvpQuizshopData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: PvpQuizshopItem = {
                'consumeitemid': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'limit': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
                'price': reader.ReadSignedInt(),
                'product': reader.ReadSignedInt(),
                'productnum': reader.ReadSignedInt(),
                'producttype': reader.ReadSignedInt(),
                'quantity': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
