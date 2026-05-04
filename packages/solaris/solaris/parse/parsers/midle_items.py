from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class MidleItemItem(TypedDict):
    name: str
    cat_id: int
    id: int
    max: int


class _MidleItemsData(TypedDict):
    items: list[MidleItemItem]


class MidleItemsParser(BaseParser[_MidleItemsData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'midleItems.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'midleItems.json'

    def parse(self, data: bytes) -> _MidleItemsData:
        reader = BytesReader(data)
        result: _MidleItemsData = {'items': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: MidleItemItem = {
                'id': reader.ReadSignedInt(),
                'max': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
                'cat_id': reader.ReadSignedInt(),
            }
            result['items'].append(item)

        return result
