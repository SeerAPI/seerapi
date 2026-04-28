from typing import Optional, cast

from sqlmodel import Field, Relationship, SQLModel

from seerapi_models.build_model import BaseCategoryModel, BaseResModel, ConvertToORM
from seerapi_models.common import ResourceRef, SkillEffectInUse, SkillEffectInUseORM
from seerapi_models.items import Item, ItemORM


class GemEffectLink(SQLModel, table=True):
    gem_id: int | None = Field(default=None, foreign_key='gem.id', primary_key=True)
    skill_effect_in_use_id: int | None = Field(
        default=None, foreign_key='skill_effect_in_use.id', primary_key=True
    )


class GemBase(BaseResModel):
    id: int = Field(primary_key=True, foreign_key='item.id', description='宝石ID')
    name: str = Field(description='宝石名称')
    level: int = Field(description='宝石等级')
    generation_id: int = Field(
        description='宝石世代', foreign_key='gem_generation_category.id'
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'gem'


class GemResRefs(SQLModel):
    prev_level_gem: ResourceRef['Gem'] | None = Field(
        default=None,
        description='该宝石的上一等级的引用，当为None时表示该宝石为最低等级',
    )
    next_level_gem: ResourceRef['Gem'] | None = Field(
        default=None,
        description='该宝石的下一等级的引用，当为None时表示该宝石为最高等级',
    )
    category: ResourceRef['GemCategory'] = Field(description='宝石类型引用')
    effect: list[SkillEffectInUse] = Field(description='宝石效果')
    item: ResourceRef['Item'] = Field(description='宝石物品资源引用')


class Gem(GemBase, GemResRefs, ConvertToORM['GemORM']):
    inlay_rate: float | None = Field(default=None, description='镶嵌成功率')
    equivalent_level1_count: int | None = Field(
        default=None, description='相当于多少个1级宝石'
    )
    fail_compensate_range: tuple[int, int] | None = Field(
        default=None, description='当镶嵌失败时返还的宝石的等级范围，仅在1代宝石中有效'
    )

    upgrade_cost: int | None = Field(
        default=None, description='升级到该等级需要的石之砂数量，仅在2代宝石中有效'
    )

    @classmethod
    def get_orm_model(cls) -> type['GemORM']:
        return GemORM

    def to_orm(self) -> 'GemORM':
        gen1_part = None
        gen2_part = None
        if self.generation_id == 1:
            fail_compensate_range = cast(tuple[int, int], self.fail_compensate_range)
            gen1_part = GemGen1PartORM(
                id=self.id,
                inlay_rate=cast(float, self.inlay_rate),
                equivalent_level1_count=cast(int, self.equivalent_level1_count),
                fail_compensate_level_start=fail_compensate_range[0],
                fail_compensate_level_end=fail_compensate_range[1],
            )
        elif self.generation_id == 2:
            gen2_part = GemGen2PartORM(
                id=self.id,
                upgrade_cost=cast(int, self.upgrade_cost),
            )
        return GemORM(
            id=self.id,
            name=self.name,
            level=self.level,
            generation_id=self.generation_id,
            gen1_part=gen1_part,
            gen2_part=gen2_part,
            next_level_gem_id=self.next_level_gem.id if self.next_level_gem else None,
            category_id=self.category.id,
            skill_effect_in_use=[effect.to_orm() for effect in self.effect],
        )

    def to_detailed(self) -> 'GemGen1 | GemGen2':
        general_args = {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'generation_id': self.generation_id,
            'category': self.category,
            'effect': self.effect,
            'prev_level_gem': self.prev_level_gem,
            'next_level_gem': self.next_level_gem,
            'item': self.item,
        }
        if self.generation_id == 1:
            return GemGen1(
                **general_args,
                inlay_rate=cast(float, self.inlay_rate),
                equivalent_level1_count=cast(int, self.equivalent_level1_count),
                fail_compensate_range=cast(tuple[int, int], self.fail_compensate_range),
            )
        else:
            return GemGen2(
                **general_args,
                upgrade_cost=cast(int, self.upgrade_cost),
            )


class GemGen1(GemBase, GemResRefs):
    inlay_rate: float = Field(description='镶嵌成功率')
    equivalent_level1_count: int = Field(description='相当于多少个1级宝石')
    fail_compensate_range: tuple[int, int] = Field(
        description='当镶嵌失败时返还的宝石的等级范围'
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'gem_gen1'


class GemGen2(GemBase, GemResRefs):
    upgrade_cost: int = Field(description='升级到该等级需要的石之砂数量')

    @classmethod
    def resource_name(cls) -> str:
        return 'gem_gen2'


class GemORM(GemBase, table=True):
    prev_level_gem: Optional['GemORM'] = Relationship(
        back_populates='next_level_gem',
        sa_relationship_kwargs={
            'uselist': False,
        },
    )
    next_level_gem_id: int | None = Field(default=None, foreign_key='gem.id')
    next_level_gem: Optional['GemORM'] = Relationship(
        back_populates='prev_level_gem',
        sa_relationship_kwargs={
            'primaryjoin': 'GemORM.next_level_gem_id == GemORM.id',
            'remote_side': 'GemORM.id',
            'uselist': False,
        },
    )
    category_id: int = Field(foreign_key='gem_category.id')
    generation: 'GemGenCategoryORM' = Relationship(
        back_populates='gem',
    )
    category: Optional['GemCategoryORM'] = Relationship(
        back_populates='gem',
        sa_relationship_kwargs={
            'primaryjoin': 'GemORM.category_id == GemCategoryORM.id',
        },
    )
    skill_effect_in_use_id: int | None = Field(
        default=None, foreign_key='skill_effect_in_use.id'
    )
    skill_effect_in_use: list['SkillEffectInUseORM'] = Relationship(
        back_populates='gem',
        link_model=GemEffectLink,
    )

    gen1_part: Optional['GemGen1PartORM'] = Relationship(
        back_populates='gem',
        sa_relationship_kwargs={
            'primaryjoin': 'GemORM.id == GemGen1PartORM.id',
        },
    )
    gen2_part: Optional['GemGen2PartORM'] = Relationship(
        back_populates='gem',
        sa_relationship_kwargs={
            'primaryjoin': 'GemORM.id == GemGen2PartORM.id',
        },
    )

    item: 'ItemORM' = Relationship(back_populates='gem')


class GemGen1PartORM(BaseResModel, table=True):
    id: int = Field(primary_key=True, foreign_key='gem.id')
    inlay_rate: float = Field(description='镶嵌成功率')
    equivalent_level1_count: int = Field(description='相当于多少个1级宝石')

    fail_compensate_level_start: int = Field(
        description='当镶嵌失败时返还的宝石的等级范围'
    )
    fail_compensate_level_end: int = Field(
        description='当镶嵌失败时返还的宝石的等级范围'
    )

    gem: 'GemORM' = Relationship(
        back_populates='gen1_part',
        sa_relationship_kwargs={
            'primaryjoin': 'GemORM.id == GemGen1PartORM.id',
        },
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'gem_gen1_part'


class GemGen2PartORM(BaseResModel, table=True):
    id: int = Field(primary_key=True, foreign_key='gem.id')
    upgrade_cost: int = Field(description='升级到该等级需要的石之砂数量')

    gem: 'GemORM' = Relationship(
        back_populates='gen2_part',
        sa_relationship_kwargs={
            'primaryjoin': 'GemORM.id == GemGen2PartORM.id',
        },
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'gem_gen2_part'


class GemCategoryBase(BaseCategoryModel):
    name: str = Field(description='名称')
    generation_id: int = Field(
        description='宝石世代', foreign_key='gem_generation_category.id'
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'gem_category'


class GemCategory(GemCategoryBase, ConvertToORM['GemCategoryORM']):
    gem: list[ResourceRef] = Field(default_factory=list, description='宝石列表')

    @classmethod
    def get_orm_model(cls) -> type['GemCategoryORM']:
        return GemCategoryORM

    def to_orm(self) -> 'GemCategoryORM':
        return GemCategoryORM(
            id=self.id,
            name=self.name,
            generation_id=self.generation_id,
        )


class GemCategoryORM(GemCategoryBase, table=True):
    gem: list['GemORM'] = Relationship(
        back_populates='category',
    )
    generation: list['GemGenCategoryORM'] = Relationship(
        back_populates='category',
    )


class GemGenCategoryBase(BaseCategoryModel):
    @classmethod
    def resource_name(cls) -> str:
        return 'gem_generation_category'


class GemGenCategory(GemGenCategoryBase, ConvertToORM['GemGenCategoryORM']):
    gem_category: list[ResourceRef] = Field(
        default_factory=list, description='宝石类别列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['GemGenCategoryORM']:
        return GemGenCategoryORM

    def to_orm(self) -> 'GemGenCategoryORM':
        return GemGenCategoryORM(
            id=self.id,
        )


class GemGenCategoryORM(GemGenCategoryBase, table=True):
    gem: list['GemORM'] = Relationship(
        back_populates='generation',
        sa_relationship_kwargs={
            'primaryjoin': 'GemORM.generation_id == GemGenCategoryORM.id',
        },
    )
    category: 'GemCategoryORM' = Relationship(
        back_populates='generation',
    )
