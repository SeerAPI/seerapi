from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from seerapi_models.build_model import (
    BaseCategoryModel,
    BaseResModel,
    ConvertToORM,
)
from seerapi_models.common import ResourceRef

from .element_type import AutocardElementType, AutocardElementTypeORM


def card_is_spell(type_id: int) -> bool:
    return type_id in (2, 4)


class AutocardBase(BaseResModel):
    name: str = Field(description='卡牌名称')
    description: str = Field(description='卡牌描述')
    level: int = Field(description='卡牌等级')
    cost: int = Field(description='卡牌费用')
    is_token: bool = Field(description='该卡牌是否是衍生卡')

    @classmethod
    def resource_name(cls) -> str:
        return 'autocard'


class AutocardResRefs(SQLModel):
    type: ResourceRef['AutocardCardType'] = Field(description='卡牌类型')
    element_type: ResourceRef['AutocardElementType'] = Field(description='卡牌元素属性')


class PetAutocard(AutocardBase, AutocardResRefs):
    attack: int = Field(description='卡牌攻击力')
    health: int = Field(description='卡牌生命值')
    is_awakened: bool = Field(description='该卡牌是否是觉醒后的卡牌')
    awaken_card: ResourceRef['Autocard'] | None = Field(
        default=None, description='该卡牌的觉醒版本，当卡牌不能觉醒时为null'
    )
    non_awaken_card: ResourceRef['Autocard'] | None = Field(
        default=None,
        description='该卡牌的非觉醒版本，仅当该卡牌为觉醒后的精灵卡时有效',
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'autocard_petcard'


class SpellAutocard(AutocardBase, AutocardResRefs):
    @classmethod
    def resource_name(cls) -> str:
        return 'autocard_spellcard'


class Autocard(AutocardBase, AutocardResRefs, ConvertToORM['AutocardORM']):
    attack: int | None = Field(
        default=None, description='卡牌攻击力，仅当该卡牌为精灵卡时有效'
    )
    health: int | None = Field(
        default=None, description='卡牌生命值，仅当该卡牌为精灵卡时有效'
    )
    is_awakened: bool = Field(
        default=None, description='该卡牌是否是觉醒后的卡牌，仅当该卡牌为精灵卡时有效'
    )
    awaken_card: ResourceRef['Autocard'] | None = Field(
        default=None, description='该卡牌的觉醒版本，仅当该卡牌为精灵卡时有效'
    )
    non_awaken_card: ResourceRef['Autocard'] | None = Field(
        default=None,
        description='该卡牌的非觉醒版本，仅当该卡牌为觉醒后的精灵卡时有效',
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'autocard'

    @classmethod
    def get_orm_model(cls) -> 'type[AutocardORM]':
        return AutocardORM

    def to_orm(self) -> 'AutocardORM':
        return AutocardORM(
            id=self.id,
            attack=self.attack,
            health=self.health,
            is_awakened=self.is_awakened,
            name=self.name,
            description=self.description,
            level=self.level,
            cost=self.cost,
            awaken_card_id=self.awaken_card.id
            if self.awaken_card and not card_is_spell(self.type.id)
            else None,
            type_id=self.type.id,
            element_type_id=self.element_type.id,
            is_token=self.is_token,
        )

    def to_detailed(self) -> 'PetAutocard | SpellAutocard':
        general_args = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'level': self.level,
            'cost': self.cost,
            'type': self.type,
            'element_type': self.element_type,
            'is_token': self.is_token,
        }
        if card_is_spell(self.type.id):
            return SpellAutocard(**general_args)

        assert self.attack is not None
        assert self.health is not None
        assert self.is_awakened is not None
        return PetAutocard(
            **general_args,
            attack=self.attack,
            health=self.health,
            is_awakened=self.is_awakened,
            awaken_card=self.awaken_card,
            non_awaken_card=self.non_awaken_card,
        )


class AutocardORM(AutocardBase, table=True):
    attack: int | None = Field(
        default=None, description='卡牌攻击力，仅当该卡牌为精灵卡时有效'
    )
    health: int | None = Field(
        default=None, description='卡牌生命值，仅当该卡牌为精灵卡时有效'
    )
    is_awakened: bool = Field(
        description='该卡牌是否是觉醒后的卡牌，仅当该卡牌为精灵卡时有效'
    )
    type_id: int = Field(foreign_key='autocard_cardtype.id')
    type: 'AutocardCardTypeORM' = Relationship(back_populates='autocard')
    element_type_id: int = Field(foreign_key='autocard_element_type.id')
    element_type: 'AutocardElementTypeORM' = Relationship(back_populates='autocard')
    awaken_card_id: int | None = Field(default=None, foreign_key='autocard.id')
    awaken_card: Optional['AutocardORM'] = Relationship(
        back_populates='non_awaken_card',
        sa_relationship_kwargs={
            'foreign_keys': '[AutocardORM.awaken_card_id]',
            'primaryjoin': 'AutocardORM.awaken_card_id == AutocardORM.id',
            'remote_side': 'AutocardORM.id',
            'uselist': False,
        },
    )
    non_awaken_card: Optional['AutocardORM'] = Relationship(
        back_populates='awaken_card',
        sa_relationship_kwargs={
            'uselist': False,
        },
    )


class BaseAutocardCardType(BaseCategoryModel):
    name: str = Field(description='类型名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'autocard_cardtype'


class AutocardCardType(BaseAutocardCardType, ConvertToORM['AutocardCardTypeORM']):
    autocard: list[ResourceRef['Autocard']] = Field(description='卡牌列表')

    @classmethod
    def get_orm_model(cls) -> 'type[AutocardCardTypeORM]':
        return AutocardCardTypeORM

    def to_orm(self) -> 'AutocardCardTypeORM':
        return AutocardCardTypeORM(
            id=self.id,
            name=self.name,
        )


class AutocardCardTypeORM(BaseAutocardCardType, table=True):
    autocard: list['AutocardORM'] = Relationship(back_populates='type')
