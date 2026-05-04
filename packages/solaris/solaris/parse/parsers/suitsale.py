from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class SuitsaleItem(TypedDict):
    id: int
    itemid: int
    normalprice: int
    specialprice: int
    type: int


class _SuitsaleData(TypedDict):
    item: list[SuitsaleItem]


class SuitsaleParser(BaseParser[_SuitsaleData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'suitsale.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'suitsale.json'

    def parse(self, data: bytes) -> _SuitsaleData:
        reader = BytesReader(data)
        result: _SuitsaleData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: SuitsaleItem = {
                'id': reader.ReadSignedInt(),
                'itemid': reader.ReadSignedInt(),
                'normalprice': reader.ReadSignedInt(),
                'specialprice': reader.ReadSignedInt(),
                'type': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
