from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _Item(TypedDict):
    details: int
    id: int
    type: int


class _Data(TypedDict):
    data: list[_Item]


class HandbookBanParser(BaseParser[_Data]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'handbook_ban.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'handbookBan.json'

    def parse(self, data: bytes) -> _Data:
        reader = BytesReader(data)
        result: _Data = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: _Item = {
                'details': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'type': reader.ReadSignedInt(),
            }
            result['data'].append(item)

        return result
