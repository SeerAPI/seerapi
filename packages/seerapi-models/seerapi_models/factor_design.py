from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import JSON, Field, Relationship, SQLModel

from seerapi_models.build_model import (
    BaseResModel,
    BaseResModelWithOptionalId,
    ConvertToORM,
)
from seerapi_models.common import ResourceRef

if TYPE_CHECKING:
    from .achievement import Achievement, AchievementORM
    from .items import Factor, FactorORM
    from .mintmark import Mintmark, MintmarkORM
    from .pet import Pet, PetORM


class FactorDesignLevel(str, Enum):
    easy = 'easy'
    normal = 'normal'
    hard = 'hard'


class BaseFactorDesignRule(SQLModel):
    tips: str = Field(description='规则提示')
    fail_tips: str = Field(description='规则验证失败时的提示')
    args: list[int] = Field(description='规则参数', sa_type=JSON)
    user_info: list[int] = Field(description='玩家状态查询参数', sa_type=JSON)


class FactorDesignRule(BaseFactorDesignRule):
    id: int = Field(description='关卡内的规则ID')


class BaseFactorDesignTask(BaseResModelWithOptionalId):
    desc: str = Field(description='BOSS描述')
    is_single_pet: bool = Field(description='该BOSS是否为单精灵对战')

    @classmethod
    def resource_name(cls) -> str:
        return 'factor_design_task'


class FactorDesignTask(BaseFactorDesignTask):
    boss_pet: ResourceRef['Pet'] = Field(description='BOSS精灵')


class BaseFactorDesignDifficulty(BaseResModelWithOptionalId):
    level: FactorDesignLevel = Field(description='难度标识')
    reward_count: int = Field(description='通关全部关卡后奖励的道具数量')

    @classmethod
    def resource_name(cls) -> str:
        return 'factor_design_difficulty'


class FactorDesignDifficulty(BaseFactorDesignDifficulty):
    tasks: list[FactorDesignTask] = Field(description='BOSS列表')
    banned_pets: list[ResourceRef['Pet']] = Field(description='该难度禁用的精灵')
    rules: list[FactorDesignRule] = Field(description='当前难度使用的规则')


class BaseFactorDesign(BaseResModel):
    @classmethod
    def resource_name(cls) -> str:
        return 'factor_design'


class FactorDesign(BaseFactorDesign, ConvertToORM['FactorDesignORM']):
    achievement: ResourceRef['Achievement'] | None = Field(
        default=None, description='可通过该因子关卡获得的成就'
    )
    difficulties: list[FactorDesignDifficulty] = Field(description='难度列表')
    reward: ResourceRef['Factor'] = Field(description='通关关卡后获得的奖励')
    mintmark_reward: ResourceRef['Mintmark'] | None = Field(
        default=None,
        description='可在该关卡页面兑换的刻印，当该关卡不支持兑换刻印时为 null',
    )

    @classmethod
    def get_orm_model(cls) -> type['FactorDesignORM']:
        return FactorDesignORM

    def to_orm(self) -> 'FactorDesignORM':
        """构造关卡的完整对象图，同一关卡内的规则由多个难度共享。"""
        definitions: dict[int, FactorDesignRule] = {}
        for difficulty in self.difficulties:
            for rule in difficulty.rules:
                existing = definitions.get(rule.id)
                if existing is not None and existing != rule:
                    raise ValueError(
                        f'Conflicting rule {rule.id} in factor design {self.id}'
                    )
                definitions[rule.id] = rule

        rules = {
            rule_id: FactorDesignRuleORM(
                rule_id=rule_id,
                tips=rule.tips,
                fail_tips=rule.fail_tips,
                args=list(rule.args),
                user_info=list(rule.user_info),
                design_id=self.id,
            )
            for rule_id, rule in definitions.items()
        }
        return FactorDesignORM(
            id=self.id,
            achievement_id=self.achievement.id if self.achievement else None,
            reward_id=self.reward.id,
            mintmark_reward_id=self.mintmark_reward.id
            if self.mintmark_reward
            else None,
            rule_definitions=list(rules.values()),
            difficulties=[
                _difficulty_to_orm(difficulty, position, rules, self.id)
                for position, difficulty in enumerate(self.difficulties)
            ],
        )


