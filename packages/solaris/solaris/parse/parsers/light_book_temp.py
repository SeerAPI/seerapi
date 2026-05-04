from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _Item(TypedDict):
    coin_id: str
    id: int
    monster_id: str
    need_mon_id: str
    newest: int
    price: str


class _Data(TypedDict):
    data: list[_Item]


class LightBookTempParser(BaseParser[_Data]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'light_book_temp.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'lightBookTemp.json'

    def parse(self, data: bytes) -> _Data:
        reader = BytesReader(data)
        result: _Data = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: _Item = {
                'coin_id': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'monster_id': reader.ReadUTFBytesWithLength(),
                'need_mon_id': reader.ReadUTFBytesWithLength(),
                'newest': reader.ReadSignedInt(),
                'price': reader.ReadUTFBytesWithLength(),
            }
            result['data'].append(item)

        return result
