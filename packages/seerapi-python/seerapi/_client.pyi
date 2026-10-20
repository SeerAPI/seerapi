# 由 scripts/generate_client.py 自动生成，请勿手动修改。
from collections.abc import AsyncIterator
from typing import Literal, overload
from typing_extensions import Self

from hishel.httpx import AsyncCacheClient
from httpx import URL
from httpx._urls import QueryParams

from seerapi._models import PagedResponse, PageInfo
from seerapi._typing import (
    ModelName,
    ResourceArg,
    T_ModelInstance,
    T_NamedModelInstance,
)
import seerapi_models as M
from seerapi_models.common import NamedData, ResourceRef

def _parse_url_params(url: str) -> QueryParams: ...
def _parse_bool_param(value: str) -> bool: ...
def _parse_url_page_info(
    url: str | None, *, expand_fallback: bool = True
) -> PageInfo | None: ...

class SeerAPI:
    scheme: str
    hostname: str
    version_path: str
    base_url: URL
    _client: AsyncCacheClient
    def __init__(
        self,
        *,
        scheme: str = 'https',
        hostname: str = 'api.seerapi.com',
        version_path: str = 'v1',
    ) -> None: ...
    async def __aenter__(self) -> Self: ...
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...
    async def aclose(self) -> None: ...
    def _get_resource_name_from_ref(self, ref: ResourceRef[T_ModelInstance]) -> str: ...
    def _get_resource_name(
        self, resource_name: ResourceArg[T_ModelInstance]
    ) -> ModelName: ...
    @overload
    async def get(
        self, resource_name: Literal['ability_mintmark'], id: int
    ) -> M.AbilityMintmark: ...
    @overload
    async def get(
        self, resource_name: Literal['achievement'], id: int
    ) -> M.Achievement: ...
    @overload
    async def get(
        self, resource_name: Literal['achievement_branch'], id: int
    ) -> M.AchievementBranch: ...
    @overload
    async def get(
        self, resource_name: Literal['achievement_category'], id: int
    ) -> M.AchievementCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['achievement_type'], id: int
    ) -> M.AchievementType: ...
    @overload
    async def get(self, resource_name: Literal['activity'], id: int) -> M.Activity: ...
    @overload
    async def get(
        self, resource_name: Literal['activity_type'], id: int
    ) -> M.ActivityType: ...
    @overload
    async def get(self, resource_name: Literal['autocard'], id: int) -> M.Autocard: ...
    @overload
    async def get(
        self, resource_name: Literal['autocard_cardtype'], id: int
    ) -> M.AutocardCardType: ...
    @overload
    async def get(
        self, resource_name: Literal['autocard_element_type'], id: int
    ) -> M.AutocardElementType: ...
    @overload
    async def get(
        self, resource_name: Literal['autocard_field'], id: int
    ) -> M.AutocardField: ...
    @overload
    async def get(
        self, resource_name: Literal['autocard_petcard'], id: int
    ) -> M.PetAutocard: ...
    @overload
    async def get(
        self, resource_name: Literal['autocard_role'], id: int
    ) -> M.AutocardRole: ...
    @overload
    async def get(
        self, resource_name: Literal['autocard_spellcard'], id: int
    ) -> M.SpellAutocard: ...
    @overload
    async def get(
        self, resource_name: Literal['avatar_frame'], id: int
    ) -> M.AvatarFrame: ...
    @overload
    async def get(
        self, resource_name: Literal['avatar_head'], id: int
    ) -> M.AvatarHead: ...
    @overload
    async def get(
        self, resource_name: Literal['battle_effect'], id: int
    ) -> M.BattleEffect: ...
    @overload
    async def get(
        self, resource_name: Literal['battle_effect_type'], id: int
    ) -> M.BattleEffectCategory: ...
    @overload
    async def get(self, resource_name: Literal['buff'], id: int) -> M.Buff: ...
    @overload
    async def get(self, resource_name: Literal['buff_type'], id: int) -> M.BuffType: ...
    @overload
    async def get(
        self, resource_name: Literal['eid_effect'], id: int
    ) -> M.EidEffect: ...
    @overload
    async def get(
        self, resource_name: Literal['element_type'], id: int
    ) -> M.ElementType: ...
    @overload
    async def get(
        self, resource_name: Literal['element_type_combination'], id: int
    ) -> M.TypeCombination: ...
    @overload
    async def get(self, resource_name: Literal['emoji'], id: int) -> M.Emoji: ...
    @overload
    async def get(
        self, resource_name: Literal['energy_bead'], id: int
    ) -> M.EnergyBead: ...
    @overload
    async def get(self, resource_name: Literal['equip'], id: int) -> M.Equip: ...
    @overload
    async def get(
        self, resource_name: Literal['equip_effective_occasion'], id: int
    ) -> M.EquipEffectiveOccasion: ...
    @overload
    async def get(
        self, resource_name: Literal['equip_type'], id: int
    ) -> M.EquipType: ...
    @overload
    async def get(
        self, resource_name: Literal['error_code'], id: int
    ) -> M.ErrorCode: ...
    @overload
    async def get(self, resource_name: Literal['factor'], id: int) -> M.Factor: ...
    @overload
    async def get(
        self, resource_name: Literal['factor_design'], id: int
    ) -> M.FactorDesign: ...
    @overload
    async def get(
        self, resource_name: Literal['field_effect'], id: int
    ) -> M.FieldEffect: ...
    @overload
    async def get(
        self, resource_name: Literal['field_effect_type'], id: int
    ) -> M.FieldEffectType: ...
    @overload
    async def get(self, resource_name: Literal['gem'], id: int) -> M.Gem: ...
    @overload
    async def get(
        self, resource_name: Literal['gem_category'], id: int
    ) -> M.GemCategory: ...
    @overload
    async def get(self, resource_name: Literal['gem_gen1'], id: int) -> M.GemGen1: ...
    @overload
    async def get(self, resource_name: Literal['gem_gen2'], id: int) -> M.GemGen2: ...
    @overload
    async def get(
        self, resource_name: Literal['gem_generation_category'], id: int
    ) -> M.GemGenCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['glossary_entry'], id: int
    ) -> M.GlossaryEntry: ...
    @overload
    async def get(
        self, resource_name: Literal['homepage_background'], id: int
    ) -> M.HomepageBackground: ...
    @overload
    async def get(self, resource_name: Literal['item'], id: int) -> M.Item: ...
    @overload
    async def get(
        self, resource_name: Literal['item_category'], id: int
    ) -> M.ItemCategory: ...
    @overload
    async def get(self, resource_name: Literal['mintmark'], id: int) -> M.Mintmark: ...
    @overload
    async def get(
        self, resource_name: Literal['mintmark_class'], id: int
    ) -> M.MintmarkClassCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['mintmark_rarity'], id: int
    ) -> M.MintmarkRarityCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['mintmark_type'], id: int
    ) -> M.MintmarkTypeCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['namecard_background'], id: int
    ) -> M.NamecardBackground: ...
    @overload
    async def get(self, resource_name: Literal['nature'], id: int) -> M.Nature: ...
    @overload
    async def get(
        self, resource_name: Literal['nickname_background'], id: int
    ) -> M.NicknameBackground: ...
    @overload
    async def get(
        self, resource_name: Literal['peak_cost_pool'], id: int
    ) -> M.PeakCostPool: ...
    @overload
    async def get(
        self, resource_name: Literal['peak_expert_pool'], id: int
    ) -> M.PeakExpertPool: ...
    @overload
    async def get(self, resource_name: Literal['peak_pool'], id: int) -> M.PeakPool: ...
    @overload
    async def get(
        self, resource_name: Literal['peak_pool_vote'], id: int
    ) -> M.PeakPoolVote: ...
    @overload
    async def get(
        self, resource_name: Literal['peak_season'], id: int
    ) -> M.PeakSeason: ...
    @overload
    async def get(self, resource_name: Literal['pet'], id: int) -> M.Pet: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_advance'], id: int
    ) -> M.PetAdvance: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_archive_story_book'], id: int
    ) -> M.PetArchiveStoryBook: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_archive_story_entry'], id: int
    ) -> M.PetArchiveStoryEntry: ...
    @overload
    async def get(self, resource_name: Literal['pet_class'], id: int) -> M.PetClass: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_effect'], id: int
    ) -> M.PetEffect: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_effect_group'], id: int
    ) -> M.PetEffectGroup: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_encyclopedia_entry'], id: int
    ) -> M.PetEncyclopediaEntry: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_gender'], id: int
    ) -> M.PetGenderCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_mount_type'], id: int
    ) -> M.PetMountTypeCategory: ...
    @overload
    async def get(self, resource_name: Literal['pet_skin'], id: int) -> M.PetSkin: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_skin_category'], id: int
    ) -> M.PetSkinCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_skin_series'], id: int
    ) -> M.PetSkinSeries: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_skin_series_sub_type'], id: int
    ) -> M.PetSkinSeriesSubType: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_variation'], id: int
    ) -> M.VariationEffect: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_vipbuff'], id: int
    ) -> M.PetVipBuffCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['resistance_category'], id: int
    ) -> M.ResistanceCategory: ...
    @overload
    async def get(self, resource_name: Literal['sign'], id: int) -> M.Sign: ...
    @overload
    async def get(self, resource_name: Literal['skill'], id: int) -> M.Skill: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_activation_item'], id: int
    ) -> M.SkillActivationItem: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_category'], id: int
    ) -> M.SkillCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_effect_param'], id: int
    ) -> M.SkillEffectParam: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_effect_type'], id: int
    ) -> M.SkillEffectType: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_effect_type_tag'], id: int
    ) -> M.SkillEffectTypeTag: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_hide_effect'], id: int
    ) -> M.SkillHideEffect: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_mintmark'], id: int
    ) -> M.SkillMintmark: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_stone'], id: int
    ) -> M.SkillStone: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_stone_category'], id: int
    ) -> M.SkillStoneCategory: ...
    @overload
    async def get(self, resource_name: Literal['soulmark'], id: int) -> M.Soulmark: ...
    @overload
    async def get(
        self, resource_name: Literal['soulmark_tag'], id: int
    ) -> M.SoulmarkTagCategory: ...
    @overload
    async def get(self, resource_name: Literal['suit'], id: int) -> M.Suit: ...
    @overload
    async def get(
        self, resource_name: Literal['suit_bonus'], id: int
    ) -> M.SuitBonus: ...
    @overload
    async def get(self, resource_name: Literal['title'], id: int) -> M.Title: ...
    @overload
    async def get(
        self, resource_name: Literal['universal_mintmark'], id: int
    ) -> M.UniversalMintmark: ...
    @overload
    async def get(
        self, resource_name: type[T_ModelInstance], id: int
    ) -> T_ModelInstance: ...
    @overload
    async def get(
        self, resource_name: ResourceRef[T_ModelInstance], id: int | None = None
    ) -> T_ModelInstance: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['ability_mintmark'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.AbilityMintmark]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['achievement'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.Achievement]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['achievement_branch'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.AchievementBranch]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['achievement_category'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.AchievementCategory]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['achievement_type'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.AchievementType]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['activity'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.Activity]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['activity_type'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.ActivityType]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['autocard'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.Autocard]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['autocard_cardtype'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.AutocardCardType]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['autocard_element_type'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.AutocardElementType]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['autocard_field'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.AutocardField]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['autocard_petcard'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.PetAutocard]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['autocard_role'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.AutocardRole]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['autocard_spellcard'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.SpellAutocard]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['avatar_frame'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.AvatarFrame]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['avatar_head'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.AvatarHead]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['battle_effect'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.BattleEffect]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['battle_effect_type'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.BattleEffectCategory]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['buff'], page_info: PageInfo, *, name: None = None
    ) -> PagedResponse[M.Buff]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['buff_type'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.BuffType]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['eid_effect'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.EidEffect]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['element_type'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.ElementType]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['element_type_combination'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.TypeCombination]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['emoji'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.Emoji]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['energy_bead'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.EnergyBead]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['equip'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.Equip]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['equip_effective_occasion'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.EquipEffectiveOccasion]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['equip_type'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.EquipType]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['error_code'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.ErrorCode]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['factor'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.Factor]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['factor_design'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.FactorDesign]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['field_effect'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.FieldEffect]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['field_effect_type'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.FieldEffectType]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['gem'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.Gem]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['gem_category'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.GemCategory]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['gem_gen1'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.GemGen1]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['gem_gen2'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.GemGen2]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['gem_generation_category'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.GemGenCategory]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['glossary_entry'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.GlossaryEntry]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['homepage_background'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.HomepageBackground]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['item'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.Item]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['item_category'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.ItemCategory]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['mintmark'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.Mintmark]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['mintmark_class'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.MintmarkClassCategory]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['mintmark_rarity'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.MintmarkRarityCategory]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['mintmark_type'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.MintmarkTypeCategory]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['namecard_background'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.NamecardBackground]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['nature'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.Nature]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['nickname_background'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.NicknameBackground]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['peak_cost_pool'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.PeakCostPool]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['peak_expert_pool'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.PeakExpertPool]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['peak_pool'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.PeakPool]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['peak_pool_vote'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.PeakPoolVote]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['peak_season'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.PeakSeason]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['pet'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.Pet]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['pet_advance'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.PetAdvance]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['pet_archive_story_book'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.PetArchiveStoryBook]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['pet_archive_story_entry'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.PetArchiveStoryEntry]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['pet_class'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.PetClass]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['pet_effect'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.PetEffect]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['pet_effect_group'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.PetEffectGroup]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['pet_encyclopedia_entry'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.PetEncyclopediaEntry]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['pet_gender'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.PetGenderCategory]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['pet_mount_type'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.PetMountTypeCategory]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['pet_skin'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.PetSkin]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['pet_skin_category'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.PetSkinCategory]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['pet_skin_series'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.PetSkinSeries]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['pet_skin_series_sub_type'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.PetSkinSeriesSubType]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['pet_variation'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.VariationEffect]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['pet_vipbuff'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.PetVipBuffCategory]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['resistance_category'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.ResistanceCategory]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['sign'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.Sign]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['skill'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.Skill]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['skill_activation_item'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.SkillActivationItem]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['skill_category'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.SkillCategory]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['skill_effect_param'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.SkillEffectParam]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['skill_effect_type'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.SkillEffectType]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['skill_effect_type_tag'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.SkillEffectTypeTag]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['skill_hide_effect'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.SkillHideEffect]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['skill_mintmark'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.SkillMintmark]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['skill_stone'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.SkillStone]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['skill_stone_category'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.SkillStoneCategory]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['soulmark'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.Soulmark]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['soulmark_tag'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.SoulmarkTagCategory]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['suit'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.Suit]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['suit_bonus'],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[M.SuitBonus]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['title'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.Title]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: Literal['universal_mintmark'],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[M.UniversalMintmark]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: type[T_NamedModelInstance],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[T_NamedModelInstance]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: ResourceRef[T_NamedModelInstance],
        page_info: PageInfo,
        *,
        name: str | None = None,
    ) -> PagedResponse[T_NamedModelInstance]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: type[T_ModelInstance],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[T_ModelInstance]: ...
    @overload
    async def paginated_list(
        self,
        resource_name: ResourceRef[T_ModelInstance],
        page_info: PageInfo,
        *,
        name: None = None,
    ) -> PagedResponse[T_ModelInstance]: ...
    @overload
    def list(
        self,
        resource_name: Literal['ability_mintmark'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.AbilityMintmark]: ...
    @overload
    def list(
        self,
        resource_name: Literal['achievement'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.Achievement]: ...
    @overload
    def list(
        self,
        resource_name: Literal['achievement_branch'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.AchievementBranch]: ...
    @overload
    def list(
        self,
        resource_name: Literal['achievement_category'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.AchievementCategory]: ...
    @overload
    def list(
        self,
        resource_name: Literal['achievement_type'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.AchievementType]: ...
    @overload
    def list(
        self,
        resource_name: Literal['activity'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.Activity]: ...
    @overload
    def list(
        self,
        resource_name: Literal['activity_type'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.ActivityType]: ...
    @overload
    def list(
        self,
        resource_name: Literal['autocard'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.Autocard]: ...
    @overload
    def list(
        self,
        resource_name: Literal['autocard_cardtype'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.AutocardCardType]: ...
    @overload
    def list(
        self,
        resource_name: Literal['autocard_element_type'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.AutocardElementType]: ...
    @overload
    def list(
        self,
        resource_name: Literal['autocard_field'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.AutocardField]: ...
    @overload
    def list(
        self,
        resource_name: Literal['autocard_petcard'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.PetAutocard]: ...
    @overload
    def list(
        self,
        resource_name: Literal['autocard_role'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.AutocardRole]: ...
    @overload
    def list(
        self,
        resource_name: Literal['autocard_spellcard'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.SpellAutocard]: ...
    @overload
    def list(
        self,
        resource_name: Literal['avatar_frame'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.AvatarFrame]: ...
    @overload
    def list(
        self,
        resource_name: Literal['avatar_head'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.AvatarHead]: ...
    @overload
    def list(
        self,
        resource_name: Literal['battle_effect'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.BattleEffect]: ...
    @overload
    def list(
        self,
        resource_name: Literal['battle_effect_type'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.BattleEffectCategory]: ...
    @overload
    def list(
        self, resource_name: Literal['buff'], *, expand: bool = True, name: None = None
    ) -> AsyncIterator[M.Buff]: ...
    @overload
    def list(
        self,
        resource_name: Literal['buff_type'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.BuffType]: ...
    @overload
    def list(
        self,
        resource_name: Literal['eid_effect'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.EidEffect]: ...
    @overload
    def list(
        self,
        resource_name: Literal['element_type'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.ElementType]: ...
    @overload
    def list(
        self,
        resource_name: Literal['element_type_combination'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.TypeCombination]: ...
    @overload
    def list(
        self,
        resource_name: Literal['emoji'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.Emoji]: ...
    @overload
    def list(
        self,
        resource_name: Literal['energy_bead'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.EnergyBead]: ...
    @overload
    def list(
        self,
        resource_name: Literal['equip'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.Equip]: ...
    @overload
    def list(
        self,
        resource_name: Literal['equip_effective_occasion'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.EquipEffectiveOccasion]: ...
    @overload
    def list(
        self,
        resource_name: Literal['equip_type'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.EquipType]: ...
    @overload
    def list(
        self,
        resource_name: Literal['error_code'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.ErrorCode]: ...
    @overload
    def list(
        self,
        resource_name: Literal['factor'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.Factor]: ...
    @overload
    def list(
        self,
        resource_name: Literal['factor_design'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.FactorDesign]: ...
    @overload
    def list(
        self,
        resource_name: Literal['field_effect'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.FieldEffect]: ...
    @overload
    def list(
        self,
        resource_name: Literal['field_effect_type'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.FieldEffectType]: ...
    @overload
    def list(
        self,
        resource_name: Literal['gem'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.Gem]: ...
    @overload
    def list(
        self,
        resource_name: Literal['gem_category'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.GemCategory]: ...
    @overload
    def list(
        self,
        resource_name: Literal['gem_gen1'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.GemGen1]: ...
    @overload
    def list(
        self,
        resource_name: Literal['gem_gen2'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.GemGen2]: ...
    @overload
    def list(
        self,
        resource_name: Literal['gem_generation_category'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.GemGenCategory]: ...
    @overload
    def list(
        self,
        resource_name: Literal['glossary_entry'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.GlossaryEntry]: ...
    @overload
    def list(
        self,
        resource_name: Literal['homepage_background'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.HomepageBackground]: ...
    @overload
    def list(
        self,
        resource_name: Literal['item'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.Item]: ...
    @overload
    def list(
        self,
        resource_name: Literal['item_category'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.ItemCategory]: ...
    @overload
    def list(
        self,
        resource_name: Literal['mintmark'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.Mintmark]: ...
    @overload
    def list(
        self,
        resource_name: Literal['mintmark_class'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.MintmarkClassCategory]: ...
    @overload
    def list(
        self,
        resource_name: Literal['mintmark_rarity'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.MintmarkRarityCategory]: ...
    @overload
    def list(
        self,
        resource_name: Literal['mintmark_type'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.MintmarkTypeCategory]: ...
    @overload
    def list(
        self,
        resource_name: Literal['namecard_background'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.NamecardBackground]: ...
    @overload
    def list(
        self,
        resource_name: Literal['nature'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.Nature]: ...
    @overload
    def list(
        self,
        resource_name: Literal['nickname_background'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.NicknameBackground]: ...
    @overload
    def list(
        self,
        resource_name: Literal['peak_cost_pool'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.PeakCostPool]: ...
    @overload
    def list(
        self,
        resource_name: Literal['peak_expert_pool'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.PeakExpertPool]: ...
    @overload
    def list(
        self,
        resource_name: Literal['peak_pool'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.PeakPool]: ...
    @overload
    def list(
        self,
        resource_name: Literal['peak_pool_vote'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.PeakPoolVote]: ...
    @overload
    def list(
        self,
        resource_name: Literal['peak_season'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.PeakSeason]: ...
    @overload
    def list(
        self,
        resource_name: Literal['pet'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.Pet]: ...
    @overload
    def list(
        self,
        resource_name: Literal['pet_advance'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.PetAdvance]: ...
    @overload
    def list(
        self,
        resource_name: Literal['pet_archive_story_book'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.PetArchiveStoryBook]: ...
    @overload
    def list(
        self,
        resource_name: Literal['pet_archive_story_entry'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.PetArchiveStoryEntry]: ...
    @overload
    def list(
        self,
        resource_name: Literal['pet_class'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.PetClass]: ...
    @overload
    def list(
        self,
        resource_name: Literal['pet_effect'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.PetEffect]: ...
    @overload
    def list(
        self,
        resource_name: Literal['pet_effect_group'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.PetEffectGroup]: ...
    @overload
    def list(
        self,
        resource_name: Literal['pet_encyclopedia_entry'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.PetEncyclopediaEntry]: ...
    @overload
    def list(
        self,
        resource_name: Literal['pet_gender'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.PetGenderCategory]: ...
    @overload
    def list(
        self,
        resource_name: Literal['pet_mount_type'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.PetMountTypeCategory]: ...
    @overload
    def list(
        self,
        resource_name: Literal['pet_skin'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.PetSkin]: ...
    @overload
    def list(
        self,
        resource_name: Literal['pet_skin_category'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.PetSkinCategory]: ...
    @overload
    def list(
        self,
        resource_name: Literal['pet_skin_series'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.PetSkinSeries]: ...
    @overload
    def list(
        self,
        resource_name: Literal['pet_skin_series_sub_type'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.PetSkinSeriesSubType]: ...
    @overload
    def list(
        self,
        resource_name: Literal['pet_variation'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.VariationEffect]: ...
    @overload
    def list(
        self,
        resource_name: Literal['pet_vipbuff'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.PetVipBuffCategory]: ...
    @overload
    def list(
        self,
        resource_name: Literal['resistance_category'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.ResistanceCategory]: ...
    @overload
    def list(
        self,
        resource_name: Literal['sign'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.Sign]: ...
    @overload
    def list(
        self,
        resource_name: Literal['skill'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.Skill]: ...
    @overload
    def list(
        self,
        resource_name: Literal['skill_activation_item'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.SkillActivationItem]: ...
    @overload
    def list(
        self,
        resource_name: Literal['skill_category'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.SkillCategory]: ...
    @overload
    def list(
        self,
        resource_name: Literal['skill_effect_param'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.SkillEffectParam]: ...
    @overload
    def list(
        self,
        resource_name: Literal['skill_effect_type'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.SkillEffectType]: ...
    @overload
    def list(
        self,
        resource_name: Literal['skill_effect_type_tag'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.SkillEffectTypeTag]: ...
    @overload
    def list(
        self,
        resource_name: Literal['skill_hide_effect'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.SkillHideEffect]: ...
    @overload
    def list(
        self,
        resource_name: Literal['skill_mintmark'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.SkillMintmark]: ...
    @overload
    def list(
        self,
        resource_name: Literal['skill_stone'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.SkillStone]: ...
    @overload
    def list(
        self,
        resource_name: Literal['skill_stone_category'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.SkillStoneCategory]: ...
    @overload
    def list(
        self,
        resource_name: Literal['soulmark'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.Soulmark]: ...
    @overload
    def list(
        self,
        resource_name: Literal['soulmark_tag'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.SoulmarkTagCategory]: ...
    @overload
    def list(
        self,
        resource_name: Literal['suit'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.Suit]: ...
    @overload
    def list(
        self,
        resource_name: Literal['suit_bonus'],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[M.SuitBonus]: ...
    @overload
    def list(
        self,
        resource_name: Literal['title'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.Title]: ...
    @overload
    def list(
        self,
        resource_name: Literal['universal_mintmark'],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[M.UniversalMintmark]: ...
    @overload
    def list(
        self,
        resource_name: type[T_NamedModelInstance],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[T_NamedModelInstance]: ...
    @overload
    def list(
        self,
        resource_name: ResourceRef[T_NamedModelInstance],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[T_NamedModelInstance]: ...
    @overload
    def list(
        self,
        resource_name: type[T_ModelInstance],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[T_ModelInstance]: ...
    @overload
    def list(
        self,
        resource_name: ResourceRef[T_ModelInstance],
        *,
        expand: bool = True,
        name: None = None,
    ) -> AsyncIterator[T_ModelInstance]: ...
    def _list_gen(
        self,
        resource_name: ResourceArg[T_ModelInstance],
        *,
        expand: bool = True,
        name: str | None = None,
    ) -> AsyncIterator[T_ModelInstance]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['ability_mintmark'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.AbilityMintmark]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['achievement'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.Achievement]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['achievement_branch'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.AchievementBranch]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['achievement_category'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.AchievementCategory]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['achievement_type'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.AchievementType]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['activity'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.Activity]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['autocard'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.Autocard]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['autocard_cardtype'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.AutocardCardType]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['autocard_element_type'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.AutocardElementType]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['autocard_field'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.AutocardField]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['autocard_petcard'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.PetAutocard]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['autocard_role'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.AutocardRole]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['autocard_spellcard'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.SpellAutocard]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['avatar_frame'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.AvatarFrame]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['avatar_head'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.AvatarHead]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['battle_effect'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.BattleEffect]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['battle_effect_type'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.BattleEffectCategory]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['element_type'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.ElementType]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['element_type_combination'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.TypeCombination]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['emoji'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.Emoji]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['energy_bead'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.EnergyBead]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['equip'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.Equip]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['equip_type'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.EquipType]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['error_code'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.ErrorCode]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['factor'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.Factor]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['field_effect'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.FieldEffect]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['gem'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.Gem]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['gem_category'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.GemCategory]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['gem_gen1'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.GemGen1]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['gem_gen2'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.GemGen2]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['glossary_entry'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.GlossaryEntry]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['homepage_background'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.HomepageBackground]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['item'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.Item]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['item_category'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.ItemCategory]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['mintmark'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.Mintmark]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['mintmark_class'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.MintmarkClassCategory]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['mintmark_type'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.MintmarkTypeCategory]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['namecard_background'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.NamecardBackground]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['nature'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.Nature]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['nickname_background'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.NicknameBackground]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['peak_cost_pool'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.PeakCostPool]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['pet'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.Pet]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['pet_archive_story_book'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.PetArchiveStoryBook]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['pet_effect'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.PetEffect]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['pet_effect_group'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.PetEffectGroup]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['pet_encyclopedia_entry'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.PetEncyclopediaEntry]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['pet_gender'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.PetGenderCategory]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['pet_mount_type'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.PetMountTypeCategory]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['pet_skin'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.PetSkin]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['pet_skin_series'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.PetSkinSeries]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['pet_skin_series_sub_type'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.PetSkinSeriesSubType]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['pet_variation'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.VariationEffect]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['pet_vipbuff'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.PetVipBuffCategory]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['resistance_category'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.ResistanceCategory]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['sign'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.Sign]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['skill'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.Skill]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['skill_activation_item'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.SkillActivationItem]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['skill_category'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.SkillCategory]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['skill_effect_type_tag'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.SkillEffectTypeTag]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['skill_hide_effect'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.SkillHideEffect]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['skill_mintmark'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.SkillMintmark]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['skill_stone'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.SkillStone]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['skill_stone_category'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.SkillStoneCategory]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['soulmark'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.Soulmark]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['soulmark_tag'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.SoulmarkTagCategory]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['suit'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.Suit]: ...
    @overload
    def search_by_name(
        self, resource_name: Literal['title'], name: str, *, expand: bool = True
    ) -> AsyncIterator[M.Title]: ...
    @overload
    def search_by_name(
        self,
        resource_name: Literal['universal_mintmark'],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[M.UniversalMintmark]: ...
    @overload
    def search_by_name(
        self,
        resource_name: type[T_NamedModelInstance],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[T_NamedModelInstance]: ...
    @overload
    def search_by_name(
        self,
        resource_name: ResourceRef[T_NamedModelInstance],
        name: str,
        *,
        expand: bool = True,
    ) -> AsyncIterator[T_NamedModelInstance]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['ability_mintmark'], name: str
    ) -> NamedData[M.AbilityMintmark]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['achievement'], name: str
    ) -> NamedData[M.Achievement]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['achievement_branch'], name: str
    ) -> NamedData[M.AchievementBranch]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['achievement_category'], name: str
    ) -> NamedData[M.AchievementCategory]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['achievement_type'], name: str
    ) -> NamedData[M.AchievementType]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['activity'], name: str
    ) -> NamedData[M.Activity]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['autocard'], name: str
    ) -> NamedData[M.Autocard]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['autocard_cardtype'], name: str
    ) -> NamedData[M.AutocardCardType]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['autocard_element_type'], name: str
    ) -> NamedData[M.AutocardElementType]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['autocard_field'], name: str
    ) -> NamedData[M.AutocardField]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['autocard_petcard'], name: str
    ) -> NamedData[M.PetAutocard]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['autocard_role'], name: str
    ) -> NamedData[M.AutocardRole]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['autocard_spellcard'], name: str
    ) -> NamedData[M.SpellAutocard]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['avatar_frame'], name: str
    ) -> NamedData[M.AvatarFrame]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['avatar_head'], name: str
    ) -> NamedData[M.AvatarHead]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['battle_effect'], name: str
    ) -> NamedData[M.BattleEffect]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['battle_effect_type'], name: str
    ) -> NamedData[M.BattleEffectCategory]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['element_type'], name: str
    ) -> NamedData[M.ElementType]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['element_type_combination'], name: str
    ) -> NamedData[M.TypeCombination]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['emoji'], name: str
    ) -> NamedData[M.Emoji]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['energy_bead'], name: str
    ) -> NamedData[M.EnergyBead]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['equip'], name: str
    ) -> NamedData[M.Equip]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['equip_type'], name: str
    ) -> NamedData[M.EquipType]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['error_code'], name: str
    ) -> NamedData[M.ErrorCode]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['factor'], name: str
    ) -> NamedData[M.Factor]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['field_effect'], name: str
    ) -> NamedData[M.FieldEffect]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['gem'], name: str
    ) -> NamedData[M.Gem]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['gem_category'], name: str
    ) -> NamedData[M.GemCategory]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['gem_gen1'], name: str
    ) -> NamedData[M.GemGen1]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['gem_gen2'], name: str
    ) -> NamedData[M.GemGen2]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['glossary_entry'], name: str
    ) -> NamedData[M.GlossaryEntry]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['homepage_background'], name: str
    ) -> NamedData[M.HomepageBackground]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['item'], name: str
    ) -> NamedData[M.Item]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['item_category'], name: str
    ) -> NamedData[M.ItemCategory]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['mintmark'], name: str
    ) -> NamedData[M.Mintmark]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['mintmark_class'], name: str
    ) -> NamedData[M.MintmarkClassCategory]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['mintmark_type'], name: str
    ) -> NamedData[M.MintmarkTypeCategory]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['namecard_background'], name: str
    ) -> NamedData[M.NamecardBackground]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['nature'], name: str
    ) -> NamedData[M.Nature]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['nickname_background'], name: str
    ) -> NamedData[M.NicknameBackground]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['peak_cost_pool'], name: str
    ) -> NamedData[M.PeakCostPool]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet'], name: str
    ) -> NamedData[M.Pet]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet_archive_story_book'], name: str
    ) -> NamedData[M.PetArchiveStoryBook]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet_effect'], name: str
    ) -> NamedData[M.PetEffect]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet_effect_group'], name: str
    ) -> NamedData[M.PetEffectGroup]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet_encyclopedia_entry'], name: str
    ) -> NamedData[M.PetEncyclopediaEntry]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet_gender'], name: str
    ) -> NamedData[M.PetGenderCategory]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet_mount_type'], name: str
    ) -> NamedData[M.PetMountTypeCategory]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet_skin'], name: str
    ) -> NamedData[M.PetSkin]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet_skin_series'], name: str
    ) -> NamedData[M.PetSkinSeries]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet_skin_series_sub_type'], name: str
    ) -> NamedData[M.PetSkinSeriesSubType]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet_variation'], name: str
    ) -> NamedData[M.VariationEffect]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet_vipbuff'], name: str
    ) -> NamedData[M.PetVipBuffCategory]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['resistance_category'], name: str
    ) -> NamedData[M.ResistanceCategory]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['sign'], name: str
    ) -> NamedData[M.Sign]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['skill'], name: str
    ) -> NamedData[M.Skill]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['skill_activation_item'], name: str
    ) -> NamedData[M.SkillActivationItem]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['skill_category'], name: str
    ) -> NamedData[M.SkillCategory]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['skill_effect_type_tag'], name: str
    ) -> NamedData[M.SkillEffectTypeTag]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['skill_hide_effect'], name: str
    ) -> NamedData[M.SkillHideEffect]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['skill_mintmark'], name: str
    ) -> NamedData[M.SkillMintmark]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['skill_stone'], name: str
    ) -> NamedData[M.SkillStone]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['skill_stone_category'], name: str
    ) -> NamedData[M.SkillStoneCategory]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['soulmark'], name: str
    ) -> NamedData[M.Soulmark]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['soulmark_tag'], name: str
    ) -> NamedData[M.SoulmarkTagCategory]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['suit'], name: str
    ) -> NamedData[M.Suit]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['title'], name: str
    ) -> NamedData[M.Title]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['universal_mintmark'], name: str
    ) -> NamedData[M.UniversalMintmark]: ...
    @overload
    async def get_by_name(
        self, resource_name: type[T_NamedModelInstance], name: str
    ) -> NamedData[T_NamedModelInstance]: ...
    @overload
    async def get_by_name(
        self, resource_name: ResourceRef[T_NamedModelInstance], name: str
    ) -> NamedData[T_NamedModelInstance]: ...
