from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class RechargeItem(TypedDict):
    name: str
    quantity: str
    give: int
    heat: int
    id: int
    money: int
    product_id: int
    type: int


class _RechargeData(TypedDict):
    item: list[RechargeItem]


class RechargeParser(BaseParser[_RechargeData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'recharge.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'recharge.json'

    def parse(self, data: bytes) -> _RechargeData:
        reader = BytesReader(data)
        result: _RechargeData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: RechargeItem = {
                'give': reader.ReadSignedInt(),
                'heat': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'money': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
                'product_id': reader.ReadSignedInt(),
                'quantity': reader.ReadUTFBytesWithLength(),
                'type': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
