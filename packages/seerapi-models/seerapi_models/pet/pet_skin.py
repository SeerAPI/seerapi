from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from seerapi_models.build_model import BaseResModel, ConvertToORM
from seerapi_models.common import ResourceRef

if TYPE_CHECKING:
    from . import Pet, PetORM


class PetSkinSeriesBase(BaseResModel):
    id: int = Field(primary_key=True, description='系列ID')
    name: str = Field(description='系列名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_skin_series'


class PetSkinSeriesSubTypeBase(BaseResModel):
    id: int = Field(
        primary_key=True,
        description='子类型ID，该值是由 SeerAPI 计算得出的，公式为（系列ID * 1000 + 子类型ID）',
    )
    name: str = Field(description='子类型名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_skin_series_sub_type'


class PetSkinSeriesSubType(
    PetSkinSeriesSubTypeBase, ConvertToORM['PetSkinSeriesSubTypeORM']
):
    series: ResourceRef['PetSkinSeries'] = Field(description='所属系列')
    skins: list[ResourceRef['PetSkin']] = Field(
        default_factory=list, description='该子类型对应的皮肤列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['PetSkinSeriesSubTypeORM']:
        return PetSkinSeriesSubTypeORM

    def to_orm(self) -> 'PetSkinSeriesSubTypeORM':
        return PetSkinSeriesSubTypeORM(
            id=self.id,
            name=self.name,
            series_id=self.series.id,
        )


class PetSkinSeriesSubTypeORM(PetSkinSeriesSubTypeBase, table=True):
    series_id: int = Field(foreign_key='pet_skin_series.id')
    series: 'PetSkinSeriesORM' = Relationship(back_populates='sub_types')
    skins: list['PetSkinORM'] = Relationship(back_populates='sub_type')


class PetSkinSeries(PetSkinSeriesBase, ConvertToORM['PetSkinSeriesORM']):
    skins: list[ResourceRef['PetSkin']] = Field(
        default_factory=list, description='该系列的皮肤列表'
    )
    sub_types: list[ResourceRef['PetSkinSeriesSubType']] = Field(
        default_factory=list, description='该系列的子类型列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['PetSkinSeriesORM']:
        return PetSkinSeriesORM

    def to_orm(self) -> 'PetSkinSeriesORM':
        return PetSkinSeriesORM(id=self.id, name=self.name)


class PetSkinSeriesORM(PetSkinSeriesBase, table=True):
    skins: list['PetSkinORM'] = Relationship(back_populates='series')
    sub_types: list['PetSkinSeriesSubTypeORM'] = Relationship(
        back_populates='series',
    )


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
    card_price: int | None = Field(
        default=None, description='皮肤礼卡价格，当皮肤未上架礼卡商店时为null'
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_skin'


class PetSkin(PetSkinBase, ConvertToORM['PetSkinORM']):
    pet: ResourceRef['Pet'] = Field(description='使用该皮肤的精灵')
    category: ResourceRef['PetSkinCategory'] = Field(
        description='该皮肤所属的稀有度类型'
    )
    series: ResourceRef['PetSkinSeries'] | None = Field(
        default=None,
        description='该皮肤所属的图鉴收集系列（在Unity端图鉴面板中显示），为null时表示该皮肤不属于任何图鉴收集系列',
    )
    sub_type: ResourceRef['PetSkinSeriesSubType'] | None = Field(
        default=None,
        description='该皮肤所属的系列子类型，为null时表示该皮肤直接归属主系列',
    )

    @classmethod
    def get_orm_model(cls) -> type['PetSkinORM']:
        return PetSkinORM

    def to_orm(self) -> 'PetSkinORM':
        return PetSkinORM(
            id=self.id,
            name=self.name,
            resource_id=self.resource_id,
            card_price=self.card_price,
            pet_id=self.pet.id,
            category_id=self.category.id,
            series_id=self.series.id if self.series else None,
            sub_type_id=self.sub_type.id if self.sub_type else None,
        )


class PetSkinORM(PetSkinBase, table=True):
    pet_id: int = Field(foreign_key='pet.id')
    pet: 'PetORM' = Relationship(back_populates='skins')
    category_id: int = Field(foreign_key='pet_skin_category.id')
    category: 'PetSkinCategoryORM' = Relationship(back_populates='skins')
    series_id: int | None = Field(default=None, foreign_key='pet_skin_series.id')
    series: Optional['PetSkinSeriesORM'] = Relationship(back_populates='skins')
    sub_type_id: int | None = Field(
        default=None, foreign_key='pet_skin_series_sub_type.id'
    )
    sub_type: Optional['PetSkinSeriesSubTypeORM'] = Relationship(back_populates='skins')


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
