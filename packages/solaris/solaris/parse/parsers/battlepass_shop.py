from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class BattlepassShopItem(TypedDict):
    commodity: str
    buytype: int
    consumeitemid: int
    discount: int
    id: int
    limit: int
    price: int
    quantity: int
    sort: int
    userinfo: int


class _BattlepassShopData(TypedDict):
    item: list[BattlepassShopItem]


class BattlepassShopParser(BaseParser[_BattlepassShopData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'battlepass_shop.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'battlepassShop.json'

    def parse(self, data: bytes) -> _BattlepassShopData:
        reader = BytesReader(data)
        result: _BattlepassShopData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: BattlepassShopItem = {
                'buytype': reader.ReadSignedInt(),
                'commodity': reader.ReadUTFBytesWithLength(),
                'consumeitemid': reader.ReadSignedInt(),
                'discount': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'limit': reader.ReadSignedInt(),
                'price': reader.ReadSignedInt(),
                'quantity': reader.ReadSignedInt(),
                'sort': reader.ReadSignedInt(),
                'userinfo': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result


class PassShopItem(TypedDict):
    commodity: str
    consumeitemid: int
    discount: int
    id: int
    limit: int
    price: int
    quantity: int
    sort: int
    userinfo: int


class _PassShopData(TypedDict):
    item: list[PassShopItem]


class PassShopParser(BaseParser[_PassShopData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'pass_shop.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'passShop.json'

    def parse(self, data: bytes) -> _PassShopData:
        reader = BytesReader(data)
        result: _PassShopData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: PassShopItem = {
                'commodity': reader.ReadUTFBytesWithLength(),
                'consumeitemid': reader.ReadSignedInt(),
                'discount': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'limit': reader.ReadSignedInt(),
                'price': reader.ReadSignedInt(),
                'quantity': reader.ReadSignedInt(),
                'sort': reader.ReadSignedInt(),
                'userinfo': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
