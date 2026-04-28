from typing import TYPE_CHECKING, Optional

from sqlmodel import JSON, Field, Relationship, SQLModel

from .build_model import (
    BaseCategoryModel,
    BaseResModel,
    BaseResModelWithOptionalId,
    ConvertToORM,
)
from .common import ResourceRef, SkillEffectInUse, SkillEffectInUseORM

if TYPE_CHECKING:
    from .element_type import TypeCombination, TypeCombinationORM
    from .mintmark import MintmarkORM
    from .pet import Pet, PetAdvance, PetAdvanceORM, SkillInPetORM


class SkillEffectLink(SQLModel, table=True):
    """技能效果链接表"""

    skill_id: int | None = Field(default=None, foreign_key='skill.id', primary_key=True)
    effect_in_use_id: int | None = Field(
        default=None, foreign_key='skill_effect_in_use.id', primary_key=True
    )


class SkillFriendSkillEffectLink(SQLModel, table=True):
    """伙伴系统强化技能效果链接表"""

    skill_id: int | None = Field(default=None, foreign_key='skill.id', primary_key=True)
    effect_in_use_id: int | None = Field(
        default=None, foreign_key='skill_effect_in_use.id', primary_key=True
    )


class EffectParamLink(SQLModel, table=True):
    """技能效果参数链接表"""

    effect_id: int | None = Field(
        default=None, foreign_key='skill_effect_type.id', primary_key=True
    )
    param_in_type_id: int | None = Field(
        default=None, foreign_key='skill_effect_param_in_type.id', primary_key=True
    )


class SkillEffectTypeTagLink(SQLModel, table=True):
    effect_id: int | None = Field(
        default=None, foreign_key='skill_effect_type.id', primary_key=True
    )
    tag_id: int | None = Field(
        default=None, foreign_key='skill_effect_type_tag.id', primary_key=True
    )


