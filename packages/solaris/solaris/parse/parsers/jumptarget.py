from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _Item(TypedDict):
    id: int
    name: str
    paras: str
    target: int
    type: int


class _Data(TypedDict):
    data: list[_Item]


class JumptargetParser(BaseParser[_Data]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'jumptarget.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'jumptarget.json'

    def parse(self, data: bytes) -> _Data:
        reader = BytesReader(data)
        result: _Data = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: _Item = {
                'id': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
                'paras': reader.ReadUTFBytesWithLength(),
                'target': reader.ReadSignedInt(),
                'type': reader.ReadSignedInt(),
            }
            result['data'].append(item)

        return result
