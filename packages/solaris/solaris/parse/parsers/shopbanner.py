from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ShopbannerItem(TypedDict):
    endtime: str
    gotoaddress: str
    pic: str
    starttime: str
    gototype: int
    id: int
    sequence: int


class _ShopbannerData(TypedDict):
    item: list[ShopbannerItem]


class ShopbannerParser(BaseParser[_ShopbannerData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'shopbanner.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'shopbanner.json'

    def parse(self, data: bytes) -> _ShopbannerData:
        reader = BytesReader(data)
        result: _ShopbannerData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ShopbannerItem = {
                'endtime': reader.ReadUTFBytesWithLength(),
                'gotoaddress': reader.ReadUTFBytesWithLength(),
                'gototype': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'pic': reader.ReadUTFBytesWithLength(),
                'sequence': reader.ReadSignedInt(),
                'starttime': reader.ReadUTFBytesWithLength(),
            }
            result['item'].append(item)

        return result
