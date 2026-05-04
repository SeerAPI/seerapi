from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ExchangeRestrictItem(TypedDict):
    id: int
    key: str


class _ExchangeRestrictData(TypedDict):
    item: list[ExchangeRestrictItem]


class ExchangeRestrictParser(BaseParser[_ExchangeRestrictData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'exchangeRestrict.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'exchangeRestrict.json'

    def parse(self, data: bytes) -> _ExchangeRestrictData:
        reader = BytesReader(data)
        result: _ExchangeRestrictData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ExchangeRestrictItem = {
                'id': reader.ReadSignedInt(),
                'key': reader.ReadUTFBytesWithLength(),
            }
            result['item'].append(item)

        return result
