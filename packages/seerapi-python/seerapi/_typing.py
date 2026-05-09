from typing import Literal, TypeAlias, TypeVar

import seerapi_models as M
from seerapi_models.build_model import BaseResModel
from seerapi_models.common import ResourceRef

# 所有可用的命名模型路径名称
NamedModelName: TypeAlias = Literal[
    'achievement',
    'achievement_branch',
    'achievement_category',
    'achievement_type',
    'title',
    'battle_effect',
    'battle_effect_type',
    'pet_effect',
    'pet_effect_group',
    'pet_variation',
    'energy_bead',
    'equip',
    'suit',
    'equip_type',
    'soulmark_tag',
    'element_type',
    'element_type_combination',
    'item',
    'item_category',
    'gem',
    'gem_category',
    'skill_activation_item',
    'skill_stone',
    'skill_stone_category',
    'mintmark',
    'ability_mintmark',
    'skill_mintmark',
    'universal_mintmark',
    'mintmark_class',
    'mintmark_type',
    'pet',
    'pet_gender',
    'pet_vipbuff',
    'pet_mount_type',
    'pet_skin',
    'pet_skin_series',
    'pet_skin_series_sub_type',
    'pet_archive_story_book',
    'pet_encyclopedia_entry',
    'nature',
    'skill',
    'skill_hide_effect',
    'skill_category',
    'skill_effect_type_tag',
    'soulmark',
    'glossary_entry',
    'error_code',
    'avatar_head',
    'avatar_frame',
    'namecard_background',
    'nickname_background',
    'homepage_background',
    'emoji',
]

# 所有可用的模型路径名称
ModelName: TypeAlias = Literal[
    NamedModelName,
    'equip_effective_occasion',
    'gem_generation_category',
    'mintmark_rarity',
    'pet_class',
    'pet_skin_category',
    'pet_archive_story_entry',
    'skill_effect_type',
    'skill_effect_param',
    'eid_effect',
    'peak_pool',
    'peak_expert_pool',
    'peak_pool_vote',
    'pet_advance',
    'peak_season',
]

ModelInstance: TypeAlias = BaseResModel
NamedModelInstance: TypeAlias = (
    M.Achievement
    | M.AchievementBranch
    | M.AchievementCategory
    | M.AchievementType
    | M.Title
    | M.BattleEffect
    | M.BattleEffectCategory
    | M.PetEffect
    | M.PetEffectGroup
    | M.VariationEffect
    | M.EnergyBead
    | M.Equip
    | M.Suit
    | M.EquipType
    | M.SoulmarkTagCategory
    | M.ElementType
    | M.TypeCombination
    | M.Item
    | M.ItemCategory
    | M.Gem
    | M.GemCategory
    | M.SkillActivationItem
    | M.SkillStone
    | M.SkillStoneCategory
    | M.Soulmark
    | M.Mintmark
    | M.AbilityMintmark
    | M.SkillMintmark
    | M.UniversalMintmark
    | M.MintmarkClassCategory
    | M.MintmarkTypeCategory
    | M.Pet
    | M.PetGenderCategory
    | M.PetVipBuffCategory
    | M.PetMountTypeCategory
    | M.PetSkin
    | M.PetSkinSeries
    | M.PetSkinSeriesSubType
    | M.PetArchiveStoryBook
    | M.PetEncyclopediaEntry
    | M.Nature
    | M.Skill
    | M.SkillHideEffect
    | M.SkillCategory
    | M.SkillEffectTypeTag
    | M.GlossaryEntry
    | M.AvatarHead
    | M.AvatarFrame
    | M.NamecardBackground
    | M.NicknameBackground
    | M.HomepageBackground
    | M.Emoji
    | M.ErrorCode
)
ModelType: TypeAlias = type[ModelInstance]

T_ModelInstance = TypeVar('T_ModelInstance', bound=ModelInstance)
T_NamedModelInstance = TypeVar('T_NamedModelInstance', bound=NamedModelInstance)

ResourceArg: TypeAlias = (
    ModelName | type[T_ModelInstance] | ResourceRef[T_ModelInstance]
)
NamedResourceArg: TypeAlias = (
    NamedModelName | type[T_NamedModelInstance] | ResourceRef[T_NamedModelInstance]
)
