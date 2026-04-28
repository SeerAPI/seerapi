from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from seerapi_models.build_model import (
    BaseCategoryModel,
    BaseResModel,
    ConvertToORM,
)
from seerapi_models.common import ResourceRef

if TYPE_CHECKING:
    from .pet import Pet, PetORM


class PetEncyclopediaEntryBase(BaseResModel):
    id: int = Field(primary_key=True, description='精灵图鉴ID', foreign_key='pet.id')
    name: str = Field(description='精灵名称')
    has_sound: bool = Field(description='精灵是否存在叫声')
    height: float | None = Field(
        default=None,
        description="精灵身高，当这个值在图鉴中为'未知'时，这个值为null",
    )
    weight: float | None = Field(
        default=None,
        description="精灵重量，当这个值在图鉴中为'未知'时，这个值为null",
    )
    foundin: str | None = Field(default=None, description='精灵发现地点')
    food: str | None = Field(default=None, description='精灵喜爱的食物')
    introduction: str = Field(description='精灵介绍')

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_encyclopedia_entry'


class PetEncyclopediaEntry(
    PetEncyclopediaEntryBase, ConvertToORM['PetEncyclopediaEntryORM']
):
    pet: ResourceRef['Pet'] = Field(description='精灵')

    @classmethod
    def get_orm_model(cls) -> type['PetEncyclopediaEntryORM']:
        return PetEncyclopediaEntryORM

    def to_orm(self) -> 'PetEncyclopediaEntryORM':
        return PetEncyclopediaEntryORM(
            id=self.id,
            name=self.name,
            has_sound=self.has_sound,
            height=self.height,
            weight=self.weight,
            foundin=self.foundin,
            food=self.food,
            introduction=self.introduction,
        )


class PetEncyclopediaEntryORM(PetEncyclopediaEntryBase, table=True):
    pet: 'PetORM' = Relationship(back_populates='encyclopedia')


class PetArchiveStoryEntryBase(BaseResModel):
    id: int = Field(primary_key=True, description='故事条目ID')
    content: str = Field(description='故事条目内容')

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_archive_story_entry'


class PetArchiveStoryEntry(
    PetArchiveStoryEntryBase, ConvertToORM['PetArchiveStoryEntryORM']
):
    pet: ResourceRef['Pet'] = Field(description='精灵')
    book: ResourceRef['PetArchiveStoryBook'] = Field(description='故事系列')

    @classmethod
    def get_orm_model(cls) -> type['PetArchiveStoryEntryORM']:
        return PetArchiveStoryEntryORM

    def to_orm(self) -> 'PetArchiveStoryEntryORM':
        return PetArchiveStoryEntryORM(
            id=self.id, content=self.content, pet_id=self.pet.id, book_id=self.book.id
        )


class PetArchiveStoryEntryORM(PetArchiveStoryEntryBase, table=True):
    pet_id: int = Field(description='精灵ID', foreign_key='pet.id')
    pet: 'PetORM' = Relationship(back_populates='archive_story')
    book_id: int = Field(
        foreign_key='pet_archive_story_book.id',
    )
    book: 'PetArchiveStoryBookORM' = Relationship(back_populates='entries')


class PetArchiveStoryBookBase(BaseCategoryModel):
    name: str = Field(description='故事名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_archive_story_book'


class PetArchiveStoryBook(
    PetArchiveStoryBookBase, ConvertToORM['PetArchiveStoryBookORM']
):
    entries: list[ResourceRef[PetArchiveStoryEntryBase]] = Field(
        default_factory=list, description='故事条目'
    )

    @classmethod
    def get_orm_model(cls) -> type['PetArchiveStoryBookORM']:
        return PetArchiveStoryBookORM

    def to_orm(self) -> 'PetArchiveStoryBookORM':
        return PetArchiveStoryBookORM(
            id=self.id,
            name=self.name,
        )


class PetArchiveStoryBookORM(PetArchiveStoryBookBase, table=True):
    entries: list[PetArchiveStoryEntryORM] = Relationship(back_populates='book')
