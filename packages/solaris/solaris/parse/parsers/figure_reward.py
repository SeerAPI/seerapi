from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class MonsterItem(TypedDict):
    """精灵项"""

    id: int


class ItemItem(TypedDict):
    """物品项"""

    count: int
    id: int


class Ach(TypedDict):
    """成就信息"""

    branch_id: int
    rule_id: int


class LevelItem(TypedDict):
    """等级项"""

    exp_need: int
    id: int
    reward_id: int
    use_bit: int
    use_value: int


class RewardItem(TypedDict):
    """奖励项"""

    head: MonsterItem | None
    head_frame: MonsterItem | None
    id: int
    item: list[ItemItem]
    mintmark: list[ItemItem]
    monster: list[MonsterItem]
    skin: MonsterItem | None
    type: int
    ach: Ach | None


class _Root(TypedDict):
    """根数据结构"""

    level: list[LevelItem]
    reward: list[RewardItem]


class FigureRewardConfig(TypedDict):
    """图鉴奖励配置"""

    root: _Root


class FigureRewardParser(BaseParser[FigureRewardConfig]):
    """图鉴奖励解析器"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'figure_reward.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'figureReward.json'

    def parse(self, data: bytes) -> FigureRewardConfig:
        reader = BytesReader(data)
        result: FigureRewardConfig = {'root': {'level': [], 'reward': []}}

        if not reader.ReadBoolean():
            return result

        if reader.ReadBoolean():
            level_count = reader.ReadSignedInt()
            for _ in range(level_count):
                exp_need = reader.ReadSignedInt()
                level_id = reader.ReadSignedInt()
                reward_id = reader.ReadSignedInt()
                use_bit = reader.ReadSignedInt()
                use_value = reader.ReadSignedInt()

                level_item: LevelItem = {
                    'exp_need': exp_need,
                    'id': level_id,
                    'reward_id': reward_id,
                    'use_bit': use_bit,
                    'use_value': use_value,
                }
                result['root']['level'].append(level_item)

        if reader.ReadBoolean():
            reward_count = reader.ReadSignedInt()
            for _ in range(reward_count):
                head: MonsterItem | None = None
                if reader.ReadBoolean():
                    head = {'id': reader.ReadSignedInt()}

                head_frame: MonsterItem | None = None
                if reader.ReadBoolean():
                    head_frame = {'id': reader.ReadSignedInt()}

                rid = reader.ReadSignedInt()

                item_list: list[ItemItem] = []
                if reader.ReadBoolean():
                    item_count = reader.ReadSignedInt()
                    for _ in range(item_count):
                        item_list.append(
                            {
                                'count': reader.ReadSignedInt(),
                                'id': reader.ReadSignedInt(),
                            }
                        )

                mintmark_list: list[ItemItem] = []
                if reader.ReadBoolean():
                    mintmark_count = reader.ReadSignedInt()
                    for _ in range(mintmark_count):
                        mintmark_list.append(
                            {
                                'count': reader.ReadSignedInt(),
                                'id': reader.ReadSignedInt(),
                            }
                        )

                monster_list: list[MonsterItem] = []
                if reader.ReadBoolean():
                    monster_count = reader.ReadSignedInt()
                    for _ in range(monster_count):
                        monster_list.append({'id': reader.ReadSignedInt()})

                skin: MonsterItem | None = None
                if reader.ReadBoolean():
                    skin = {'id': reader.ReadSignedInt()}

                rtype = reader.ReadSignedInt()

                ach: Ach | None = None
                if reader.ReadBoolean():
                    ach = {
                        'branch_id': reader.ReadSignedInt(),
                        'rule_id': reader.ReadSignedInt(),
                    }

                reward_item: RewardItem = {
                    'head': head,
                    'head_frame': head_frame,
                    'id': rid,
                    'item': item_list,
                    'mintmark': mintmark_list,
                    'monster': monster_list,
                    'skin': skin,
                    'type': rtype,
                    'ach': ach,
                }
                result['root']['reward'].append(reward_item)

        return result
