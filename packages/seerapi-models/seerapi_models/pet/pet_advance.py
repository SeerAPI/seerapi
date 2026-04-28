from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from seerapi_models.build_model import BaseResModel, ConvertToORM
from seerapi_models.common import ResourceRef, SixAttributes, SixAttributesORMBase

if TYPE_CHECKING:
    from seerapi_models.skill import Skill, SkillORM

    from . import Pet, PetORM, Soulmark, SoulmarkORM


class AdvanceBaseStatORM(SixAttributesORMBase, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
        foreign_key='pet_advance.id',
    )
    advance: 'PetAdvanceORM' = Relationship(back_populates='base_stats')

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_advance_base_stats'


class PetAdvanceBase(BaseResModel):
    id: int = Field(primary_key=True)

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_advance'


class PetAdvance(PetAdvanceBase, ConvertToORM['PetAdvanceORM']):
    pet: ResourceRef['Pet'] = Field(description='该项觉醒对应的精灵')
    skill: list[ResourceRef['Skill']] = Field(description='完成觉醒可开启的技能')
    soulmark: ResourceRef['Soulmark'] = Field(description='完成觉醒可开启的魂印')
    base_stats: SixAttributes = Field(description='觉醒后的种族值')

    @classmethod
    def get_orm_model(cls) -> type['PetAdvanceORM']:
        return PetAdvanceORM

    def to_orm(self) -> 'PetAdvanceORM':
        base_stats = AdvanceBaseStatORM(
            id=self.id,
            **self.base_stats.model_dump(),
        )
        return PetAdvanceORM(
            id=self.id,
            pet_id=self.pet.id,
            base_stats=base_stats,
            soulmark_id=self.soulmark.id,
        )


class PetAdvanceORM(PetAdvanceBase, table=True):
    pet_id: int = Field(foreign_key='pet.id', unique=True)
    pet: 'PetORM' = Relationship(back_populates='advance')
    skill: list['SkillORM'] = Relationship(back_populates='advance')
    soulmark_id: int = Field(foreign_key='soulmark.id', unique=True)
    soulmark: 'SoulmarkORM' = Relationship(back_populates='advance')
    base_stats: 'AdvanceBaseStatORM' = Relationship(
        back_populates='advance',
        sa_relationship_kwargs={
            'uselist': False,
        },
    )
