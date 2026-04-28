from typing import TYPE_CHECKING, Optional, cast

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

from seerapi_models.build_model import (
    BaseCategoryModel,
    BaseResModel,
    ConvertToORM,
)
from seerapi_models.common import ResourceRef, SixAttributes, SixAttributesORMBase

if TYPE_CHECKING:
    from seerapi_models.element_type import TypeCombination, TypeCombinationORM
    from seerapi_models.glossary import GlossaryEntryORM
    from seerapi_models.items import (
        SkillActivationItem,
        SkillActivationItemORM,
        SuitBonusORM,
    )
    from seerapi_models.mintmark import MintmarkORM
    from seerapi_models.peak_pool import (
        PeakExpertPool,
        PeakExpertPoolORM,
        PeakPool,
        PeakPoolORM,
        PeakPoolVoteORM,
    )
    from seerapi_models.skill import Skill, SkillORM

    from . import (
        PetAdvance,
        PetAdvanceORM,
        PetArchiveStoryEntry,
        PetArchiveStoryEntryORM,
        PetEncyclopediaEntry,
        PetEncyclopediaEntryORM,
        PetSkinORM,
        Soulmark,
        SoulmarkORM,
    )


class BaseStatORM(SixAttributesORMBase, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
        foreign_key='pet.id',
    )
    pet: 'PetORM' = Relationship(
        back_populates='base_stats',
        sa_relationship_kwargs={
            'primaryjoin': 'BaseStatORM.id == PetORM.id',
        },
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_base_stats'


class YieldingEvORM(SixAttributesORMBase, table=True):
    id: int | None = Field(default=None, primary_key=True, foreign_key='pet.id')
    pet: 'PetORM' = Relationship(
        back_populates='yielding_ev',
        sa_relationship_kwargs={
            'primaryjoin': 'YieldingEvORM.id == PetORM.id',
        },
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_yielding_ev'


class DiyStatsRangeORM(BaseResModel, table=True):
    id: int = Field(default=None, primary_key=True, foreign_key='pet.id')
    pet: 'PetORM' = Relationship(
        back_populates='diy_stats',
        sa_relationship_kwargs={
            'primaryjoin': 'DiyStatsRangeORM.id == PetORM.id',
        },
    )
    atk_min: int = Field(description='精灵自定义种族值攻击最小值')
    def_min: int = Field(description='精灵自定义种族值防御最小值')
    sp_atk_min: int = Field(description='精灵自定义种族值特攻最小值')
    sp_def_min: int = Field(description='精灵自定义种族值特防最小值')
    spd_min: int = Field(description='精灵自定义种族值速度最小值')
    hp_min: int = Field(description='精灵自定义种族值体力最小值')
    atk_max: int = Field(description='精灵自定义种族值攻击最大值')
    def_max: int = Field(description='精灵自定义种族值防御最大值')
    sp_atk_max: int = Field(description='精灵自定义种族值特攻最大值')
    sp_def_max: int = Field(description='精灵自定义种族值特防最大值')
    spd_max: int = Field(description='精灵自定义种族值速度最大值')
    hp_max: int = Field(description='精灵自定义种族值体力最大值')

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_diy_stats_range'


class DiyStatsRange(BaseModel):
    min: SixAttributes = Field(description='精灵自定义种族值最小值')
    max: SixAttributes = Field(description='精灵自定义种族值最大值')

    def to_orm(self, pet_id: int) -> DiyStatsRangeORM:
        """将DiyStats转换为DiyStatsRangeORM"""
        return DiyStatsRangeORM(
            id=pet_id,
            atk_min=int(self.min.atk),
            def_min=int(self.min.def_),
            sp_atk_min=int(self.min.sp_atk),
            sp_def_min=int(self.min.sp_def),
            spd_min=int(self.min.spd),
            hp_min=int(self.min.hp),
            atk_max=int(self.max.atk),
            def_max=int(self.max.def_),
            sp_atk_max=int(self.max.sp_atk),
            sp_def_max=int(self.max.sp_def),
            spd_max=int(self.max.spd),
            hp_max=int(self.max.hp),
        )


class SkillInPetBase(SQLModel):
    learning_level: int | None = Field(
        default=None,
        description='技能的学习等级，当该技能无法通过升级获得时，该字段为null',
    )
    is_special: bool = Field(default=False, description='是否是特训技能')
    is_advanced: bool = Field(default=False, description='是否是神谕觉醒技能')
    is_fifth: bool = Field(default=False, description='是否是第五技能')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_in_pet'


class SkillInPet(SkillInPetBase):
    skill: ResourceRef['Skill'] = Field(description='技能资源')
    skill_activation_item: ResourceRef['SkillActivationItem'] | None = Field(
        default=None, description='学习该技能需要的激活道具'
    )


class SkillInPetORM(SkillInPetBase, table=True):
    skill_id: int = Field(primary_key=True, foreign_key='skill.id')
    skill: 'SkillORM' = Relationship(back_populates='pet_links')
    pet_id: int = Field(primary_key=True, foreign_key='pet.id')
    pet: 'PetORM' = Relationship(back_populates='skill_links')
    skill_activation_item_id: int | None = Field(
        default=None,
        foreign_key='skill_activation_item.id',
    )
    skill_activation_item: Optional['SkillActivationItemORM'] = Relationship(
        back_populates='skill_in_pet',
        sa_relationship_kwargs={
            'primaryjoin': 'SkillInPetORM.skill_activation_item_id == SkillActivationItemORM.id',
        },
    )


class PetBase(BaseResModel):
    name: str = Field(description='精灵名称')
    # 精灵基础信息
    yielding_exp: int = Field(description='击败精灵可获得的经验值')
    catch_rate: int = Field(description='精灵捕捉率')
    evolving_lv: int | None = Field(
        default=None, description='精灵进化等级，当精灵无法再通过等级进化时为null'
    )
    # 其他
    releaseable: bool = Field(description='精灵是否可放生')
    fusion_master: bool = Field(description='精灵是否可作为融合精灵的主宠')
    fusion_sub: bool = Field(description='精灵是否可作为融合精灵的副宠')
    has_resistance: bool = Field(description='精灵是否可获得抗性')

    resource_id: int = Field(description='精灵资源ID')
    enemy_resource_id: int | None = Field(
        default=None,
        description='该精灵在对手侧时使用的资源的ID，仅少数精灵存在这种资源',
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'pet'


class Pet(PetBase, ConvertToORM['PetORM']):
    type: ResourceRef['TypeCombination'] = Field(description='精灵属性')
    gender: ResourceRef['PetGenderCategory'] = Field(description='精灵性别')
    base_stats: SixAttributes = Field(description='精灵种族值')
    pet_class: ResourceRef['PetClass'] | None = Field(
        default=None, description='精灵类别，同一进化链中的精灵属于同一类'
    )
    evolution_chain_index: int = Field(description='该精灵在进化链中的位置，从0开始')
    yielding_ev: SixAttributes = Field(description='击败精灵可获得的学习力')
    vipbuff: ResourceRef['PetVipBuffCategory'] | None = Field(
        default=None, description='精灵VIP加成，仅在闪光/暗黑精灵上使用'
    )
    mount_type: ResourceRef['PetMountTypeCategory'] | None = Field(
        default=None, description='精灵骑乘类型，仅在坐骑精灵上使用'
    )
    diy_stats: DiyStatsRange | None = Field(
        default=None, description='精灵自定义种族值，仅在合体精灵王上使用'
    )
    skill: list['SkillInPet'] = Field(description='精灵可学习的技能')
    soulmark: list[ResourceRef['Soulmark']] | None = Field(
        default=None, description='精灵可持有的魂印'
    )
    # 其他数据
    encyclopedia_entry: ResourceRef['PetEncyclopediaEntry'] | None = Field(
        default=None, description='精灵图鉴条目'
    )
    archive_story_entry: ResourceRef['PetArchiveStoryEntry'] | None = Field(
        default=None, description='精灵故事条目'
    )
    peak_pool: ResourceRef['PeakPool'] | None = Field(
        default=None, description='精灵所属巅峰池'
    )
    peak_expert_pool: ResourceRef['PeakExpertPool'] | None = Field(
        default=None, description='精灵所属巅峰专家池'
    )
    peak_pool_vote_id: int | None = Field(
        default=None, description='精灵所属巅峰池票选ID', exclude=True
    )
    advance: ResourceRef['PetAdvance'] | None = Field(
        default=None, description='精灵觉醒信息'
    )

    @classmethod
    def get_orm_model(cls) -> 'type[PetORM]':
        return PetORM

    def to_orm(self) -> 'PetORM':
        base_stats = BaseStatORM(
            id=self.id,
            **self.base_stats.model_dump(),
        )
        yielding_ev = YieldingEvORM(
            id=self.id,
            **self.yielding_ev.model_dump(),
        )
        diy_stats = self.diy_stats.to_orm(self.id) if self.diy_stats else None
        skill_links = [
            SkillInPetORM(
                skill_id=skill.skill.id,
                pet_id=self.id,
                learning_level=skill.learning_level,
                is_special=skill.is_special,
                is_advanced=skill.is_advanced,
                is_fifth=skill.is_fifth,
                skill_activation_item_id=(
                    skill.skill_activation_item.id
                    if skill.skill_activation_item
                    else None
                ),
            )
            for skill in self.skill
        ]
        return PetORM(
            id=self.id,
            name=self.name,
            yielding_exp=self.yielding_exp,
            catch_rate=self.catch_rate,
            evolving_lv=self.evolving_lv,
            releaseable=self.releaseable,
            fusion_master=self.fusion_master,
            fusion_sub=self.fusion_sub,
            has_resistance=self.has_resistance,
            type_id=self.type.id,
            gender_id=self.gender.id,
            pet_class_id=self.pet_class.id if self.pet_class else None,
            base_stats_id=cast(int, base_stats.id),
            base_stats=base_stats,
            skill_links=skill_links,
            yielding_ev_id=cast(int, yielding_ev.id),
            yielding_ev=yielding_ev,
            vipbuff_id=self.vipbuff.id if self.vipbuff else None,
            mount_type_id=self.mount_type.id if self.mount_type else None,
            diy_stats_id=diy_stats.id if diy_stats else None,
            diy_stats=diy_stats,
            resource_id=self.resource_id,
            enemy_resource_id=self.enemy_resource_id,
            peak_pool_id=self.peak_pool.id if self.peak_pool else None,
            peak_expert_pool_id=self.peak_expert_pool.id
            if self.peak_expert_pool
            else None,
            peak_pool_vote_id=self.peak_pool_vote_id,
        )


class PetORM(PetBase, table=True):
    type_id: int = Field(foreign_key='element_type_combination.id')
    type: 'TypeCombinationORM' = Relationship(
        back_populates='pet',
    )
    gender_id: int = Field(foreign_key='pet_gender.id')
    gender: 'PetGenderORM' = Relationship(
        back_populates='pet',
    )
    pet_class_id: int | None = Field(default=None, foreign_key='pet_class.id')
    pet_class: Optional['PetClassORM'] = Relationship(
        back_populates='evolution_chain',
    )
    base_stats_id: int = Field(foreign_key='pet_base_stats.id')
    base_stats: BaseStatORM = Relationship(
        back_populates='pet',
        sa_relationship_kwargs={
            'primaryjoin': 'PetORM.id == BaseStatORM.id',
        },
    )
    yielding_ev_id: int = Field(foreign_key='pet_yielding_ev.id')
    yielding_ev: YieldingEvORM = Relationship(
        back_populates='pet',
        sa_relationship_kwargs={
            'primaryjoin': 'PetORM.id == YieldingEvORM.id',
        },
    )
    # 技能，魂印
    skill_links: list['SkillInPetORM'] = Relationship(
        back_populates='pet',
    )
    soulmark: list['SoulmarkORM'] = Relationship(
        back_populates='pet',
        sa_relationship_kwargs={
            'secondary': 'petsoulmarklink',
        },
    )
    # 杂项分类
    vipbuff_id: int | None = Field(default=None, foreign_key='pet_vipbuff.id')
    vipbuff: Optional['PetVipBuffORM'] = Relationship(
        back_populates='pet',
    )
    mount_type_id: int | None = Field(default=None, foreign_key='pet_mount_type.id')
    mount_type: Optional['PetMountTypeORM'] = Relationship(
        back_populates='pet',
    )
    diy_stats_id: int | None = Field(default=None, foreign_key='pet_diy_stats_range.id')
    diy_stats: Optional['DiyStatsRangeORM'] = Relationship(
        back_populates='pet',
        sa_relationship_kwargs={
            'primaryjoin': 'PetORM.id == DiyStatsRangeORM.id',
        },
    )
    exclusive_mintmark: list['MintmarkORM'] = Relationship(
        back_populates='pet',
        sa_relationship_kwargs={
            'secondary': 'petmintmarklink',
        },
    )
    exclusive_suit_bonus: list['SuitBonusORM'] = Relationship(
        back_populates='effective_pets',
        sa_relationship_kwargs={
            'secondary': 'petsuitlink',
        },
    )
    skins: list['PetSkinORM'] = Relationship(
        back_populates='pet',
        sa_relationship_kwargs={
            'primaryjoin': 'PetORM.id == PetSkinORM.pet_id',
        },
    )
    encyclopedia: Optional['PetEncyclopediaEntryORM'] = Relationship(
        back_populates='pet',
        sa_relationship_kwargs={
            'primaryjoin': 'PetORM.id == PetEncyclopediaEntryORM.id',
        },
    )
    archive_story: Optional['PetArchiveStoryEntryORM'] = Relationship(
        back_populates='pet',
        sa_relationship_kwargs={
            'primaryjoin': 'PetORM.id == PetArchiveStoryEntryORM.pet_id',
        },
    )
    peak_pool_id: int | None = Field(default=None, foreign_key='peak_pool.id')
    peak_pool: Optional['PeakPoolORM'] = Relationship(back_populates='pet')
    peak_expert_pool_id: int | None = Field(
        default=None, foreign_key='peak_expert_pool.id'
    )
    peak_expert_pool: Optional['PeakExpertPoolORM'] = Relationship(back_populates='pet')
    peak_pool_vote_id: int | None = Field(default=None, foreign_key='peak_pool_vote.id')
    peak_pool_vote: Optional['PeakPoolVoteORM'] = Relationship(back_populates='pet')
    advance: Optional['PetAdvanceORM'] = Relationship(
        back_populates='pet',
        sa_relationship_kwargs={
            'uselist': False,
        },
    )
    glossary_entry: list['GlossaryEntryORM'] = Relationship(
        back_populates='pet',
        sa_relationship_kwargs={
            'secondary': 'petglossaryentrylink',
        },
    )


class PetClassBase(BaseResModel):
    is_variant_pet: bool = Field(default=False, description='是否是异能精灵')
    is_dark_pet: bool = Field(default=False, description='是否是暗黑精灵')
    is_shine_pet: bool = Field(default=False, description='是否是闪光精灵')
    is_rare_pet: bool = Field(default=False, description='是否是稀有精灵')
    is_breeding_pet: bool = Field(default=False, description='是否是繁殖二代精灵')
    is_fusion_pet: bool = Field(default=False, description='是否是融合二代精灵')

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_class'


class PetClass(PetClassBase, ConvertToORM['PetClassORM']):
    """描述一个精灵类别，所有第一形态为同一ID的精灵为一类"""

    evolution_chain: list[ResourceRef['Pet']] = Field(
        description='精灵进化链，从第一形态到最终形态的精灵列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['PetClassORM']:
        return PetClassORM

    def to_orm(self) -> 'PetClassORM':
        return PetClassORM(
            id=self.id,
            is_variant_pet=self.is_variant_pet,
            is_dark_pet=self.is_dark_pet,
            is_shine_pet=self.is_shine_pet,
            is_rare_pet=self.is_rare_pet,
            is_breeding_pet=self.is_breeding_pet,
            is_fusion_pet=self.is_fusion_pet,
        )


class PetClassORM(PetClassBase, table=True):
    evolution_chain: list['PetORM'] = Relationship(back_populates='pet_class')


class PetCategoryBase(BaseCategoryModel):
    name: str = Field(description='名称')
    description: str = Field(description='描述')


class PetCategoryRefs(SQLModel):
    pet: list[ResourceRef['Pet']] = Field(description='精灵列表')


class PetGenderBase(PetCategoryBase):
    @classmethod
    def resource_name(cls) -> str:
        return 'pet_gender'


class PetGenderCategory(PetGenderBase, PetCategoryRefs, ConvertToORM['PetGenderORM']):
    @classmethod
    def get_orm_model(cls) -> type['PetGenderORM']:
        return PetGenderORM

    def to_orm(self) -> 'PetGenderORM':
        return PetGenderORM(
            id=self.id,
            name=self.name,
            description=self.description,
        )


class PetGenderORM(PetGenderBase, table=True):
    pet: list['PetORM'] = Relationship(back_populates='gender')


class PetVipBuffBase(PetCategoryBase):
    @classmethod
    def resource_name(cls) -> str:
        return 'pet_vipbuff'


class PetVipBuffCategory(
    PetVipBuffBase, PetCategoryRefs, ConvertToORM['PetVipBuffORM']
):
    @classmethod
    def get_orm_model(cls) -> type['PetVipBuffORM']:
        return PetVipBuffORM

    def to_orm(self) -> 'PetVipBuffORM':
        return PetVipBuffORM(
            id=self.id,
            name=self.name,
            description=self.description,
        )


class PetVipBuffORM(PetVipBuffBase, table=True):
    pet: list['PetORM'] = Relationship(back_populates='vipbuff')


class PetMountTypeBase(PetCategoryBase):
    @classmethod
    def resource_name(cls) -> str:
        return 'pet_mount_type'


class PetMountTypeCategory(
    PetMountTypeBase, PetCategoryRefs, ConvertToORM['PetMountTypeORM']
):
    @classmethod
    def get_orm_model(cls) -> type['PetMountTypeORM']:
        return PetMountTypeORM

    def to_orm(self) -> 'PetMountTypeORM':
        return PetMountTypeORM(
            id=self.id,
            name=self.name,
            description=self.description,
        )


class PetMountTypeORM(PetMountTypeBase, table=True):
    pet: list['PetORM'] = Relationship(back_populates='mount_type')
