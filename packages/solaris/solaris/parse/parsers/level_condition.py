from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _Item(TypedDict):
    count: int
    id: int
    script: str


class _Data(TypedDict):
    data: list[_Item]


class LevelConditionParser(BaseParser[_Data]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'LevelCondition.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'levelCondition.json'

    def parse(self, data: bytes) -> _Data:
        reader = BytesReader(data)
        result: _Data = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: _Item = {
                'count': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'script': reader.ReadUTFBytesWithLength(),
            }
            result['data'].append(item)

        return result
