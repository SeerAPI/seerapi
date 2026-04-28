from typing import ClassVar

from sqlmodel import Field, Relationship

from seerapi_models.build_model import BaseCategoryModel, BaseResModel, ConvertToORM
from seerapi_models.common import (
    EidEffectInUse,
    EidEffectInUseORM,
    ResourceRef,
)


class EffectSeDataBase(BaseResModel):
    name: str = Field(description='名称')
    desc: str = Field(description='描述')


class EffectSeData(EffectSeDataBase):
    __name_fields__: ClassVar[list[str]] = ['name', 'effect_alias']
    effect: EidEffectInUse = Field(description='效果')
    effect_alias: str = Field(
        description='效果别名，命名规则为：[效果名称]_[参数1]_[参数2]_…'
    )


class EffectSeDataORM(EffectSeDataBase):
    effect_in_use_id: int | None = Field(
        default=None, foreign_key='eid_effect_in_use.id'
    )


class VariationEffectBase(BaseResModel):
    @classmethod
    def resource_name(cls) -> str:
        return 'pet_variation'


class VariationEffect(
    VariationEffectBase, EffectSeData, ConvertToORM['VariationEffectORM']
):
    """特质效果"""

    @classmethod
    def get_orm_model(cls) -> type['VariationEffectORM']:
        return VariationEffectORM

    def to_orm(self) -> 'VariationEffectORM':
        return VariationEffectORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
            effect_in_use=self.effect.to_orm(),
        )


class VariationEffectORM(VariationEffectBase, EffectSeDataORM, table=True):
    effect_in_use: 'EidEffectInUseORM' = Relationship(
        back_populates='variation_effect',
    )


class PetEffectBase(EffectSeDataBase):
    star_level: int = Field(description='特性星级')

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_effect'


class PetEffect(PetEffectBase, EffectSeData, ConvertToORM['PetEffectORM']):
    effect_group: ResourceRef['PetEffectGroup'] = Field(
        description='特性组资源引用，同特性的不同星级属于同一组'
    )

    @classmethod
    def get_orm_model(cls) -> type['PetEffectORM']:
        return PetEffectORM

    def to_orm(self) -> 'PetEffectORM':
        return PetEffectORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
            effect_in_use=self.effect.to_orm(),
            star_level=self.star_level,
            effect_group_id=self.effect_group.id,
        )


class PetEffectORM(PetEffectBase, EffectSeDataORM, table=True):
    effect_in_use: 'EidEffectInUseORM' = Relationship(
        back_populates='pet_effect',
    )
    effect_group_id: int = Field(foreign_key='pet_effect_group.id')
    effect_group: 'PetEffectGroupORM' = Relationship(back_populates='effect')


class PetEffectGroupBase(BaseCategoryModel):
    name: str = Field(description='名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_effect_group'


class PetEffectGroup(PetEffectGroupBase, ConvertToORM['PetEffectGroupORM']):
    effect: list[ResourceRef[PetEffect]] = Field(
        default_factory=list, description='特性列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['PetEffectGroupORM']:
        return PetEffectGroupORM

    def to_orm(self) -> 'PetEffectGroupORM':
        return PetEffectGroupORM(
            id=self.id,
            name=self.name,
        )


class PetEffectGroupORM(PetEffectGroupBase, table=True):
    effect: list['PetEffectORM'] = Relationship(
        back_populates='effect_group',
    )
