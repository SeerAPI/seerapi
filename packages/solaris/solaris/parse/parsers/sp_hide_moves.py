"""特殊隐藏技能相关配置解析器

解析赛尔号客户端的特殊隐藏技能数据文件。
"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 特殊技能项数据结构
class SpMovesItem(TypedDict):
    """特殊隐藏技能项"""

    itemname: str
    movesname: str
    id: int
    item: int
    itemnumber: int
    monster: int
    moves: int
    movetype: int
    newse: int  # 2026-11-19 起国服每行末尾新增，台服暂无


# 特殊隐藏技能配置结构
class _Config(TypedDict):
    """特殊隐藏技能配置"""

    show_moves: list[SpMovesItem]
    sp_moves: list[SpMovesItem]


# 顶层数据结构
class SpHideMovesConfig(TypedDict):
    """特殊隐藏技能配置数据"""

    config: _Config


class SpHideMovesParser(BaseParser[SpHideMovesConfig]):
    """特殊隐藏技能配置解析器"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'sp_hide_moves.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'spHideMoves.json'

    def parse(self, data: bytes) -> SpHideMovesConfig:
        # 2026-11-19 国服 sp_hide_moves 每行末尾多了一个 int（反编译 ISpMovesItem.newse），
        # 台服还没有该字段；两种布局都试一遍，取能正好读到文件尾的那种。
        errors: list[Exception] = []
        for has_newse in (True, False):
            try:
                return self._parse_layout(data, has_newse)
            except Exception as e:  # noqa: BLE001 - 布局不匹配则换下一种
                errors.append(e)
        raise ValueError(f'sp_hide_moves.bytes 布局不匹配: {errors}')

    def _parse_layout(self, data: bytes, has_newse: bool) -> SpHideMovesConfig:
        reader = BytesReader(data)
        result: SpHideMovesConfig = {'config': {'show_moves': [], 'sp_moves': []}}

        # 检查是否有数据
        if not reader.ReadBoolean():
            return result

        # 解析 ShowMoves 数组
        if reader.ReadBoolean():
            show_moves_count = reader.ReadSignedInt()
            for _ in range(show_moves_count):
                result['config']['show_moves'].append(self._read_item(reader, has_newse))

        # 解析 SpMoves 数组
        if reader.ReadBoolean():
            sp_moves_count = reader.ReadSignedInt()
            for _ in range(sp_moves_count):
                result['config']['sp_moves'].append(self._read_item(reader, has_newse))

        if not reader.eof():
            raise ValueError(f'解析后仍有 {reader.remaining()} 字节未消费')
        return result

    @staticmethod
    def _read_item(reader: BytesReader, has_newse: bool) -> SpMovesItem:
        # 按照 C# 代码顺序读取
        item_id = reader.ReadSignedInt()
        item = reader.ReadSignedInt()
        itemname = reader.ReadUTFBytesWithLength()
        itemnumber = reader.ReadSignedInt()
        monster = reader.ReadSignedInt()
        moves = reader.ReadSignedInt()
        movesname = reader.ReadUTFBytesWithLength()
        movetype = reader.ReadSignedInt()
        newse = reader.ReadSignedInt() if has_newse else 0

        return {
            'itemname': itemname,
            'movesname': movesname,
            'id': item_id,
            'item': item,
            'itemnumber': itemnumber,
            'monster': monster,
            'moves': moves,
            'movetype': movetype,
            'newse': newse,
        }
