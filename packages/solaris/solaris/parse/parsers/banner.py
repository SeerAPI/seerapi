from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _Item(TypedDict):
    finish_time: str
    id: int
    image: str
    is_show: int
    sort: int
    start_time: str
    target: int


class _Data(TypedDict):
    data: list[_Item]


class BannerParser(BaseParser[_Data]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'banner.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'banner.json'

    def parse(self, data: bytes) -> _Data:
        reader = BytesReader(data)
        result: _Data = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: _Item = {
                'finish_time': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'image': reader.ReadUTFBytesWithLength(),
                'is_show': reader.ReadSignedInt(),
                'sort': reader.ReadSignedInt(),
                'start_time': reader.ReadUTFBytesWithLength(),
                'target': reader.ReadSignedInt(),
            }
            result['data'].append(item)

        return result


class BannerBisaifuParser(BaseParser[_Data]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'banner_bisaifu.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'bannerBisaifu.json'

    def parse(self, data: bytes) -> _Data:
        reader = BytesReader(data)
        result: _Data = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: _Item = {
                'finish_time': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'image': reader.ReadUTFBytesWithLength(),
                'is_show': reader.ReadSignedInt(),
                'sort': reader.ReadSignedInt(),
                'start_time': reader.ReadUTFBytesWithLength(),
                'target': reader.ReadSignedInt(),
            }
            result['data'].append(item)

        return result
