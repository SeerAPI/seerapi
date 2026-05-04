from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _Item(TypedDict):
    id: int
    mon_id: int
    product_id: int
    type: int


class _Data(TypedDict):
    data: list[_Item]


class LightAndAarkPrizeDrawParser(BaseParser[_Data]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'LightAndAarkPrizeDraw.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'lightAndAarkPrizeDraw.json'

    def parse(self, data: bytes) -> _Data:
        reader = BytesReader(data)
        result: _Data = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: _Item = {
                'id': reader.ReadSignedInt(),
                'mon_id': reader.ReadSignedInt(),
                'product_id': reader.ReadSignedInt(),
                'type': reader.ReadSignedInt(),
            }
            result['data'].append(item)

        return result
