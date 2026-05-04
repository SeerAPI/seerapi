from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _Item(TypedDict):
    commodity: str
    id: int
    pet_info: str
    price: int
    product_id: int
    tab: int
    type: int
    unique: int
    user_info_bit_pos: int
    user_info_id: int


class _Data(TypedDict):
    data: list[_Item]


class LightAndAarkDeitiesParser(BaseParser[_Data]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'LightAndAarkDeities.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'lightAndAarkDeities.json'

    def parse(self, data: bytes) -> _Data:
        reader = BytesReader(data)
        result: _Data = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: _Item = {
                'commodity': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'pet_info': reader.ReadUTFBytesWithLength(),
                'price': reader.ReadSignedInt(),
                'product_id': reader.ReadSignedInt(),
                'tab': reader.ReadSignedInt(),
                'type': reader.ReadSignedInt(),
                'unique': reader.ReadSignedInt(),
                'user_info_bit_pos': reader.ReadSignedInt(),
                'user_info_id': reader.ReadSignedInt(),
            }
            result['data'].append(item)

        return result
