from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ClassicSweepInfoInfo(TypedDict):
    arg_1: int
    arg_2: str
    level_lock: str
    data_key: int
    id: int
    monsterid: int
    name: str
    order: int
    type: int


class _Root(TypedDict):
    item: list[ClassicSweepInfoInfo]


class ClassicSweepInfoConfig(TypedDict):
    root: _Root


class ClassicSweepInfoParser(BaseParser[ClassicSweepInfoConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'classicSweepInfo.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'classicSweepInfo.json'

    def parse(self, data: bytes) -> ClassicSweepInfoConfig:
        reader = BytesReader(data)
        result: ClassicSweepInfoConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        num = reader.ReadSignedInt()
        for _ in range(num):
            item: ClassicSweepInfoInfo = {
                'arg_1': reader.ReadSignedInt(),
                'arg_2': reader.ReadUTFBytesWithLength(),
                'level_lock': reader.ReadUTFBytesWithLength(),
                'data_key': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'monsterid': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
                'order': reader.ReadSignedInt(),
                'type': reader.ReadSignedInt(),
            }
            result['root']['item'].append(item)

        return result
