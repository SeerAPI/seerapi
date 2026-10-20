from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from seerapi_models.build_model import BaseResModel, ConvertToORM
from seerapi_models.common import ResourceRef

if TYPE_CHECKING:
    from ..factor_design import FactorDesign, FactorDesignORM
    from ..pet import Pet, PetORM, Soulmark, SoulmarkORM
    from ..skill import Skill, SkillORM
    from ._common import Item, ItemORM


class BaseFactor(BaseResModel):
    id: int = Field(primary_key=True, description='因子道具ID', foreign_key='item.id')
    name: str = Field(description='因子道具名称')
    pet_limit: bool = Field(description='该因子兑换的精灵是否具有唯一性')
    pet_consume: int = Field(
        description='兑换精灵所需因子数量',
    )
    skill_consume: int | None = Field(
        default=None,
        description='兑换技能所需因子数量，当因子不可兑换技能时为null',
    )
    soulmark_consume: int | None = Field(
        default=None,
        description='兑换魂印所需因子数量，当因子不可兑换魂印时为null',
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'factor'


class Factor(BaseFactor, ConvertToORM['FactorORM']):
    item: ResourceRef['Item'] = Field(description='因子道具资源引用')
    design: ResourceRef['FactorDesign'] | None = Field(
        default=None,
        description='因子关卡设计资源引用',
    )
    need_pet: ResourceRef['Pet'] | None = Field(
        default=None,
        description='兑换该精灵所需的前置精灵，当不需要前置时为 null',
    )
    pet: ResourceRef['Pet'] = Field(
        default=None,
        description='因子所属的精灵资源引用',
    )
    skill: ResourceRef['Skill'] | None = Field(
        default=None,
        description='因子可兑换的技能资源引用，当因子不可兑换技能时为null',
    )
    soulmark: ResourceRef['Soulmark'] | None = Field(
        default=None,
        description='因子可兑换的魂印资源引用，当因子不可兑换魂印时为null',
    )

    @classmethod
    def get_orm_model(cls) -> type['FactorORM']:
        return FactorORM

    def to_orm(self) -> 'FactorORM':
        return FactorORM(
            id=self.id,
            name=self.name,
            pet_limit=self.pet_limit,
            pet_consume=self.pet_consume,
            skill_consume=self.skill_consume,
            soulmark_consume=self.soulmark_consume,
            need_pet_id=self.need_pet.id if self.need_pet else None,
            pet_id=self.pet.id,
            skill_id=self.skill.id if self.skill else None,
            soulmark_id=self.soulmark.id if self.soulmark else None,
        )


class FactorORM(BaseFactor, table=True):
    item: 'ItemORM' = Relationship(back_populates='factor')
    design: Optional['FactorDesignORM'] = Relationship(
        back_populates='reward',
        sa_relationship_kwargs={'uselist': False},
    )
    need_pet_id: int | None = Field(default=None, foreign_key='pet.id')
    need_pet: Optional['PetORM'] = Relationship(
        back_populates='required_by_factor',
        sa_relationship_kwargs={
            'foreign_keys': '[FactorORM.need_pet_id]',
        },
    )
    pet_id: int = Field(foreign_key='pet.id')
    pet: 'PetORM' = Relationship(
        back_populates='factor',
        sa_relationship_kwargs={
            'foreign_keys': '[FactorORM.pet_id]',
        },
    )
    skill_id: int | None = Field(default=None, foreign_key='skill.id')
    skill: Optional['SkillORM'] = Relationship(back_populates='factor')
    soulmark_id: int | None = Field(default=None, foreign_key='soulmark.id')
    soulmark: Optional['SoulmarkORM'] = Relationship(back_populates='factor')