class FactorDesignORM(BaseFactorDesign, table=True):
    achievement_id: int | None = Field(default=None, foreign_key='achievement.id')
    achievement: Optional['AchievementORM'] = Relationship()
    reward_id: int = Field(foreign_key='factor.id', unique=True)
    reward: 'FactorORM' = Relationship(back_populates='design')
    mintmark_reward_id: int | None = Field(default=None, foreign_key='mintmark.id')
    mintmark_reward: Optional['MintmarkORM'] = Relationship()
    difficulties: list['FactorDesignDifficultyORM'] = Relationship(
        back_populates='design',
        sa_relationship_kwargs={'order_by': 'FactorDesignDifficultyORM.position'},
    )
    rule_definitions: list['FactorDesignRuleORM'] = Relationship(
        back_populates='design'
    )


class FactorDesignDifficultyORM(BaseFactorDesignDifficulty, table=True):
    design_id: int = Field(foreign_key='factor_design.id')
    design: 'FactorDesignORM' = Relationship(back_populates='difficulties')
    position: int = Field(description='难度在列表中的位置，从0开始')
    tasks: list['FactorDesignTaskORM'] = Relationship(
        back_populates='difficulty',
        sa_relationship_kwargs={'order_by': 'FactorDesignTaskORM.position'},
    )
    rule_links: list['FactorDesignDifficultyRuleLink'] = Relationship(
        back_populates='difficulty',
        sa_relationship_kwargs={
            'order_by': 'FactorDesignDifficultyRuleLink.position',
        },
    )
    banned_pet_links: list['FactorDesignDifficultyBannedPetLink'] = Relationship(
        back_populates='difficulty',
        sa_relationship_kwargs={
            'order_by': 'FactorDesignDifficultyBannedPetLink.position',
        },
    )


class FactorDesignTaskORM(BaseFactorDesignTask, table=True):
    difficulty_id: int = Field(foreign_key='factor_design_difficulty.id')
    difficulty: 'FactorDesignDifficultyORM' = Relationship(back_populates='tasks')
    position: int = Field(description='BOSS在挑战列表中的位置，从0开始')
    boss_pet_id: int = Field(foreign_key='pet.id')
    boss_pet: 'PetORM' = Relationship()


class FactorDesignRuleORM(BaseFactorDesignRule, BaseResModelWithOptionalId, table=True):
    __table_args__ = (UniqueConstraint('design_id', 'rule_id'),)

    design_id: int = Field(foreign_key='factor_design.id')
    design: 'FactorDesignORM' = Relationship(back_populates='rule_definitions')
    rule_id: int = Field(description='关卡内的原始规则ID')
    difficulty_links: list['FactorDesignDifficultyRuleLink'] = Relationship(
        back_populates='rule'
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'factor_design_rule'


class FactorDesignDifficultyRuleLink(SQLModel, table=True):
    difficulty_id: int | None = Field(
        default=None, foreign_key='factor_design_difficulty.id', primary_key=True
    )
    rule_id: int | None = Field(
        default=None, foreign_key='factor_design_rule.id', primary_key=True
    )
    position: int = Field(description='规则在当前难度列表中的位置，从0开始')
    difficulty: 'FactorDesignDifficultyORM' = Relationship(back_populates='rule_links')
    rule: 'FactorDesignRuleORM' = Relationship(back_populates='difficulty_links')


class FactorDesignDifficultyBannedPetLink(SQLModel, table=True):
    difficulty_id: int | None = Field(
        default=None, foreign_key='factor_design_difficulty.id', primary_key=True
    )
    pet_id: int = Field(foreign_key='pet.id', primary_key=True)
    position: int = Field(description='精灵在禁用列表中的位置，从0开始')
    difficulty: 'FactorDesignDifficultyORM' = Relationship(
        back_populates='banned_pet_links'
    )
    pet: 'PetORM' = Relationship()


def _difficulty_to_orm(
    difficulty: FactorDesignDifficulty,
    position: int,
    rules: dict[int, FactorDesignRuleORM],
    design_id: int,
) -> FactorDesignDifficultyORM:
    return FactorDesignDifficultyORM(
        id=difficulty.id,
        design_id=design_id,
        level=difficulty.level,
        reward_count=difficulty.reward_count,
        position=position,
        tasks=[
            FactorDesignTaskORM(
                id=task.id,
                desc=task.desc,
                is_single_pet=task.is_single_pet,
                boss_pet_id=task.boss_pet.id,
                position=task_position,
            )  # type: ignore
            for task_position, task in enumerate(difficulty.tasks)
        ],
        rule_links=[
            FactorDesignDifficultyRuleLink(rule=rules[rule.id], position=rule_position)
            for rule_position, rule in enumerate(difficulty.rules)
        ],
        banned_pet_links=[
            FactorDesignDifficultyBannedPetLink(pet_id=pet.id, position=pet_position)
            for pet_position, pet in enumerate(difficulty.banned_pets)
        ],
    )
