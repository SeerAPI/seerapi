from typing import TYPE_CHECKING

from seerapi_models import (
    Achievement,
    AchievementBranch,
    Factor,
    FactorDesign,
    FactorDesignDifficulty,
    FactorDesignLevel,
    FactorDesignRule,
    FactorDesignTask,
    Mintmark,
    Pet,
)
from seerapi_models.common import ResourceRef
from solaris.analyze.base import (
    BaseAnalyzer,
    BaseDataSourcePostAnalyzer,
    DataImportConfig,
)
from solaris.analyze.typing_ import AnalyzeResult
from solaris.utils import split_string_arg

from .achievement import AchievementAnalyzer, _achievement_id_generator

if TYPE_CHECKING:
    from solaris.parse.parsers.new_super_design import (
        EasyBattle,
        NewSuperDesignConfig,
        NormalBattle,
    )


class DesignAnalyzer(BaseDataSourcePostAnalyzer):
    """将因子关卡配置整理为关卡、难度、BOSS和规则资源。"""

    @classmethod
    def get_input_analyzers(cls) -> tuple[type[BaseAnalyzer], ...]:
        return (AchievementAnalyzer,)

    @classmethod
    def get_data_import_config(cls) -> DataImportConfig:
        return DataImportConfig(
            unity_paths=('newSuperDesign.json',),
        )

    @classmethod
    def get_result_res_models(cls):
        return (FactorDesign,)

    def analyze(self) -> tuple[AnalyzeResult[FactorDesign], ...]:
        data: NewSuperDesignConfig = self._get_data('unity', 'newSuperDesign.json')
        achievements = self._get_input_data(AchievementAnalyzer, Achievement)
        branches = self._get_input_data(AchievementAnalyzer, AchievementBranch)
        results: dict[int, FactorDesign] = {}

        for item in data['root']['design']:
            design_id = item['id']
            reward = item['reward']
            if reward is None:
                raise ValueError(f'Factor design {design_id} has no reward')

            rule_items = item['rules']['rule'] if item['rules'] is not None else []
            rules = {
                rule['id']: FactorDesignRule(
                    id=rule['id'],
                    tips=rule['check_tips'],
                    fail_tips=rule['fail_tips'],
                    args=split_string_arg(rule['args'], handle_float=False),
                    user_info=split_string_arg(rule['user_info'], handle_float=False),
                )
                for rule in rule_items
            }
            # 规则编号是关卡内的局部编号，mould_id 才决定规则的含义。
            banned_rule_ids = {
                rule['id'] for rule in rule_items if rule['mould_id'] == 3
            }
            difficulties = [
                _analyze_difficulty(design_id, level, battle, rules, banned_rule_ids)
                for level, battle in (
                    (FactorDesignLevel.easy, item['easy_battle']),
                    (FactorDesignLevel.normal, item['normal_battle']),
                    (FactorDesignLevel.hard, item['hard_battle']),
                )
                if battle is not None
            ]

            achievement_ref = None
            achievement = item['achievement']
            if achievement and achievement['branch_id'] and achievement['rule_id']:
                branch = branches[achievement['branch_id']]
                achievement_id = _achievement_id_generator(
                    branch.type.id, branch.id, achievement['rule_id']
                )
                achievement_ref = ResourceRef.from_model(achievements[achievement_id])

            results[design_id] = FactorDesign(
                id=design_id,
                achievement=achievement_ref,
                difficulties=difficulties,
                reward=ResourceRef.from_model(Factor, id=reward['item_id']),
                mintmark_reward=ResourceRef.from_model(
                    Mintmark, id=reward['mint_mark_id']
                )
                if reward['mint_mark_id']
                else None,
            )

        return (AnalyzeResult(FactorDesign, results),)


def _analyze_difficulty(
    design_id: int,
    level: FactorDesignLevel,
    battle: 'EasyBattle | NormalBattle',
    rules: dict[int, FactorDesignRule],
    banned_rule_ids: set[int],
) -> FactorDesignDifficulty:
    # 简单难度没有 rule_id，其余难度按配置中的顺序引用规则。
    selected_rules: list[FactorDesignRule] = []
    for rule_id in split_string_arg(battle.get('rule_id', ''), handle_float=False):
        if rule_id not in rules:
            raise ValueError(
                f'因子关卡 {design_id}（{level.value}）引用了未知规则 {rule_id}'
            )
        selected_rules.append(rules[rule_id])

    banned_pet_ids = [
        pet_id
        for rule in selected_rules
        if rule.id in banned_rule_ids
        for pet_id in rule.args
    ]
    return FactorDesignDifficulty(
        level=level,
        reward_count=battle['out'],
        tasks=[
            FactorDesignTask(
                desc=task['desc'],
                is_single_pet=task['battle_type'] == 1,
                boss_pet=ResourceRef.from_model(Pet, id=task['battle_boss']),
            )
            for task in battle['task']
        ],
        banned_pets=[
            ResourceRef.from_model(Pet, id=pet_id) for pet_id in banned_pet_ids
        ],
        rules=selected_rules,
    )
