from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _HideMoveItem(TypedDict):
    move_id: int
    move_name1: str
    move_name2: str
    pet_id: int


class _Root(TypedDict):
    _text: str
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
        result: HideMovesConfig = {'root': {'_text': '', 'item': []}}

        if not reader.ReadBoolean():
            return result

        result['root']['_text'] = reader.ReadUTFBytesWithLength()

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()

        for _ in range(count):
            item: _HideMoveItem = {
                'move_id': reader.read_i32(),
                'move_name1': reader.ReadUTFBytesWithLength(),
                'move_name2': reader.ReadUTFBytesWithLength(),
                'pet_id': reader.read_i32(),
            }
            result['root']['item'].append(item)

        return result
