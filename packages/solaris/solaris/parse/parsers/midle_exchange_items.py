from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class MidleExchangeItemItem(TypedDict):
    exchange_out_cnt: str
    exchange_out_id: str
    name: str
    cat_id: int
    exchange_id: int
    exchange_type: int
    id: int
    max: int
    skin_id: int
    target_id: int


class _MidleExchangeItemsData(TypedDict):
    items: list[MidleExchangeItemItem]


class MidleExchangeItemsParser(BaseParser[_MidleExchangeItemsData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'midleExchangeItems.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'midleExchangeItems.json'

    def parse(self, data: bytes) -> _MidleExchangeItemsData:
        reader = BytesReader(data)
        result: _MidleExchangeItemsData = {'items': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: MidleExchangeItemItem = {
                'exchange_id': reader.ReadSignedInt(),
                'exchange_out_cnt': reader.ReadUTFBytesWithLength(),
                'exchange_out_id': reader.ReadUTFBytesWithLength(),
                'exchange_type': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'max': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
                'skin_id': reader.ReadSignedInt(),
                'target_id': reader.ReadSignedInt(),
                'cat_id': reader.ReadSignedInt(),
            }
            result['items'].append(item)

        return result
