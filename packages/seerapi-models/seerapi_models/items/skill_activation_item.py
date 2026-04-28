from sqlmodel import Field, Relationship

from seerapi_models.build_model import BaseResModel, ConvertToORM
from seerapi_models.common import ResourceRef
from seerapi_models.pet import Pet, SkillInPetORM
from seerapi_models.skill import Skill

from ._common import Item, ItemORM


class SkillActivationItemBase(BaseResModel):
    id: int = Field(
        primary_key=True, foreign_key='item.id', description='技能激活道具ID'
    )
    name: str = Field(description='技能激活道具名称')
    item_number: int = Field(description='激活技能需要的该道具数量')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_activation_item'


class SkillActivationItem(
    SkillActivationItemBase, ConvertToORM['SkillActivationItemORM']
):
    item: ResourceRef['Item'] = Field(description='道具资源引用')
    skill: ResourceRef['Skill'] = Field(description='使用该道具激活的技能')
    pet: ResourceRef['Pet'] = Field(description='使用该道具的精灵')

    @classmethod
    def get_orm_model(cls) -> type['SkillActivationItemORM']:
        return SkillActivationItemORM

    def to_orm(self) -> 'SkillActivationItemORM':
        return SkillActivationItemORM(
            id=self.id,
            name=self.name,
            item_number=self.item_number,
        )


class SkillActivationItemORM(SkillActivationItemBase, table=True):
    item: 'ItemORM' = Relationship(back_populates='skill_activation_item')
    skill_in_pet: 'SkillInPetORM' = Relationship(back_populates='skill_activation_item')
