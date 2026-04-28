from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from seerapi_models.build_model import BaseCategoryModel, BaseResModel, ConvertToORM
from seerapi_models.common import ResourceRef

if TYPE_CHECKING:
    from .enegry_bead import EnergyBeadORM
    from .equip import EquipORM
    from .mintmark_gem import GemORM
    from .skill_activation_item import SkillActivationItemORM
    from .skill_stone import SkillStoneORM


class ItemBase(BaseResModel):
    name: str = Field(description='物品名称')
    desc: str | None = Field(
        default=None, description='物品描述，可能为空（在游戏内显示为默认描述）'
    )
    max: int = Field(description='物品最大数量')

    @classmethod
    def resource_name(cls) -> str:
        return 'item'


class Item(ItemBase, ConvertToORM['ItemORM']):
    category: ResourceRef['ItemCategory'] = Field(description='物品分类')

    @classmethod
    def get_orm_model(cls) -> type['ItemORM']:
        return ItemORM

    def to_orm(self) -> 'ItemORM':
        return ItemORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
            max=self.max,
            category_id=self.category.id,
        )


class ItemORM(ItemBase, table=True):
    skill_stone: Optional['SkillStoneORM'] = Relationship(
        back_populates='item',
    )
    energy_bead: Optional['EnergyBeadORM'] = Relationship(
        back_populates='item',
    )
    skill_activation_item: Optional['SkillActivationItemORM'] = Relationship(
        back_populates='item',
    )
    equip: Optional['EquipORM'] = Relationship(
        back_populates='item',
    )
    gem: Optional['GemORM'] = Relationship(
        back_populates='item',
    )

    category_id: int = Field(foreign_key='item_category.id')
    category: 'ItemCategoryORM' = Relationship(
        back_populates='item',
    )


class ItemCategoryBase(BaseCategoryModel):
    name: str = Field(description='物品分类名称')
    max: int = Field(description='物品最大数量')

    @classmethod
    def resource_name(cls) -> str:
        return 'item_category'


class ItemCategory(ItemCategoryBase, ConvertToORM['ItemCategoryORM']):
    item: list[ResourceRef['Item']] = Field(
        default_factory=list, description='该分类下的所有物品'
    )

    @classmethod
    def get_orm_model(cls) -> type['ItemCategoryORM']:
        return ItemCategoryORM

    def to_orm(self) -> 'ItemCategoryORM':
        return ItemCategoryORM(
            id=self.id,
            name=self.name,
            max=self.max,
        )


class ItemCategoryORM(ItemCategoryBase, table=True):
    item: list['ItemORM'] = Relationship(back_populates='category')
