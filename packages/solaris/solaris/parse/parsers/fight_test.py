from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class FightTestBossConfigItem(TypedDict):
    base_data: list[int]
    extra_data: list[int]
    mintmark_data: list[int]
    monster_move: list[int]
    id: int
    monster_effect_id: int
    monster_id: int


class _FightTestBossConfigData(TypedDict):
    item: list[FightTestBossConfigItem]


class FightTestBossConfigParser(BaseParser[_FightTestBossConfigData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'fightTestBossConfig.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'fightTestBossConfig.json'

    def parse(self, data: bytes) -> _FightTestBossConfigData:
        reader = BytesReader(data)
        result: _FightTestBossConfigData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            base_data: list[int] = []
            if reader.ReadBoolean():
                bdc = reader.ReadSignedInt()
                base_data = [reader.ReadSignedInt() for _ in range(bdc)]
            extra_data: list[int] = []
            if reader.ReadBoolean():
                edc = reader.ReadSignedInt()
                extra_data = [reader.ReadSignedInt() for _ in range(edc)]
            item_id = reader.ReadSignedInt()
            mintmark_data: list[int] = []
            if reader.ReadBoolean():
                mdc = reader.ReadSignedInt()
                mintmark_data = [reader.ReadSignedInt() for _ in range(mdc)]
            monster_effect_id = reader.ReadSignedInt()
            monster_id = reader.ReadSignedInt()
            monster_move: list[int] = []
            if reader.ReadBoolean():
                mmc = reader.ReadSignedInt()
                monster_move = [reader.ReadSignedInt() for _ in range(mmc)]
            item: FightTestBossConfigItem = {
                'base_data': base_data,
                'extra_data': extra_data,
                'mintmark_data': mintmark_data,
                'monster_move': monster_move,
                'id': item_id,
                'monster_effect_id': monster_effect_id,
                'monster_id': monster_id,
            }
            result['item'].append(item)

        return result


class FightTestMonsterConfigItem(TypedDict):
    base_data: list[int]
    extra_data: list[int]
    mintmark: list[int]
    mintmark_data: list[int]
    monster_learning: list[int]
    monster_move: list[int]
    id: int
    monster_character: int
    monster_effect_id: int
    monster_id: int
    monster_lv: int
    monster_nature: int
    monster_strength: int
    monster_talent: int


class _FightTestMonsterConfigData(TypedDict):
    item: list[FightTestMonsterConfigItem]


class FightTestMonsterConfigParser(BaseParser[_FightTestMonsterConfigData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'fightTestMonsterConfig.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'fightTestMonsterConfig.json'

    def parse(self, data: bytes) -> _FightTestMonsterConfigData:
        reader = BytesReader(data)
        result: _FightTestMonsterConfigData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            base_data: list[int] = []
            if reader.ReadBoolean():
                bdc = reader.ReadSignedInt()
                base_data = [reader.ReadSignedInt() for _ in range(bdc)]
            extra_data: list[int] = []
            if reader.ReadBoolean():
                edc = reader.ReadSignedInt()
                extra_data = [reader.ReadSignedInt() for _ in range(edc)]
            item_id = reader.ReadSignedInt()
            mintmark: list[int] = []
            if reader.ReadBoolean():
                mc = reader.ReadSignedInt()
                mintmark = [reader.ReadSignedInt() for _ in range(mc)]
            mintmark_data: list[int] = []
            if reader.ReadBoolean():
                mdc = reader.ReadSignedInt()
                mintmark_data = [reader.ReadSignedInt() for _ in range(mdc)]
            monster_character = reader.ReadSignedInt()
            monster_effect_id = reader.ReadSignedInt()
            monster_id = reader.ReadSignedInt()
            monster_learning: list[int] = []
            if reader.ReadBoolean():
                mlc = reader.ReadSignedInt()
                monster_learning = [reader.ReadSignedInt() for _ in range(mlc)]
            monster_lv = reader.ReadSignedInt()
            monster_move: list[int] = []
            if reader.ReadBoolean():
                mmc = reader.ReadSignedInt()
                monster_move = [reader.ReadSignedInt() for _ in range(mmc)]
            monster_nature = reader.ReadSignedInt()
            monster_strength = reader.ReadSignedInt()
            monster_talent = reader.ReadSignedInt()
            item: FightTestMonsterConfigItem = {
                'base_data': base_data,
                'extra_data': extra_data,
                'mintmark': mintmark,
                'mintmark_data': mintmark_data,
                'monster_learning': monster_learning,
                'monster_move': monster_move,
                'id': item_id,
                'monster_character': monster_character,
                'monster_effect_id': monster_effect_id,
                'monster_id': monster_id,
                'monster_lv': monster_lv,
                'monster_nature': monster_nature,
                'monster_strength': monster_strength,
                'monster_talent': monster_talent,
            }
            result['item'].append(item)

        return result


class FightTestStageConfigItem(TypedDict):
    boss_intro: str
    fight_boss_indexes: list[int]
    fight_monster_indexs: list[int]
    first_reward: list[int]
    reward: list[int]
    equip: int
    id: int
    need_mon_num: int
    order: int
    stage_type: int
    title: int


class _FightTestStageConfigData(TypedDict):
    item: list[FightTestStageConfigItem]


class FightTestStageConfigParser(BaseParser[_FightTestStageConfigData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'fightTestStageConfig.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'fightTestStageConfig.json'

    def parse(self, data: bytes) -> _FightTestStageConfigData:
        reader = BytesReader(data)
        result: _FightTestStageConfigData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            need_mon_num = reader.ReadSignedInt()
            stage_type = reader.ReadSignedInt()
            boss_intro = reader.ReadUTFBytesWithLength()
            equip = reader.ReadSignedInt()
            fight_boss_indexes: list[int] = []
            if reader.ReadBoolean():
                fbc = reader.ReadSignedInt()
                fight_boss_indexes = [reader.ReadSignedInt() for _ in range(fbc)]
            fight_monster_indexs: list[int] = []
            if reader.ReadBoolean():
                fmc = reader.ReadSignedInt()
                fight_monster_indexs = [reader.ReadSignedInt() for _ in range(fmc)]
            first_reward: list[int] = []
            if reader.ReadBoolean():
                frc = reader.ReadSignedInt()
                first_reward = [reader.ReadSignedInt() for _ in range(frc)]
            item_id = reader.ReadSignedInt()
            order = reader.ReadSignedInt()
            reward: list[int] = []
            if reader.ReadBoolean():
                rc = reader.ReadSignedInt()
                reward = [reader.ReadSignedInt() for _ in range(rc)]
            title = reader.ReadSignedInt()
            item: FightTestStageConfigItem = {
                'boss_intro': boss_intro,
                'fight_boss_indexes': fight_boss_indexes,
                'fight_monster_indexs': fight_monster_indexs,
                'first_reward': first_reward,
                'reward': reward,
                'equip': equip,
                'id': item_id,
                'need_mon_num': need_mon_num,
                'order': order,
                'stage_type': stage_type,
                'title': title,
            }
            result['item'].append(item)

        return result
