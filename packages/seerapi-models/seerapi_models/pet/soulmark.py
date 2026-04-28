from typing import TYPE_CHECKING, ClassVar, Optional

from pydantic import AliasChoices
from sqlmodel import Field, Relationship, SQLModel

from seerapi_models.build_model import (
    BaseCategoryModel,
    BaseResModel,
    ConvertToORM,
)
from seerapi_models.common import EidEffectInUse, EidEffectInUseORM, ResourceRef

if TYPE_CHECKING:
    from .pet import Pet, PetAdvance, PetAdvanceORM, PetORM


class PetSoulmarkLink(SQLModel, table=True):
    pet_id: int | None = Field(default=None, primary_key=True, foreign_key='pet.id')
    soulmark_id: int | None = Field(
        default=None, primary_key=True, foreign_key='soulmark.id'
    )


class SoulmarkTagLink(SQLModel, table=True):
    soulmark_id: int | None = Field(
        default=None, primary_key=True, foreign_key='soulmark.id'
    )
    tag_id: int | None = Field(
        default=None, primary_key=True, foreign_key='soulmark_tag.id'
    )


class SoulmarkBase(BaseResModel):
    desc: str = Field(description='魂印描述')
    desc_formatting_adjustment: str | None = Field(
        default=None,
        description='Unity 客户端历史格式的魂印描述文本（部分旧魂印专用，应优先使用 analyze_desc 字段）',
    )
    analyze_desc: str | None = Field(
        default=None,
        description='当前 Unity 端采用的格式化魂印描述文本',
    )
    pve_effective: bool | None = Field(
        default=None,
        description='该魂印是否PVE生效，如果为null则表示无法通过数据层面推断其是否生效',
    )
    intensified: bool = Field(description='是否是强化的魂印')
    is_adv: bool = Field(description='是否是神谕觉醒魂印')

    @classmethod
    def resource_name(cls) -> str:
        return 'soulmark'


class Soulmark(SoulmarkBase, ConvertToORM['SoulmarkORM']):
    __name_fields__: ClassVar[list[str]] = ['effect_alias']

    pet: list[ResourceRef['Pet']] = Field(description='可持有该魂印的精灵ID')
    effect: EidEffectInUse | None = Field(description='魂印效果')
    effect_alias: str | None = Field(
        default=None, description='效果别名，命名规则为：alias_[效果ID]_[参数1]_[参数2]_…'
    )
    tag: list[ResourceRef['SoulmarkTagCategory']] = Field(
        description='魂印标签，例如强攻，断回合等'
    )
    intensified_to: ResourceRef['Soulmark'] | None = Field(
        description='强化后的魂印资源，该字段仅在该魂印有强化版时有效，否则为null'
    )
    from_: ResourceRef['Soulmark'] | None = Field(
        description='强化前的魂印资源，该字段仅在该魂印是强化/觉醒魂印时有效',
        schema_extra={
            'serialization_alias': 'from',
            'validation_alias': AliasChoices('from', 'from_'),
        },
    )
    advance: ResourceRef['PetAdvance'] | None = Field(
        default=None,
        description='觉醒后的魂印资源，该字段仅在该魂印是神谕觉醒魂印时有效',
    )

    @classmethod
    def get_orm_model(cls) -> type['SoulmarkORM']:
        return SoulmarkORM

    def to_orm(self) -> 'SoulmarkORM':
        return SoulmarkORM(
            id=self.id,
            desc=self.desc,
            intensified=self.intensified,
            is_adv=self.is_adv,
            effect_in_use=self.effect.to_orm() if self.effect else None,
            intensified_to_id=self.intensified_to.id if self.intensified_to else None,
            desc_formatting_adjustment=self.desc_formatting_adjustment,
            pve_effective=self.pve_effective,
            analyze_desc=self.analyze_desc,
        )


class SoulmarkORM(SoulmarkBase, table=True):
    pet: list['PetORM'] = Relationship(
        back_populates='soulmark', link_model=PetSoulmarkLink
    )
    tag: list['SoulmarkTagORM'] = Relationship(
        back_populates='soulmark', link_model=SoulmarkTagLink
    )
    effect_in_use_id: int | None = Field(
        default=None, foreign_key='eid_effect_in_use.id'
    )
    effect_in_use: EidEffectInUseORM | None = Relationship(
        back_populates='soulmark',
    )

    from_: Optional['SoulmarkORM'] = Relationship(
        back_populates='intensified_to',
        sa_relationship_kwargs={
            # "foreign_keys": "[SoulmarkORM.from_id]",
            # "primaryjoin": "SoulmarkORM.from_id == SoulmarkORM.id",
            # "remote_side": "SoulmarkORM.id",
            'uselist': False,
        },
    )
    intensified_to_id: int | None = Field(default=None, foreign_key='soulmark.id')
    intensified_to: Optional['SoulmarkORM'] = Relationship(
        back_populates='from_',
        sa_relationship_kwargs={
            'foreign_keys': '[SoulmarkORM.intensified_to_id]',
            'primaryjoin': 'SoulmarkORM.intensified_to_id == SoulmarkORM.id',
            'remote_side': 'SoulmarkORM.id',
            'uselist': False,
        },
    )
    advance: Optional['PetAdvanceORM'] = Relationship(
        back_populates='soulmark',
        sa_relationship_kwargs={
            'uselist': False,
        },
    )


class SoulmarkTagBase(BaseCategoryModel):
    name: str = Field(description='魂印标签名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'soulmark_tag'


class SoulmarkTagCategory(SoulmarkTagBase, ConvertToORM['SoulmarkTagORM']):
    soulmark: list[ResourceRef] = Field(default_factory=list, description='魂印列表')

    @classmethod
    def get_orm_model(cls) -> type['SoulmarkTagORM']:
        return SoulmarkTagORM

    def to_orm(self) -> 'SoulmarkTagORM':
        return SoulmarkTagORM(
            id=self.id,
            name=self.name,
        )


class SoulmarkTagORM(SoulmarkTagBase, table=True):
    soulmark: list['SoulmarkORM'] = Relationship(
        back_populates='tag', link_model=SoulmarkTagLink
    )
