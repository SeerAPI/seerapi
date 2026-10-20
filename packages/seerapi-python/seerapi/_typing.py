# 由 scripts/generate_client.py 自动生成，请勿手动修改。
from typing import Literal, TypeAlias, TypeVar

import seerapi_models as M
from seerapi_models.build_model import BaseResModel
from seerapi_models.common import ResourceRef

NamedModelName: TypeAlias = Literal[
    'ability_mintmark',
    'achievement',
    'achievement_branch',
    'achievement_category',
    'achievement_type',
    'activity',
    'autocard',
    'autocard_cardtype',
    'autocard_element_type',
    'autocard_field',
    'autocard_petcard',
    'autocard_role',
    'autocard_spellcard',
    'avatar_frame',
    'avatar_head',
    'battle_effect',
    'battle_effect_type',
    'element_type',
    'element_type_combination',
    'emoji',
    'energy_bead',
    'equip',
    'equip_type',
    'error_code',
    'factor',
    'field_effect',
    'gem',
    'gem_category',
    'gem_gen1',
    'gem_gen2',
    'glossary_entry',
    'homepage_background',
    'item',
    'item_category',
    'mintmark',
    'mintmark_class',
    'mintmark_type',
    'namecard_background',
    'nature',
    'nickname_background',
    'peak_cost_pool',
    'pet',
    'pet_archive_story_book',
    'pet_effect',
    'pet_effect_group',
    'pet_encyclopedia_entry',
    'pet_gender',
    'pet_mount_type',
    'pet_skin',
    'pet_skin_series',
    'pet_skin_series_sub_type',
    'pet_variation',
    'pet_vipbuff',
    'resistance_category',
    'sign',
    'skill',
    'skill_activation_item',
    'skill_category',
    'skill_effect_type_tag',
    'skill_hide_effect',
    'skill_mintmark',
    'skill_stone',
    'skill_stone_category',
    'soulmark',
    'soulmark_tag',
    'suit',
    'title',
    'universal_mintmark',
]
ModelName: TypeAlias = Literal[
    'ability_mintmark',
    'achievement',
    'achievement_branch',
    'achievement_category',
    'achievement_type',
    'activity',
    'activity_type',
    'autocard',
    'autocard_cardtype',
    'autocard_element_type',
    'autocard_field',
    'autocard_petcard',
    'autocard_role',
    'autocard_spellcard',
    'avatar_frame',
    'avatar_head',
    'battle_effect',
    'battle_effect_type',
    'buff',
    'buff_type',
    'eid_effect',
    'element_type',
    'element_type_combination',
    'emoji',
    'energy_bead',
    'equip',
    'equip_effective_occasion',
    'equip_type',
    'error_code',
    'factor',
    'factor_design',
    'field_effect',
    'field_effect_type',
    'gem',
    'gem_category',
    'gem_gen1',
    'gem_gen2',
    'gem_generation_category',
    'glossary_entry',
    'homepage_background',
    'item',
    'item_category',
    'mintmark',
    'mintmark_class',
    'mintmark_rarity',
    'mintmark_type',
    'namecard_background',
    'nature',
    'nickname_background',
    'peak_cost_pool',
    'peak_expert_pool',
    'peak_pool',
    'peak_pool_vote',
    'peak_season',
    'pet',
    'pet_advance',
    'pet_archive_story_book',
    'pet_archive_story_entry',
    'pet_class',
    'pet_effect',
    'pet_effect_group',
    'pet_encyclopedia_entry',
    'pet_gender',
    'pet_mount_type',
    'pet_skin',
    'pet_skin_category',
    'pet_skin_series',
    'pet_skin_series_sub_type',
    'pet_variation',
    'pet_vipbuff',
    'resistance_category',
    'sign',
    'skill',
    'skill_activation_item',
    'skill_category',
    'skill_effect_param',
    'skill_effect_type',
    'skill_effect_type_tag',
    'skill_hide_effect',
    'skill_mintmark',
    'skill_stone',
    'skill_stone_category',
    'soulmark',
    'soulmark_tag',
    'suit',
    'suit_bonus',
    'title',
    'universal_mintmark',
]
ModelInstance: TypeAlias = BaseResModel
NamedModelInstance: TypeAlias = (
    M.AbilityMintmark
    | M.Achievement
    | M.AchievementBranch
    | M.AchievementCategory
    | M.AchievementType
    | M.Activity
    | M.Autocard
    | M.AutocardCardType
    | M.AutocardElementType
    | M.AutocardField
    | M.PetAutocard
    | M.AutocardRole
    | M.SpellAutocard
    | M.AvatarFrame
    | M.AvatarHead
    | M.BattleEffect
    | M.BattleEffectCategory
    | M.ElementType
    | M.TypeCombination
    | M.Emoji
    | M.EnergyBead
    | M.Equip
    | M.EquipType
    | M.ErrorCode
    | M.Factor
    | M.FieldEffect
    | M.Gem
    | M.GemCategory
    | M.GemGen1
    | M.GemGen2
    | M.GlossaryEntry
    | M.HomepageBackground
    | M.Item
    | M.ItemCategory
    | M.Mintmark
    | M.MintmarkClassCategory
    | M.MintmarkTypeCategory
    | M.NamecardBackground
    | M.Nature
    | M.NicknameBackground
    | M.PeakCostPool
    | M.Pet
    | M.PetArchiveStoryBook
    | M.PetEffect
    | M.PetEffectGroup
    | M.PetEncyclopediaEntry
    | M.PetGenderCategory
    | M.PetMountTypeCategory
    | M.PetSkin
    | M.PetSkinSeries
    | M.PetSkinSeriesSubType
    | M.VariationEffect
    | M.PetVipBuffCategory
    | M.ResistanceCategory
    | M.Sign
    | M.Skill
    | M.SkillActivationItem
    | M.SkillCategory
    | M.SkillEffectTypeTag
    | M.SkillHideEffect
    | M.SkillMintmark
    | M.SkillStone
    | M.SkillStoneCategory
    | M.Soulmark
    | M.SoulmarkTagCategory
    | M.Suit
    | M.Title
    | M.UniversalMintmark
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
