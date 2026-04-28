from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from seerapi_models.build_model import BaseResModel, ConvertToORM
from seerapi_models.common import ResourceRef

if TYPE_CHECKING:
    from . import Pet, PetORM


class PetSkinBase(BaseResModel):
    id: int = Field(
        primary_key=True, description='皮肤ID，注意该字段不是头像/立绘等所使用的资源ID'
    )
    name: str = Field(description='皮肤名称')
    resource_id: int = Field(description='皮肤资源ID')
    enemy_resource_id: int | None = Field(
        default=None,
        description='该皮肤在对手侧时使用的资源的ID，仅少数皮肤存在这种资源',
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_skin'


class PetSkin(PetSkinBase, ConvertToORM['PetSkinORM']):
    pet: ResourceRef['Pet'] = Field(description='使用该皮肤的精灵')
    category: ResourceRef['PetSkinCategory'] = Field(description='该皮肤所属的系列')

    @classmethod
    def get_orm_model(cls) -> type['PetSkinORM']:
        return PetSkinORM

    def to_orm(self) -> 'PetSkinORM':
        return PetSkinORM(
            id=self.id,
            name=self.name,
            resource_id=self.resource_id,
            pet_id=self.pet.id,
            category_id=self.category.id,
        )


class PetSkinORM(PetSkinBase, table=True):
    pet_id: int = Field(foreign_key='pet.id')
    pet: 'PetORM' = Relationship(back_populates='skins')
    category_id: int = Field(foreign_key='pet_skin_category.id')
    category: 'PetSkinCategoryORM' = Relationship(back_populates='skins')


class PetSkinCategoryBase(BaseResModel):
    id: int = Field(primary_key=True, description='系列ID')
    # name: str = Field(
    # 	description='系列名称'
    # ) TODO: 该字段可能在数据中不存在，暂时忽略，等待游戏内数据或打补丁补充

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_skin_category'


class PetSkinCategory(PetSkinCategoryBase, ConvertToORM['PetSkinCategoryORM']):
    skins: list[ResourceRef['PetSkin']] = Field(
        default_factory=list, description='该系列的皮肤列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['PetSkinCategoryORM']:
        return PetSkinCategoryORM

    def to_orm(self) -> 'PetSkinCategoryORM':
        return PetSkinCategoryORM(id=self.id)


class PetSkinCategoryORM(PetSkinCategoryBase, table=True):
    skins: list['PetSkinORM'] = Relationship(back_populates='category')