class SkillEffectParam(BaseResModel, ConvertToORM['SkillEffectParamORM']):
    infos: list[str] | None = Field(
        default=None,
        description='参数类型描述列表',
        sa_type=JSON,
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_effect_param'

    @classmethod
    def get_orm_model(cls) -> type['SkillEffectParamORM']:
        return SkillEffectParamORM

    def to_orm(self) -> 'SkillEffectParamORM':
        return SkillEffectParamORM(
            id=self.id,
            infos=self.infos,
        )


class SkillEffectParamORM(SkillEffectParam, table=True):
    in_type: list['SkillEffectParamInTypeORM'] = Relationship(
        back_populates='param',
    )


class SkillEffectParamInTypeBase(BaseResModelWithOptionalId):
    position: int = Field(description='参数位置')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_effect_param_in_type'


class SkillEffectParamInType(
    SkillEffectParamInTypeBase, ConvertToORM['SkillEffectParamInTypeORM']
):
    param: ResourceRef[SkillEffectParam] = Field(description='参数类型引用')

    @classmethod
    def get_orm_model(cls) -> type['SkillEffectParamInTypeORM']:
        return SkillEffectParamInTypeORM

    def to_orm(self) -> 'SkillEffectParamInTypeORM':
        return SkillEffectParamInTypeORM(
            id=self.id,
            param_id=self.param.id,
            position=self.position,
        )


class SkillEffectParamInTypeORM(SkillEffectParamInTypeBase, table=True):
    param_id: int = Field(foreign_key='skill_effect_param.id')
    param: 'SkillEffectParamORM' = Relationship(back_populates='in_type')
    effect: 'SkillEffectTypeORM' = Relationship(
        back_populates='param', link_model=EffectParamLink
    )


class SkillEffectTypeBase(BaseResModel):
    """描述一条技能效果类型"""

    args_num: int = Field(description='参数数量')
    info: str = Field(description='效果描述')
    info_formatting_adjustment: str | None = Field(
        default=None,
        description='效果描述的"可格式化版本"，用于呈现Unity端中的多行描述形式',
    )
    analyze_info: str = Field(description='新版 Unity 端采用的格式化技能效果描述文本')
    pve_effective: bool = Field(description='该效果是否PVE生效')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_effect_type'


class SkillEffectType(SkillEffectTypeBase, ConvertToORM['SkillEffectTypeORM']):
    param: list[SkillEffectParamInType] | None = Field(
        default=None, description='参数类型列表，描述参数类型和参数位置'
    )
    skill: list[ResourceRef['Skill']] = Field(
        default_factory=list, description='使用该效果的技能列表'
    )
    tag: list[ResourceRef['SkillEffectTypeTag']] = Field(
        default_factory=list, description='标签列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['SkillEffectTypeORM']:
        return SkillEffectTypeORM

    def to_orm(self) -> 'SkillEffectTypeORM':
        return SkillEffectTypeORM(
            id=self.id,
            args_num=self.args_num,
            info=self.info,
            pve_effective=self.pve_effective,
            info_formatting_adjustment=self.info_formatting_adjustment,
            analyze_info=self.analyze_info,
        )


class SkillEffectTypeORM(SkillEffectTypeBase, table=True):
    param: list['SkillEffectParamInTypeORM'] = Relationship(
        back_populates='effect', link_model=EffectParamLink
    )
    tag: list['SkillEffectTypeTagORM'] = Relationship(
        back_populates='effect', link_model=SkillEffectTypeTagLink
    )
    in_use: list['SkillEffectInUseORM'] = Relationship(back_populates='effect')


class SkillCategoryBase(BaseCategoryModel):
    name: str = Field(description='技能分类名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_category'


class SkillCategory(SkillCategoryBase, ConvertToORM['SkillCategoryORM']):
    skill: list[ResourceRef['Skill']] = Field(
        default_factory=list, description='使用该分类的技能列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['SkillCategoryORM']:
        return SkillCategoryORM

    def to_orm(self) -> 'SkillCategoryORM':
        return SkillCategoryORM(
            id=self.id,
            name=self.name,
        )


class SkillCategoryORM(SkillCategoryBase, table=True):
    skill: list['SkillORM'] = Relationship(back_populates='category')


class SkillHideEffectBase(BaseCategoryModel):
    name: str = Field(description='技能隐藏效果名称')
    description: str = Field(description='技能隐藏效果描述')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_hide_effect'


class SkillHideEffect(SkillHideEffectBase, ConvertToORM['SkillHideEffectORM']):
    skill: list[ResourceRef['Skill']] = Field(
        default_factory=list, description='使用该隐藏效果的技能列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['SkillHideEffectORM']:
        return SkillHideEffectORM

    def to_orm(self) -> 'SkillHideEffectORM':
        return SkillHideEffectORM(
            id=self.id,
            name=self.name,
            description=self.description,
        )


class SkillHideEffectORM(SkillHideEffectBase, table=True):
    skill: list['SkillORM'] = Relationship(back_populates='hide_effect')


class SkillEffectTypeTagBase(BaseCategoryModel):
    name: str = Field(description='标签名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_effect_type_tag'


class SkillEffectTypeTag(SkillEffectTypeTagBase, ConvertToORM['SkillEffectTypeTagORM']):
    effect: list[ResourceRef['SkillEffectType']] = Field(
        default_factory=list, description='技能效果类型列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['SkillEffectTypeTagORM']:
        return SkillEffectTypeTagORM

    def to_orm(self) -> 'SkillEffectTypeTagORM':
        return SkillEffectTypeTagORM(id=self.id, name=self.name)


class SkillEffectTypeTagORM(SkillEffectTypeTagBase, table=True):
    effect: list['SkillEffectTypeORM'] = Relationship(
        back_populates='tag', link_model=SkillEffectTypeTagLink
    )


class SkillBase(BaseResModel):
    name: str = Field(description='技能名称')
    power: int = Field(description='技能威力')
    max_pp: int = Field(description='技能最大PP')
    accuracy: int = Field(description='技能命中率')
    crit_rate: float | None = Field(
        description='技能暴击率, 该技能无法暴击时为null（例如属性技能）'
    )
    priority: int = Field(description='技能优先级')
    must_hit: bool = Field(description='技能是否必定命中')
    atk_num: int = Field(default=1, description='组队对战中技能可作用目标数量，默认为1')
    info: str | None = Field(default=None, description='技能描述')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill'


class Skill(SkillBase, ConvertToORM['SkillORM']):
    category: ResourceRef[SkillCategory] = Field(description='技能分类')
    type: ResourceRef['TypeCombination'] = Field(description='技能属性')
    learned_by_pet: list[ResourceRef['Pet']] = Field(
        default_factory=list, description='可学习该技能的精灵列表'
    )
    skill_effect: list[SkillEffectInUse] = Field(
        default_factory=list, description='技能效果列表'
    )
    friend_skill_effect: list[SkillEffectInUse] = Field(
        default_factory=list,
        description='旧版伙伴系统强化后的技能效果',
    )
    hide_effect: ResourceRef[SkillHideEffect] | None = Field(
        default=None, description='技能隐藏效果'
    )
    advance: ResourceRef['PetAdvance'] | None = Field(
        default=None,
        description='技能觉醒信息，仅在该技能是通过神谕觉醒开启的技能时生效',
    )

    @classmethod
    def get_orm_model(cls) -> 'type[SkillORM]':
        return SkillORM

    def to_orm(self) -> 'SkillORM':
        return SkillORM(
            id=self.id,
            name=self.name,
            power=self.power,
            max_pp=self.max_pp,
            accuracy=self.accuracy,
            crit_rate=self.crit_rate,
            priority=self.priority,
            must_hit=self.must_hit,
            info=self.info,
            category_id=self.category.id,
            type_id=self.type.id,
            hide_effect_id=self.hide_effect.id if self.hide_effect else None,
            atk_num=self.atk_num,
            advance_id=self.advance.id if self.advance else None,
        )


class SkillORM(SkillBase, table=True):
    category_id: int = Field(foreign_key='skill_category.id')
    category: SkillCategoryORM = Relationship(back_populates='skill')
    type_id: int = Field(foreign_key='element_type_combination.id')
    type: 'TypeCombinationORM' = Relationship(
        back_populates='skill',
    )
    mintmark: list['MintmarkORM'] = Relationship(
        back_populates='skill',
        sa_relationship_kwargs={
            'secondary': 'skillmintmarklink',
        },
    )
    skill_effect: list[SkillEffectInUseORM] = Relationship(
        back_populates='skill', link_model=SkillEffectLink
    )
    friend_skill_effect: list[SkillEffectInUseORM] = Relationship(
        back_populates='skill', link_model=SkillFriendSkillEffectLink
    )
    hide_effect_id: int | None = Field(default=None, foreign_key='skill_hide_effect.id')
    hide_effect: SkillHideEffectORM | None = Relationship(back_populates='skill')

    pet_links: list['SkillInPetORM'] = Relationship(
        back_populates='skill',
    )

    advance_id: int | None = Field(default=None, foreign_key='pet_advance.id')
    advance: Optional['PetAdvanceORM'] = Relationship(back_populates='skill')
