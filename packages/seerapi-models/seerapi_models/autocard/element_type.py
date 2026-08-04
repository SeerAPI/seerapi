from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from seerapi_models.build_model import BaseCategoryModel, ConvertToORM
from seerapi_models.common import ResourceRef

if TYPE_CHECKING:
    from .card import Autocard, AutocardORM
    from .role import AutocardRole, AutocardRoleORM


class BaseAutocardElementType(BaseCategoryModel):
    name: str = Field(description='类型名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'autocard_element_type'


class AutocardElementType(
    BaseAutocardElementType, ConvertToORM['AutocardElementTypeORM']
):
    autocard: list[ResourceRef['Autocard']] = Field(description='卡牌列表')
    role: list[ResourceRef['AutocardRole']] = Field(description='角色列表')

    @classmethod
    def get_orm_model(cls) -> 'type[AutocardElementTypeORM]':
        return AutocardElementTypeORM

    def to_orm(self) -> 'AutocardElementTypeORM':
        return AutocardElementTypeORM(
            id=self.id,
            name=self.name,
        )


class AutocardElementTypeORM(BaseAutocardElementType, table=True):
    autocard: list['AutocardORM'] = Relationship(back_populates='element_type')
    role: list['AutocardRoleORM'] = Relationship(back_populates='element_type')
