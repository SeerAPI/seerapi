from sqlmodel import Field, Relationship, SQLModel

from seerapi_models.build_model import (
    BaseResModel,
    BaseResModelWithOptionalId,
    ConvertToORM,
)


class Buff(SQLModel):
    name: str = Field(description='Buff名称')
    description: str = Field(description='Buff描述')
    open_turn: int = Field(
        description='该Buff可被选择的最早回合（即从第几回合起可开放选择）'
    )


class BaseAutocardField(BaseResModel):
    """群星牌圣域Buff"""

    name: str = Field(description='圣域名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'autocard_field'


class AutocardField(BaseAutocardField, ConvertToORM['AutocardFieldORM']):
    buff_stage: dict[int, list[Buff]] = Field(
        description='Buff阶段，包含每个阶段的所有可选项'
    )

    @classmethod
    def get_orm_model(cls) -> type['AutocardFieldORM']:
        return AutocardFieldORM

    def to_orm(self) -> 'AutocardFieldORM':
        return AutocardFieldORM(
            id=self.id,
            name=self.name,
            buffs=[
                AutocardFieldBuffORM(
                    field_id=self.id,
                    stage=stage,
                    name=buff.name,
                    description=buff.description,
                    open_turn=buff.open_turn,
                )
                for stage, buffs in self.buff_stage.items()
                for buff in buffs
            ],
        )


class AutocardFieldORM(BaseAutocardField, table=True):
    buffs: list['AutocardFieldBuffORM'] = Relationship(back_populates='field')


class AutocardFieldBuffORM(BaseResModelWithOptionalId, Buff, table=True):
    stage: int = Field(description='Buff所属的阶段')
    field_id: int = Field(description='圣域ID', foreign_key='autocard_field.id')
    field: 'AutocardFieldORM' = Relationship(back_populates='buffs')

    @classmethod
    def resource_name(cls) -> str:
        return 'autocard_field_buff'
