from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class BoxordinaryItem(TypedDict):
    tips: str
    id: int
    itemid: int


class _BoxordinaryData(TypedDict):
    item: list[BoxordinaryItem]


class BoxordinaryParser(BaseParser[_BoxordinaryData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'boxordinary.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'boxordinary.json'

    def parse(self, data: bytes) -> _BoxordinaryData:
        reader = BytesReader(data)
        result: _BoxordinaryData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: BoxordinaryItem = {
                'id': reader.ReadSignedInt(),
                'itemid': reader.ReadSignedInt(),
                'tips': reader.ReadUTFBytesWithLength(),
            }
            result['item'].append(item)

        return result
