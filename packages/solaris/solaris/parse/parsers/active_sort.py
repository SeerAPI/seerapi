from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ActiveSortItem(TypedDict):
    controller: str
    dest: str
    finishtime: str
    image: str
    name: str
    statlog: str
    reddotid: list[int]
    daily_red: int
    id: int
    iosreviewshow: int
    isdeadline: int
    isshow: int
    jumptarget: int
    priority: int
    truepos: int
    type: int


class _ActiveSortData(TypedDict):
    item: list[ActiveSortItem]


class ActiveSortParser(BaseParser[_ActiveSortData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'active_sort.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'activeSort.json'

    def parse(self, data: bytes) -> _ActiveSortData:
        reader = BytesReader(data)
        result: _ActiveSortData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            controller = reader.ReadUTFBytesWithLength()
            daily_red = reader.ReadSignedInt()
            dest = reader.ReadUTFBytesWithLength()
            finishtime = reader.ReadUTFBytesWithLength()
            iosreviewshow = reader.ReadSignedInt()
            item_id = reader.ReadSignedInt()
            image = reader.ReadUTFBytesWithLength()
            isdeadline = reader.ReadSignedInt()
            isshow = reader.ReadSignedInt()
            jumptarget = reader.ReadSignedInt()
            name = reader.ReadUTFBytesWithLength()
            priority = reader.ReadSignedInt()
            reddotid: list[int] = []
            if reader.ReadBoolean():
                rc = reader.ReadSignedInt()
                reddotid = [reader.ReadSignedInt() for _ in range(rc)]
            statlog = reader.ReadUTFBytesWithLength()
            truepos = reader.ReadSignedInt()
            _type = reader.ReadSignedInt()
            item: ActiveSortItem = {
                'controller': controller,
                'dest': dest,
                'finishtime': finishtime,
                'image': image,
                'name': name,
                'statlog': statlog,
                'reddotid': reddotid,
                'daily_red': daily_red,
                'id': item_id,
                'iosreviewshow': iosreviewshow,
                'isdeadline': isdeadline,
                'isshow': isshow,
                'jumptarget': jumptarget,
                'priority': priority,
                'truepos': truepos,
                'type': _type,
            }
            result['item'].append(item)

        return result


class ActiveSortBisaifuItem(TypedDict):
    controller: str
    dest: str
    finishtime: str
    image: str
    name: str
    statlog: str
    reddotid: list[int]
    daily_red: int
    id: int
    iosreviewshow: int
    isdeadline: int
    isshow: int
    jumptarget: int
    priority: int
    truepos: int
    type: int


class _ActiveSortBisaifuData(TypedDict):
    item: list[ActiveSortBisaifuItem]


class ActiveSortBisaifuParser(BaseParser[_ActiveSortBisaifuData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'active_sort_bisaifu.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'activeSortBisaifu.json'

    def parse(self, data: bytes) -> _ActiveSortBisaifuData:
        reader = BytesReader(data)
        result: _ActiveSortBisaifuData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            controller = reader.ReadUTFBytesWithLength()
            daily_red = reader.ReadSignedInt()
            dest = reader.ReadUTFBytesWithLength()
            finishtime = reader.ReadUTFBytesWithLength()
            iosreviewshow = reader.ReadSignedInt()
            item_id = reader.ReadSignedInt()
            image = reader.ReadUTFBytesWithLength()
            isdeadline = reader.ReadSignedInt()
            isshow = reader.ReadSignedInt()
            jumptarget = reader.ReadSignedInt()
            name = reader.ReadUTFBytesWithLength()
            priority = reader.ReadSignedInt()
            reddotid: list[int] = []
            if reader.ReadBoolean():
                rc = reader.ReadSignedInt()
                reddotid = [reader.ReadSignedInt() for _ in range(rc)]
            statlog = reader.ReadUTFBytesWithLength()
            truepos = reader.ReadSignedInt()
            _type = reader.ReadSignedInt()
            item: ActiveSortBisaifuItem = {
                'controller': controller,
                'dest': dest,
                'finishtime': finishtime,
                'image': image,
                'name': name,
                'statlog': statlog,
                'reddotid': reddotid,
                'daily_red': daily_red,
                'id': item_id,
                'iosreviewshow': iosreviewshow,
                'isdeadline': isdeadline,
                'isshow': isshow,
                'jumptarget': jumptarget,
                'priority': priority,
                'truepos': truepos,
                'type': _type,
            }
            result['item'].append(item)

        return result
