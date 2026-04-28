from sqlmodel import Field, Relationship, SQLModel

from seerapi_models.build_model import BaseCategoryModel, BaseResModel, ConvertToORM
from seerapi_models.common import ResourceRef


class BattleEffectCategoryLink(SQLModel, table=True):
    battle_effect_id: int | None = Field(
        default=None, foreign_key='battle_effect.id', primary_key=True
    )
    type_id: int | None = Field(
        default=None, foreign_key='battle_effect_type.id', primary_key=True
    )


class BattleEffectBase(BaseResModel):
    name: str = Field(description='状态名称')
    desc: str = Field(description='状态描述')

    @classmethod
    def resource_name(cls) -> str:
        return 'battle_effect'


class BattleEffect(BattleEffectBase, ConvertToORM['BattleEffectORM']):
    type: list[ResourceRef['BattleEffectCategory']] = Field(
        default_factory=list,
        description='状态类型，可能同时属于多个类型，例如瘫痪同时属于控制类和限制类异常',
    )

    @classmethod
    def get_orm_model(cls) -> 'type[BattleEffectORM]':
        return BattleEffectORM

    def to_orm(self) -> 'BattleEffectORM':
        return BattleEffectORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
        )


class BattleEffectORM(BattleEffectBase, table=True):
    type: list['BattleEffectCategoryORM'] = Relationship(
        back_populates='effect', link_model=BattleEffectCategoryLink
    )


class BattleEffectCategoryBase(BaseCategoryModel):
    name: str = Field(description='状态类型名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'battle_effect_type'


class BattleEffectCategory(
    BattleEffectCategoryBase, ConvertToORM['BattleEffectCategoryORM']
):
    effect: list[ResourceRef['BattleEffect']] = Field(
        default_factory=list, description='异常状态列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['BattleEffectCategoryORM']:
        return BattleEffectCategoryORM

    def to_orm(self) -> 'BattleEffectCategoryORM':
        return BattleEffectCategoryORM(
            id=self.id,
            name=self.name,
        )


class BattleEffectCategoryORM(BattleEffectCategoryBase, table=True):
    effect: list['BattleEffectORM'] = Relationship(
        back_populates='type', link_model=BattleEffectCategoryLink
    )
