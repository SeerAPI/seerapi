from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class BorucashopItem(TypedDict):
    endtime: int
    id: int
    itemid: int
    price: int
    quantity: int
    quota: int
    starttime: int


class _BorucashopData(TypedDict):
    item: list[BorucashopItem]


class BorucashopParser(BaseParser[_BorucashopData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'borucashop.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'borucashop.json'

    def parse(self, data: bytes) -> _BorucashopData:
        reader = BytesReader(data)
        result: _BorucashopData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: BorucashopItem = {
                'endtime': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'itemid': reader.ReadSignedInt(),
                'price': reader.ReadSignedInt(),
                'quantity': reader.ReadSignedInt(),
                'quota': reader.ReadSignedInt(),
                'starttime': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
