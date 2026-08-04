from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from seerapi_models.build_model import BaseResModel, ConvertToORM
from seerapi_models.common import ResourceRef

if TYPE_CHECKING:
    from .element_type import AutocardElementType, AutocardElementTypeORM


class BaseAutocardRole(BaseResModel):
    name: str = Field(description='角色名称')
    description: str = Field(description='角色描述')
    health: int = Field(description='角色初始生命值')
    skill_desc: str = Field(description='角色技能描述')
    is_passive_skill: bool = Field(description='角色技能是否为被动技能')
    skill_cost: int | None = Field(
        default=None,
        description='使用技能消耗的金币数量，None表示该技能为被动技能，此字段无效',
    )
    skill_game_limit: int | None = Field(
        default=None,
        description='技能在游戏中的使用次数限制，0表示无限制，None表示该技能为被动技能，此字段无效',
    )
    skill_round_limit: int | None = Field(
        default=None,
        description='技能在回合中的使用次数限制，0表示无限制，None表示该技能为被动技能，此字段无效',
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'autocard_role'


class AutocardRole(BaseAutocardRole, ConvertToORM['AutocardRoleORM']):
    element_type: ResourceRef['AutocardElementType'] = Field(description='角色元素类型')

    @classmethod
    def get_orm_model(cls) -> 'type[AutocardRoleORM]':
        return AutocardRoleORM

    def to_orm(self) -> 'AutocardRoleORM':
        return AutocardRoleORM(
            id=self.id,
            name=self.name,
            description=self.description,
            health=self.health,
            skill_desc=self.skill_desc,
            skill_cost=self.skill_cost,
            is_passive_skill=self.is_passive_skill,
            skill_game_limit=self.skill_game_limit,
            skill_round_limit=self.skill_round_limit,
            element_type_id=self.element_type.id,
        )


class AutocardRoleORM(BaseAutocardRole, table=True):
    element_type: 'AutocardElementTypeORM' = Relationship(back_populates='role')
    element_type_id: int = Field(foreign_key='autocard_element_type.id')
