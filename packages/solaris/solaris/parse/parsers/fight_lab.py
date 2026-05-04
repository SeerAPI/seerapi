from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class FightLabBossConfigItem(TypedDict):
    monster_data: str
    monster_intro: str
    monster_move: str
    monster_newse: str
    id: int
    index: int
    monster_id: int


class _FightLabBossConfigData(TypedDict):
    item: list[FightLabBossConfigItem]


class FightLabBossConfigParser(BaseParser[_FightLabBossConfigData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'fightLabBossConfig.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'fightLabBossConfig.json'

    def parse(self, data: bytes) -> _FightLabBossConfigData:
        reader = BytesReader(data)
        result: _FightLabBossConfigData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: FightLabBossConfigItem = {
                'id': reader.ReadSignedInt(),
                'index': reader.ReadSignedInt(),
                'monster_data': reader.ReadUTFBytesWithLength(),
                'monster_id': reader.ReadSignedInt(),
                'monster_intro': reader.ReadUTFBytesWithLength(),
                'monster_move': reader.ReadUTFBytesWithLength(),
                'monster_newse': reader.ReadUTFBytesWithLength(),
            }
            result['item'].append(item)

        return result


class FightLabLevelConfigItem(TypedDict):
    boss_intro: str
    first_reward_txt: str
    monster_name: str
    reward_txt: str
    first_reward: list[int]
    reward: list[int]
    id: int
    monster_id: int
    order: int


class _FightLabLevelConfigData(TypedDict):
    item: list[FightLabLevelConfigItem]


class FightLabLevelConfigParser(BaseParser[_FightLabLevelConfigData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'fightLabLevelConfig.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'fightLabLevelConfig.json'

    def parse(self, data: bytes) -> _FightLabLevelConfigData:
        reader = BytesReader(data)
        result: _FightLabLevelConfigData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            boss_intro = reader.ReadUTFBytesWithLength()
            first_reward: list[int] = []
            if reader.ReadBoolean():
                frc = reader.ReadSignedInt()
                first_reward = [reader.ReadSignedInt() for _ in range(frc)]
            first_reward_txt = reader.ReadUTFBytesWithLength()
            item_id = reader.ReadSignedInt()
            monster_id = reader.ReadSignedInt()
            monster_name = reader.ReadUTFBytesWithLength()
            order = reader.ReadSignedInt()
            reward: list[int] = []
            if reader.ReadBoolean():
                rc = reader.ReadSignedInt()
                reward = [reader.ReadSignedInt() for _ in range(rc)]
            reward_txt = reader.ReadUTFBytesWithLength()
            item: FightLabLevelConfigItem = {
                'boss_intro': boss_intro,
                'first_reward_txt': first_reward_txt,
                'monster_name': monster_name,
                'reward_txt': reward_txt,
                'first_reward': first_reward,
                'reward': reward,
                'id': item_id,
                'monster_id': monster_id,
                'order': order,
            }
            result['item'].append(item)

        return result


class FightLabMonsterConfigItem(TypedDict):
    monster_intro: str
    monster_data: list[int]
    monster_move: list[int]
    id: int
    monster_id: int


class _FightLabMonsterConfigData(TypedDict):
    item: list[FightLabMonsterConfigItem]


class FightLabMonsterConfigParser(BaseParser[_FightLabMonsterConfigData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'fightLabMonsterConfig.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'fightLabMonsterConfig.json'

    def parse(self, data: bytes) -> _FightLabMonsterConfigData:
        reader = BytesReader(data)
        result: _FightLabMonsterConfigData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item_id = reader.ReadSignedInt()
            monster_data: list[int] = []
            if reader.ReadBoolean():
                mdc = reader.ReadSignedInt()
                monster_data = [reader.ReadSignedInt() for _ in range(mdc)]
            monster_id = reader.ReadSignedInt()
            monster_intro = reader.ReadUTFBytesWithLength()
            monster_move: list[int] = []
            if reader.ReadBoolean():
                mmc = reader.ReadSignedInt()
                monster_move = [reader.ReadSignedInt() for _ in range(mmc)]
            item: FightLabMonsterConfigItem = {
                'monster_intro': monster_intro,
                'monster_data': monster_data,
                'monster_move': monster_move,
                'id': item_id,
                'monster_id': monster_id,
            }
            result['item'].append(item)

        return result
