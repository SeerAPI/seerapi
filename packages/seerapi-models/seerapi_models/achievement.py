from enum import Enum
from typing import Optional, cast

from sqlmodel import Field, Relationship, SQLModel

from seerapi_models.build_model import BaseCategoryModel, BaseResModel, ConvertToORM
from seerapi_models.common import ResourceRef, SixAttributes, SixAttributesORMBase


class AchievementCategoryNameEnum(str, Enum):
    ability_achievement = 'ability_achievement'
    hide_achievement = 'hide_achievement'


class AbilityBonusMixin(SQLModel):
    """能力加成字段的混入类"""

    is_ability_bonus: bool = Field(description='是否是能力加成成就')
    ability_desc: str | None = Field(default=None, description='能力加成描述')


class TitleInfoMixin(SQLModel):
    """称号信息字段的混入类"""

    name: str = Field(description='称号名称')
    original_name: str = Field(description='称号原始名称，包含分隔符')


class TitleAttrBonusORM(SixAttributesORMBase, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
        foreign_key='title_part.id',
        description='成就能力加成属性ID',
    )
    title_part: 'TitlePartORM' = Relationship(
        back_populates='attr_bonus',
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'title_attr_bonus'


class BaseAchievement(BaseResModel):
    id: int = Field(
        primary_key=True,
        description='成就ID，由 SeerAPI 生成，游戏内不存在该ID',
    )

    name: str = Field(description='成就名称')
    point: int = Field(description='成就点数')
    desc: str = Field(description='成就描述')
    is_hide: bool = Field(
        description='是否是隐藏成就，隐藏成就在游戏成就列表中不会显示'
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'achievement'


class AchievementRefsMixin(SQLModel):
    type: ResourceRef['AchievementType'] = Field(description='成就类型')
    branch: ResourceRef['AchievementBranch'] = Field(description='成就所属的分支')
    next_level_achievement: ResourceRef['Achievement'] | None = Field(
        default=None, description='下一级成就'
    )
    prev_level_achievement: ResourceRef['Achievement'] | None = Field(
        default=None, description='上一级成就'
    )
    attr_bonus: SixAttributes | None = Field(
        default=None,
        description='成就能力加成属性，该值仅在成就有能力加成且为数值加成时不为空',
    )


class Achievement(
    BaseAchievement,
    AchievementRefsMixin,
    AbilityBonusMixin,
    ConvertToORM['AchievementORM'],
):
    """成就资源"""

    title_id: int | None = Field(default=None, description='称号ID')
    title: str | None = Field(default=None, description='成就称号')
    original_title: str | None = Field(
        default=None, description='成就称号原始名称，包含分隔符'
    )

    @classmethod
    def get_orm_model(cls) -> 'type[AchievementORM]':
        return AchievementORM

    def to_orm(self) -> 'AchievementORM':
        if self.title_id is not None:
            title_part = TitlePartORM(
                id=self.title_id,
                achievement_id=self.id,
                name=cast(str, self.title),
                original_name=cast(str, self.original_title),
                ability_desc=self.ability_desc,
                attr_bonus=TitleAttrBonusORM(**self.attr_bonus.model_dump())
                if self.attr_bonus
                else None,
            )
        else:
            title_part = None

        return AchievementORM(
            id=self.id,
            name=self.name,
            point=self.point,
            desc=self.desc,
            is_hide=self.is_hide,
            type_id=self.type.id,
            branch_id=self.branch.id,
            next_level_achievement_id=self.next_level_achievement.id
            if self.next_level_achievement
            else None,
            title_part=title_part,
        )

    def to_title(self) -> 'Title | None':
        if self.title_id is None:
            return None

        kwargs = self.model_dump()
        title_id = kwargs.pop('title_id')
        title_name = kwargs.pop('title')
        achievement_id = kwargs.pop('id')
        achievement_name = kwargs.pop('name')

        return Title(
            id=title_id,
            name=title_name,
            original_name=kwargs['original_title'],
            achievement_id=achievement_id,
            achievement_name=achievement_name,
            **kwargs,
        )


class AchievementORM(BaseAchievement, table=True):
    type_id: int = Field(foreign_key='achievement_type.id')
    type: 'AchievementTypeORM' = Relationship(
        back_populates='achievement',
        sa_relationship_kwargs={
            'primaryjoin': 'AchievementORM.type_id == AchievementTypeORM.id',
        },
    )
    branch_id: int = Field(foreign_key='achievement_branch.id')
    branch: 'AchievementBranchORM' = Relationship(
        back_populates='achievement',
        sa_relationship_kwargs={
            'primaryjoin': 'AchievementORM.branch_id == AchievementBranchORM.id',
        },
    )
    next_level_achievement_id: int | None = Field(
        default=None, foreign_key='achievement.id'
    )
    next_level_achievement: Optional['AchievementORM'] = Relationship(
        back_populates='prev_level_achievement',
        sa_relationship_kwargs={
            'foreign_keys': '[AchievementORM.next_level_achievement_id]',
            'primaryjoin': (
                'AchievementORM.next_level_achievement_id == AchievementORM.id'
            ),
            'remote_side': 'AchievementORM.id',
            'uselist': False,
        },
    )
    prev_level_achievement: Optional['AchievementORM'] = Relationship(
        back_populates='next_level_achievement',
        sa_relationship_kwargs={
            'uselist': False,
        },
    )
    title_part: Optional['TitlePartORM'] = Relationship(
        back_populates='achievement',
        sa_relationship_kwargs={
            'uselist': False,
        },
    )


class BaseTitle(BaseAchievement, AbilityBonusMixin):
    id: int = Field(description='称号ID')
    achievement_id: int = Field('成就ID，由 SeerAPI 生成，游戏内不存在该ID')
    achievement_name: str = Field(description='成就名称')
    name: str = Field(description='称号名称')
    original_name: str = Field(description='称号原始名称，包含分隔符')

    @classmethod
    def resource_name(cls) -> str:
        return 'title'


class Title(BaseTitle, AchievementRefsMixin):
    """成就称号资源"""


class TitlePartORM(BaseResModel, TitleInfoMixin, table=True):
    ability_desc: str | None = Field(default=None, description='能力加成描述')

    achievement: list['AchievementORM'] = Relationship(
        back_populates='title_part',
        sa_relationship_kwargs={
            'primaryjoin': 'TitlePartORM.achievement_id == AchievementORM.id',
        },
    )
    achievement_id: int = Field(foreign_key='achievement.id')
    attr_bonus: Optional['TitleAttrBonusORM'] = Relationship(
        back_populates='title_part',
        sa_relationship_kwargs={
            'uselist': False,
            'primaryjoin': 'TitlePartORM.id == TitleAttrBonusORM.id',
        },
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'title_part'


class BaseAchievementType(BaseCategoryModel):
    name: str = Field(description='成就类型名称')
    point_total: int = Field(description='该类型下成就点数总和')

    @classmethod
    def resource_name(cls) -> str:
        return 'achievement_type'


class AchievementType(BaseAchievementType, ConvertToORM['AchievementTypeORM']):
    """成就类型资源"""

    achievement: list[ResourceRef['Achievement']] = Field(
        default_factory=list, description='该类型下的成就'
    )
    branch: list[ResourceRef['AchievementBranch']] = Field(
        default_factory=list, description='该类型下的成就分支'
    )

    @classmethod
    def get_orm_model(cls) -> type['AchievementTypeORM']:
        return AchievementTypeORM

    def to_orm(self) -> 'AchievementTypeORM':
        return AchievementTypeORM(
            id=self.id,
            name=self.name,
            point_total=self.point_total,
        )


class AchievementTypeORM(BaseAchievementType, table=True):
    achievement: list['AchievementORM'] = Relationship(
        back_populates='type',
    )
    branch: list['AchievementBranchORM'] = Relationship(
        back_populates='type',
    )


class BaseAchievementBranch(BaseCategoryModel):
    name: str = Field(description='成就分支名称')
    point_total: int = Field(description='该分支下成就点数总和')
    is_series: bool = Field(
        description='表示该分支下的成就是否是系列成就，当该值为False时，成就彼此之间独立。'
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'achievement_branch'


class AchievementBranch(BaseAchievementBranch, ConvertToORM['AchievementBranchORM']):
    """成就分支资源，当is_series为True时，分支存放同一个系列的成就，反之仅作为分类使用"""

    achievement: list[ResourceRef['Achievement']] = Field(
        default_factory=list, description='该分支下的成就'
    )
    type: ResourceRef['AchievementType'] = Field(description='成就所属的类型')

    @classmethod
    def get_orm_model(cls) -> 'type[AchievementBranchORM]':
        return AchievementBranchORM

    def to_orm(self) -> 'AchievementBranchORM':
        return AchievementBranchORM(
            id=self.id,
            name=self.name,
            is_series=self.is_series,
            point_total=self.point_total,
            type_id=self.type.id,
        )


class AchievementBranchORM(BaseAchievementBranch, table=True):
    achievement: list['AchievementORM'] = Relationship(
        back_populates='branch',
    )
    type_id: int = Field(foreign_key='achievement_type.id')
    type: 'AchievementTypeORM' = Relationship(back_populates='branch')


class BaseAchievementCategory(BaseCategoryModel, use_enum_values=True):
    name: AchievementCategoryNameEnum = Field(
        description='成就分类名称，'
        '`hide_achievement`表示分类下隐藏成就，'
        '`ability_achievement`表示仅包含能力加成成就'
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'achievement_category'


class AchievementCategory(BaseAchievementCategory):
    """成就分类资源，用于在API中便捷地获取成就"""

    achievement: list[ResourceRef['Achievement']] = Field(
        default_factory=list, description='该分类下的成就'
    )
