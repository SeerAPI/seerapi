from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class DungeonEnterItem(TypedDict):
    name: str
    open_param: str
    res: str
    time_limit: str
    reward: list[int]
    times: list[int]
    id: int
    is_open: int
    is_show: int
    module_id: int
    order: int
    redbadge: int
    show_type: int
    type: int


class _DungeonEnterData(TypedDict):
    item: list[DungeonEnterItem]


class DungeonEnterParser(BaseParser[_DungeonEnterData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'dungeon_enter.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'dungeonEnter.json'

    def parse(self, data: bytes) -> _DungeonEnterData:
        reader = BytesReader(data)
        result: _DungeonEnterData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            _id = reader.ReadSignedInt()
            is_open = reader.ReadSignedInt()
            is_show = reader.ReadSignedInt()
            module_id = reader.ReadSignedInt()
            name = reader.ReadUTFBytesWithLength()
            open_param = reader.ReadUTFBytesWithLength()
            order = reader.ReadSignedInt()
            redbadge = reader.ReadSignedInt()
            res = reader.ReadUTFBytesWithLength()
            reward: list[int] = []
            if reader.ReadBoolean():
                r_count = reader.ReadSignedInt()
                reward = [reader.ReadSignedInt() for _ in range(r_count)]
            show_type = reader.ReadSignedInt()
            time_limit = reader.ReadUTFBytesWithLength()
            times: list[int] = []
            if reader.ReadBoolean():
                t_count = reader.ReadSignedInt()
                times = [reader.ReadSignedInt() for _ in range(t_count)]
            _type = reader.ReadSignedInt()
            item: DungeonEnterItem = {
                'name': name,
                'open_param': open_param,
                'res': res,
                'time_limit': time_limit,
                'reward': reward,
                'times': times,
                'id': _id,
                'is_open': is_open,
                'is_show': is_show,
                'module_id': module_id,
                'order': order,
                'redbadge': redbadge,
                'show_type': show_type,
                'type': _type,
            }
            result['item'].append(item)

        return result
