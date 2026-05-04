from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class SpMovesItem(TypedDict):
    """特殊招式项"""

    id: int
    item: int
    itemname: str
    itemnumber: int
    monster: int
    moves: int
    movesname: str
    movetype: int


class _Config(TypedDict):
    """配置容器"""

    show_moves: list[SpMovesItem]
    sp_moves: list[SpMovesItem]


class SpHideMovesBisaifuConfig(TypedDict):
    """赛事服隐藏招式配置"""

    config: _Config


class SpHideMovesBisaifuParser(BaseParser[SpHideMovesBisaifuConfig]):
    """赛事服隐藏招式解析器"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'sp_hide_moves_bisaifu.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'spHideMovesBisaifu.json'

    def parse(self, data: bytes) -> SpHideMovesBisaifuConfig:
        reader = BytesReader(data)
        result: SpHideMovesBisaifuConfig = {
            'config': {'show_moves': [], 'sp_moves': []}
        }

        if not reader.ReadBoolean():
            return result

        if reader.ReadBoolean():
            show_count = reader.ReadSignedInt()
            for _ in range(show_count):
                sid = reader.ReadSignedInt()
                item = reader.ReadSignedInt()
                itemname = reader.ReadUTFBytesWithLength()
                itemnumber = reader.ReadSignedInt()
                monster = reader.ReadSignedInt()
                moves = reader.ReadSignedInt()
                movesname = reader.ReadUTFBytesWithLength()
                movetype = reader.ReadSignedInt()

                sp_item: SpMovesItem = {
                    'id': sid,
                    'item': item,
                    'itemname': itemname,
                    'itemnumber': itemnumber,
                    'monster': monster,
                    'moves': moves,
                    'movesname': movesname,
                    'movetype': movetype,
                }
                result['config']['show_moves'].append(sp_item)

        if reader.ReadBoolean():
            sp_count = reader.ReadSignedInt()
            for _ in range(sp_count):
                sid = reader.ReadSignedInt()
                item = reader.ReadSignedInt()
                itemname = reader.ReadUTFBytesWithLength()
                itemnumber = reader.ReadSignedInt()
                monster = reader.ReadSignedInt()
                moves = reader.ReadSignedInt()
                movesname = reader.ReadUTFBytesWithLength()
                movetype = reader.ReadSignedInt()

                sp_item: SpMovesItem = {
                    'id': sid,
                    'item': item,
                    'itemname': itemname,
                    'itemnumber': itemnumber,
                    'monster': monster,
                    'moves': moves,
                    'movesname': movesname,
                    'movetype': movetype,
                }
                result['config']['sp_moves'].append(sp_item)

        return result
