from typing import Optional

from sqlmodel import Field, Relationship

from seerapi_models.build_model import BaseResModel, ConvertToORM
from seerapi_models.common import (
    EidEffectInUse,
    EidEffectInUseORM,
    ResourceRef,
    SixAttributes,
    SixAttributesORMBase,
)

from ._common import Item, ItemORM


class EnergyBeadBase(BaseResModel):
    id: int = Field(primary_key=True, foreign_key='item.id', description='能量珠ID')
    name: str = Field(description='能量珠名称')
    desc: str = Field(description='能量珠描述')
    idx: int = Field(description='能量珠效果ID')
    use_times: int = Field(description='使用次数')

    @classmethod
    def resource_name(cls) -> str:
        return 'energy_bead'


class EnergyBead(EnergyBeadBase, ConvertToORM['EnergyBeadORM']):
    item: ResourceRef['Item'] = Field(description='能量珠物品资源引用')
    effect: EidEffectInUse = Field(description='能量珠效果')
    ability_buff: SixAttributes | None = Field(
        default=None, description='能力加成数值，仅当能量珠效果为属性加成时有效'
    )

    @classmethod
    def get_orm_model(cls) -> type['EnergyBeadORM']:
        return EnergyBeadORM

    def to_orm(self) -> 'EnergyBeadORM':
        return EnergyBeadORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
            idx=self.idx,
            effect_in_use=self.effect.to_orm(),
            use_times=self.use_times,
            ability_buff=EnergyBeadBuffAttrORM(
                **self.ability_buff.model_dump(),
            )
            if self.ability_buff
            else None,
        )


class EnergyBeadORM(EnergyBeadBase, table=True):
    effect_in_use: 'EidEffectInUseORM' = Relationship(
        back_populates='energy_bead',
        sa_relationship_kwargs={
            'primaryjoin': 'EnergyBeadORM.effect_in_use_id == EidEffectInUseORM.id',
        },
    )
    effect_in_use_id: int | None = Field(
        default=None, foreign_key='eid_effect_in_use.id'
    )
    ability_buff: Optional['EnergyBeadBuffAttrORM'] = Relationship(
        back_populates='energy_bead',
        sa_relationship_kwargs={
            'uselist': False,
            'primaryjoin': 'EnergyBeadORM.id == EnergyBeadBuffAttrORM.id',
        },
    )
    item: 'ItemORM' = Relationship(back_populates='energy_bead')


class EnergyBeadBuffAttrORM(SixAttributesORMBase, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
        foreign_key='energy_bead.id',
        description='能量珠能力加成ID',
    )
    energy_bead: 'EnergyBeadORM' = Relationship(
        back_populates='ability_buff',
        sa_relationship_kwargs={
            'uselist': False,
            'primaryjoin': 'EnergyBeadORM.id == EnergyBeadBuffAttrORM.id',
        },
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'energy_bead_buff_attr'
