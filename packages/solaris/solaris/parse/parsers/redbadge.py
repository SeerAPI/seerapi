from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class RedbadgeItem(TypedDict):
    channel: str
    subset: list[int]
    endtime: int
    id: int
    isshow: int
    starttime: int
    subtype: int
    type: int


class _RedbadgeData(TypedDict):
    item: list[RedbadgeItem]


class RedbadgeParser(BaseParser[_RedbadgeData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'redbadge.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'redbadge.json'

    def parse(self, data: bytes) -> _RedbadgeData:
        reader = BytesReader(data)
        result: _RedbadgeData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: RedbadgeItem = {
                'channel': reader.ReadUTFBytesWithLength(),
                'endtime': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'isshow': reader.ReadSignedInt(),
                'starttime': reader.ReadSignedInt(),
                'subset': [],
                'subtype': 0,
                'type': 0,
            }
            if reader.ReadBoolean():
                ss_count = reader.ReadSignedInt()
                item['subset'] = [reader.ReadSignedInt() for _ in range(ss_count)]
            item['subtype'] = reader.ReadSignedInt()
            item['type'] = reader.ReadSignedInt()
            result['item'].append(item)

        return result


class RedbadgeBisaifuItem(TypedDict):
    channel: str
    subset: list[int]
    endtime: int
    id: int
    isshow: int
    starttime: int
    subtype: int
    type: int


class _RedbadgeBisaifuData(TypedDict):
    item: list[RedbadgeBisaifuItem]


class RedbadgeBisaifuParser(BaseParser[_RedbadgeBisaifuData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'redbadge_bisaifu.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'redbadgeBisaifu.json'

    def parse(self, data: bytes) -> _RedbadgeBisaifuData:
        reader = BytesReader(data)
        result: _RedbadgeBisaifuData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: RedbadgeBisaifuItem = {
                'channel': reader.ReadUTFBytesWithLength(),
                'endtime': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'isshow': reader.ReadSignedInt(),
                'starttime': reader.ReadSignedInt(),
                'subset': [],
                'subtype': 0,
                'type': 0,
            }
            if reader.ReadBoolean():
                ss_count = reader.ReadSignedInt()
                item['subset'] = [reader.ReadSignedInt() for _ in range(ss_count)]
            item['subtype'] = reader.ReadSignedInt()
            item['type'] = reader.ReadSignedInt()
            result['item'].append(item)

        return result
