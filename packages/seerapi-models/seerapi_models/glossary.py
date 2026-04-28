from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from seerapi_models.build_model import BaseResModel, ConvertToORM
from seerapi_models.common import ResourceRef

if TYPE_CHECKING:
    from seerapi_models.pet import Pet, PetORM


class GlossaryEntryLink(SQLModel, table=True):
    """术语自引用链接表"""

    source_id: int | None = Field(
        default=None, foreign_key='glossary_entry.id', primary_key=True
    )
    target_id: int | None = Field(
        default=None, foreign_key='glossary_entry.id', primary_key=True
    )


class PetGlossaryEntryLink(SQLModel, table=True):
    pet_id: int | None = Field(default=None, foreign_key='pet.id', primary_key=True)
    glossary_entry_id: int | None = Field(
        default=None, foreign_key='glossary_entry.id', primary_key=True
    )


class GlossaryEntryBase(BaseResModel):
    id: int = Field(description='术语ID', primary_key=True)
    name: str = Field(description='术语名称')
    desc: str = Field(description='术语描述')
    kind: int = Field(
        description='术语类型，数值对应的类型尚不明确，这里暂时保留原始值'
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'glossary_entry'


class GlossaryEntry(GlossaryEntryBase, ConvertToORM['GlossaryEntryORM']):
    link: list[ResourceRef['GlossaryEntry']] | None = Field(
        default_factory=list,
        description='术语链接，用于指示显示该术语时应同时显示的其他术语',
    )
    pet: list[ResourceRef['Pet']] | None = Field(
        default=None, description='用于指示该术语是否是特定精灵专属的'
    )

    @classmethod
    def get_orm_model(cls) -> type['GlossaryEntryORM']:
        return GlossaryEntryORM

    def to_orm(self) -> 'GlossaryEntryORM':
        return GlossaryEntryORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
            kind=self.kind,
        )


class GlossaryEntryORM(GlossaryEntryBase, table=True):
    link: list['GlossaryEntryORM'] = Relationship(
        link_model=GlossaryEntryLink,
        sa_relationship_kwargs={
            'primaryjoin': 'GlossaryEntryORM.id == GlossaryEntryLink.source_id',
            'secondaryjoin': 'GlossaryEntryORM.id == GlossaryEntryLink.target_id',
        },
    )
    pet: list['PetORM'] = Relationship(
        back_populates='glossary_entry',
        link_model=PetGlossaryEntryLink,
    )
