from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class FightTestLevelConfigItem(TypedDict):
    boss_intro: str
    fight_boss_indexes: str
    first_reward: str
    first_reward_txt: str
    monster_name: str
    reward: str
    reward_txt: str
    battle_mode: int
    index: int
    monster_id: int
    new_msglog_id: int
    order: int
    unlock_monster_cond_id: int
    unlock_monster_index: int
    unlock_msglog_id: int
    unlock_pos: int


class _FightTestLevelConfigRoot(TypedDict):
    item: list[FightTestLevelConfigItem]


class FightTestLevelConfigData(TypedDict):
    root: _FightTestLevelConfigRoot


class FightTestLevelConfigParser(BaseParser[FightTestLevelConfigData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'fightTestLevelConfig.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'fightTestLevelConfig.json'

    def parse(self, data: bytes) -> FightTestLevelConfigData:
        reader = BytesReader(data)
        result: FightTestLevelConfigData = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: FightTestLevelConfigItem = {
                'new_msglog_id': reader.ReadSignedInt(),
                'unlock_monster_cond_id': reader.ReadSignedInt(),
                'unlock_monster_index': reader.ReadSignedInt(),
                'unlock_msglog_id': reader.ReadSignedInt(),
                'unlock_pos': reader.ReadSignedInt(),
                'battle_mode': reader.ReadSignedInt(),
                'boss_intro': reader.ReadUTFBytesWithLength(),
                'fight_boss_indexes': reader.ReadUTFBytesWithLength(),
                'first_reward': reader.ReadUTFBytesWithLength(),
                'first_reward_txt': reader.ReadUTFBytesWithLength(),
                'index': reader.ReadSignedInt(),
                'monster_id': reader.ReadSignedInt(),
                'monster_name': reader.ReadUTFBytesWithLength(),
                'order': reader.ReadSignedInt(),
                'reward': reader.ReadUTFBytesWithLength(),
                'reward_txt': reader.ReadUTFBytesWithLength(),
            }
            result['root']['item'].append(item)

        return result
