from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class BattleServerShopItem(TypedDict):
    coinid: int
    cointype: int
    count: int
    id: int
    limitcount: int
    limittype: int
    price: int
    realid: int
    subtag: int
    type: int


class _BattleServerShopData(TypedDict):
    item: list[BattleServerShopItem]


class BattleServerShopParser(BaseParser[_BattleServerShopData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'BattleServerShop.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'battleServerShop.json'

    def parse(self, data: bytes) -> _BattleServerShopData:
        reader = BytesReader(data)
        result: _BattleServerShopData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: BattleServerShopItem = {
                'limitcount': reader.ReadSignedInt(),
                'limittype': reader.ReadSignedInt(),
                'subtag': reader.ReadSignedInt(),
                'coinid': reader.ReadSignedInt(),
                'cointype': reader.ReadSignedInt(),
                'count': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'price': reader.ReadSignedInt(),
                'realid': reader.ReadSignedInt(),
                'type': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
