from sqlmodel import Field, Relationship

from seerapi_models.build_model import BaseResModel, ConvertToORM
from seerapi_models.common import SixAttributes, SixAttributesORMBase


class NatureAttrORM(SixAttributesORMBase, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
        foreign_key='nature.id',
        description='性格修正属性ID',
    )
    nature: 'NatureORM' = Relationship(back_populates='attributes')

    @classmethod
    def resource_name(cls) -> str:
        return 'nature_attr'


class BaseNature(BaseResModel):
    name: str = Field(description='性格名称')
    des: str = Field(description='性格描述')
    des2: str = Field(description='性格描述2')

    @classmethod
    def resource_name(cls) -> str:
        return 'nature'


class Nature(BaseNature, ConvertToORM['NatureORM']):
    """精灵性格修正模型"""

    attributes: SixAttributes = Field(description='性格修正属性')

    @classmethod
    def get_orm_model(cls) -> type['NatureORM']:
        return NatureORM

    def to_orm(self) -> 'NatureORM':
        return NatureORM(
            id=self.id,
            name=self.name,
            des=self.des,
            des2=self.des2,
            attributes=NatureAttrORM(
                **self.attributes.model_dump(),
            ),
        )


class NatureORM(BaseNature, table=True):
    attributes: NatureAttrORM = Relationship(back_populates='nature')
