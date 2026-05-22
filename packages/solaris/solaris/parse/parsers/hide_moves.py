from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _HideMoveItem(TypedDict):
    move_id: int
    move_name1: str
    move_name2: str
    pet_id: int


class _Root(TypedDict):
    item: list[_HideMoveItem]


class HideMovesConfig(TypedDict):
    root: _Root


class HideMovesParser(BaseParser[HideMovesConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'hide_moves.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'hideMoves.json'

    def parse(self, data: bytes) -> HideMovesConfig:
        reader = BytesReader(data)
        result: HideMovesConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()

        for _ in range(count):
            item: _HideMoveItem = {
                'move_id': reader.ReadSignedInt(),
                'move_name1': reader.ReadUTFBytesWithLength(),
                'move_name2': reader.ReadUTFBytesWithLength(),
                'pet_id': reader.ReadSignedInt(),
            }
            result['root']['item'].append(item)

        return result
