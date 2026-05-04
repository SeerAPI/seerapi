from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class BitBufferInfo(TypedDict):
    id: int
    index: int


class _Root(TypedDict):
    item: list[BitBufferInfo]


class BitBufferConfig(TypedDict):
    root: _Root


class BitBufferParser(BaseParser[BitBufferConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'bitBuffer.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'bitBuffer.json'

    def parse(self, data: bytes) -> BitBufferConfig:
        reader = BytesReader(data)
        result: BitBufferConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        num = reader.ReadSignedInt()
        for _ in range(num):
            item: BitBufferInfo = {
                'id': reader.ReadSignedInt(),
                'index': reader.ReadSignedInt(),
            }
            result['root']['item'].append(item)

        return result
