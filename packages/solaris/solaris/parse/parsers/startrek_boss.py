from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class StartrekbossconfigItem(TypedDict):
    monster_move: str
    monster_name: str
    monster_newse: str
    atk: int
    def_: int
    hp: int
    id: int
    monster_id: int
    sp_atk: int
    sp_def: int
    spd: int


class _StartrekbossconfigData(TypedDict):
    item: list[StartrekbossconfigItem]


class StartrekbossconfigParser(BaseParser[_StartrekbossconfigData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'Startrekbossconfig.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'startrekbossconfig.json'

    def parse(self, data: bytes) -> _StartrekbossconfigData:
        reader = BytesReader(data)
        result: _StartrekbossconfigData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: StartrekbossconfigItem = {
                'atk': reader.ReadSignedInt(),
                'def_': reader.ReadSignedInt(),
                'hp': reader.ReadSignedInt(),
                'sp_atk': reader.ReadSignedInt(),
                'sp_def': reader.ReadSignedInt(),
                'spd': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'monster_id': reader.ReadSignedInt(),
                'monster_move': reader.ReadUTFBytesWithLength(),
                'monster_name': reader.ReadUTFBytesWithLength(),
                'monster_newse': reader.ReadUTFBytesWithLength(),
            }
            result['item'].append(item)

        return result


class StartrekbossfightItem(TypedDict):
    monster_ids: list[int]
    rewardinfo: list[int]
    bossfight_id: int
    boss_type: int
    id: int
    win_reward_num: int


class _StartrekbossfightData(TypedDict):
    item: list[StartrekbossfightItem]


class StartrekbossfightParser(BaseParser[_StartrekbossfightData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'Startrekbossfight.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'startrekbossfight.json'

    def parse(self, data: bytes) -> _StartrekbossfightData:
        reader = BytesReader(data)
        result: _StartrekbossfightData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            boss_type = reader.ReadSignedInt()
            bossfight_id = reader.ReadSignedInt()
            monster_ids: list[int] = []
            if reader.ReadBoolean():
                mc = reader.ReadSignedInt()
                monster_ids = [reader.ReadSignedInt() for _ in range(mc)]
            win_reward_num = reader.ReadSignedInt()
            item_id = reader.ReadSignedInt()
            rewardinfo: list[int] = []
            if reader.ReadBoolean():
                rc = reader.ReadSignedInt()
                rewardinfo = [reader.ReadSignedInt() for _ in range(rc)]
            item: StartrekbossfightItem = {
                'monster_ids': monster_ids,
                'rewardinfo': rewardinfo,
                'bossfight_id': bossfight_id,
                'boss_type': boss_type,
                'id': item_id,
                'win_reward_num': win_reward_num,
            }
            result['item'].append(item)

        return result


class StartrekbuffinfoItem(TypedDict):
    buff_desc: str
    buff_name: str
    basic_value: list[int]
    buff_id: int
    buff_pond_id: int
    id: int


class _StartrekbuffinfoData(TypedDict):
    item: list[StartrekbuffinfoItem]


class StartrekbuffinfoParser(BaseParser[_StartrekbuffinfoData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'Startrekbuffinfo.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'startrekbuffinfo.json'

    def parse(self, data: bytes) -> _StartrekbuffinfoData:
        reader = BytesReader(data)
        result: _StartrekbuffinfoData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            basic_value: list[int] = []
            if reader.ReadBoolean():
                bvc = reader.ReadSignedInt()
                basic_value = [reader.ReadSignedInt() for _ in range(bvc)]
            buff_desc = reader.ReadUTFBytesWithLength()
            buff_id = reader.ReadSignedInt()
            buff_name = reader.ReadUTFBytesWithLength()
            buff_pond_id = reader.ReadSignedInt()
            item_id = reader.ReadSignedInt()
            item: StartrekbuffinfoItem = {
                'buff_desc': buff_desc,
                'buff_name': buff_name,
                'basic_value': basic_value,
                'buff_id': buff_id,
                'buff_pond_id': buff_pond_id,
                'id': item_id,
            }
            result['item'].append(item)

        return result
