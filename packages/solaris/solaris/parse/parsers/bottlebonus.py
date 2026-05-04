from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class BottlebonusItem(TypedDict):
    exchangecut: int
    exchangenum: int
    id: int
    needcnt: int
    needitem: int
    output: int
    realid: int
    type: int


class _BottlebonusData(TypedDict):
    item: list[BottlebonusItem]


class BottlebonusParser(BaseParser[_BottlebonusData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'bottlebonus.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'bottlebonus.json'

    def parse(self, data: bytes) -> _BottlebonusData:
        reader = BytesReader(data)
        result: _BottlebonusData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: BottlebonusItem = {
                'exchangecut': reader.ReadSignedInt(),
                'exchangenum': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'needcnt': reader.ReadSignedInt(),
                'needitem': reader.ReadSignedInt(),
                'output': reader.ReadSignedInt(),
                'realid': reader.ReadSignedInt(),
                'type': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
