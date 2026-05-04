from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class GlobalStrInfo(TypedDict):
    content: str
    id: int
    name: str


class _Root(TypedDict):
    item: list[GlobalStrInfo]


class GlobalStrConfig(TypedDict):
    root: _Root


class GlobalStrParser(BaseParser[GlobalStrConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'globalStr.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'globalStr.json'

    def parse(self, data: bytes) -> GlobalStrConfig:
        reader = BytesReader(data)
        result: GlobalStrConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        num = reader.ReadSignedInt()
        for _ in range(num):
            item: GlobalStrInfo = {
                'content': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
            }
            result['root']['item'].append(item)

        return result
