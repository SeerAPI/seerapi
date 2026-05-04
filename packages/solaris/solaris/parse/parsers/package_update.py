from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _Item(TypedDict):
    channel: str
    force_update: int
    id: int
    msg: str
    size: int
    title: str
    url: str
    version: int


class _Data(TypedDict):
    data: list[_Item]


class PackageUpdateParser(BaseParser[_Data]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'package_update.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'packageUpdate.json'

    def parse(self, data: bytes) -> _Data:
        reader = BytesReader(data)
        result: _Data = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: _Item = {
                'channel': reader.ReadUTFBytesWithLength(),
                'force_update': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'msg': reader.ReadUTFBytesWithLength(),
                'size': reader.ReadSignedInt(),
                'title': reader.ReadUTFBytesWithLength(),
                'url': reader.ReadUTFBytesWithLength(),
                'version': reader.ReadSignedInt(),
            }
            result['data'].append(item)

        return result
