from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PreferentialBestItem(TypedDict):
    canchoose: str
    price: str
    recommendlearningability: str
    skinname: str
    id: int
    iscommon: int
    petid: int
    recommendnature: int


class _PreferentialBestData(TypedDict):
    item: list[PreferentialBestItem]


class PreferentialBestParser(BaseParser[_PreferentialBestData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'PreferentialBest.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'preferentialBest.json'

    def parse(self, data: bytes) -> _PreferentialBestData:
        reader = BytesReader(data)
        result: _PreferentialBestData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: PreferentialBestItem = {
                'canchoose': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'iscommon': reader.ReadSignedInt(),
                'petid': reader.ReadSignedInt(),
                'price': reader.ReadUTFBytesWithLength(),
                'recommendlearningability': reader.ReadUTFBytesWithLength(),
                'recommendnature': reader.ReadSignedInt(),
                'skinname': reader.ReadUTFBytesWithLength(),
            }
            result['item'].append(item)

        return result
