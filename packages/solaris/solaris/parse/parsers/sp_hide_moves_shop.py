from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class SpHideMovesShopItem(TypedDict):
    item_name: str
    coin_id: int
    id: int
    item_id: int
    limit: int
    monster_id: int
    move_id: int
    price: int
    user_info_id: int
    user_info_pos: int


class _SpHideMovesShopData(TypedDict):
    item: list[SpHideMovesShopItem]


class SpHideMovesShopParser(BaseParser[_SpHideMovesShopData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'sp_hide_moves_shop.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'spHideMovesShop.json'

    def parse(self, data: bytes) -> _SpHideMovesShopData:
        reader = BytesReader(data)
        result: _SpHideMovesShopData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: SpHideMovesShopItem = {
                'coin_id': reader.ReadSignedInt(),
                'item_id': reader.ReadSignedInt(),
                'item_name': reader.ReadUTFBytesWithLength(),
                'limit': reader.ReadSignedInt(),
                'monster_id': reader.ReadSignedInt(),
                'move_id': reader.ReadSignedInt(),
                'price': reader.ReadSignedInt(),
                'user_info_id': reader.ReadSignedInt(),
                'user_info_pos': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
