from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class GlobalNumberInfo(TypedDict):
    content: int
    id: int
    name: str


class _Root(TypedDict):
    item: list[GlobalNumberInfo]


class GlobalNumberConfig(TypedDict):
    root: _Root


class GlobalNumberParser(BaseParser[GlobalNumberConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'globalNumber.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'globalNumber.json'

    def parse(self, data: bytes) -> GlobalNumberConfig:
        reader = BytesReader(data)
        result: GlobalNumberConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        num = reader.ReadSignedInt()
        for _ in range(num):
            item: GlobalNumberInfo = {
                'content': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
            }
            result['root']['item'].append(item)

        return result
