from collections.abc import AsyncGenerator
from typing import Literal, overload
from typing_extensions import Self

from hishel.httpx import AsyncCacheClient
from httpx import URL

from seerapi._models import PagedResponse, PageInfo
from seerapi._typing import T_ModelInstance, T_NamedModelInstance
import seerapi_models as M
from seerapi_models.common import NamedData, ResourceRef

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
    async def get(self, resource_name: Literal['title'], id: int) -> M.Title: ...
    @overload
    async def get(
        self, resource_name: Literal['battle_effect'], id: int
    ) -> M.BattleEffect: ...
    @overload
    async def get(
        self, resource_name: Literal['battle_effect_type'], id: int
    ) -> M.BattleEffectCategory: ...
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
        self, resource_name: Literal['pet_variation'], id: int
    ) -> M.VariationEffect: ...
    @overload
    async def get(
        self, resource_name: Literal['energy_bead'], id: int
    ) -> M.EnergyBead: ...
    @overload
    async def get(self, resource_name: Literal['equip'], id: int) -> M.Equip: ...
    @overload
    async def get(self, resource_name: Literal['suit'], id: int) -> M.Suit: ...
    @overload
    async def get(
        self, resource_name: Literal['equip_type'], id: int
    ) -> M.EquipType: ...
    @overload
    async def get(
        self, resource_name: Literal['equip_effective_occasion'], id: int
    ) -> M.EquipEffectiveOccasion: ...
    @overload
    async def get(self, resource_name: Literal['soulmark'], id: int) -> M.Soulmark: ...
    @overload
    async def get(
        self, resource_name: Literal['soulmark_tag'], id: int
    ) -> M.SoulmarkTagCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['element_type'], id: int
    ) -> M.ElementType: ...
    @overload
    async def get(
        self, resource_name: Literal['element_type_combination'], id: int
    ) -> M.TypeCombination: ...
    @overload
    async def get(self, resource_name: Literal['item'], id: int) -> M.Item: ...
    @overload
    async def get(
        self, resource_name: Literal['item_category'], id: int
    ) -> M.ItemCategory: ...
    @overload
    async def get(self, resource_name: Literal['gem'], id: int) -> M.Gem: ...
    @overload
    async def get(
        self, resource_name: Literal['gem_category'], id: int
    ) -> M.GemCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['gem_generation_category'], id: int
    ) -> M.GemGenCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_activation_item'], id: int
    ) -> M.SkillActivationItem: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_stone'], id: int
    ) -> M.SkillStone: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_stone_category'], id: int
    ) -> M.SkillStoneCategory: ...
    @overload
    async def get(self, resource_name: Literal['mintmark'], id: int) -> M.Mintmark: ...
    @overload
    async def get(
        self, resource_name: Literal['ability_mintmark'], id: int
    ) -> M.AbilityMintmark: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_mintmark'], id: int
    ) -> M.SkillMintmark: ...
    @overload
    async def get(
        self, resource_name: Literal['universal_mintmark'], id: int
    ) -> M.UniversalMintmark: ...
    @overload
    async def get(
        self, resource_name: Literal['mintmark_class'], id: int
    ) -> M.MintmarkClassCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['mintmark_type'], id: int
    ) -> M.MintmarkTypeCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['mintmark_rarity'], id: int
    ) -> M.MintmarkRarityCategory: ...
    @overload
    async def get(self, resource_name: Literal['pet'], id: int) -> M.Pet: ...
    @overload
    async def get(self, resource_name: Literal['pet_class'], id: int) -> M.PetClass: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_gender'], id: int
    ) -> M.PetGenderCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_vipbuff'], id: int
    ) -> M.PetVipBuffCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_mount_type'], id: int
    ) -> M.PetMountTypeCategory: ...
    @overload
    async def get(self, resource_name: Literal['pet_skin'], id: int) -> M.PetSkin: ...
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
        self, resource_name: Literal['pet_skin_category'], id: int
    ) -> M.PetSkinCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_archive_story_entry'], id: int
    ) -> M.PetArchiveStoryEntry: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_archive_story_book'], id: int
    ) -> M.PetArchiveStoryBook: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_encyclopedia_entry'], id: int
    ) -> M.PetEncyclopediaEntry: ...
    @overload
    async def get(self, resource_name: Literal['nature'], id: int) -> M.Nature: ...
    @overload
    async def get(self, resource_name: Literal['skill'], id: int) -> M.Skill: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_effect_type'], id: int
    ) -> M.SkillEffectType: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_effect_param'], id: int
    ) -> M.SkillEffectParam: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_hide_effect'], id: int
    ) -> M.SkillHideEffect: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_category'], id: int
    ) -> M.SkillCategory: ...
    @overload
    async def get(
        self, resource_name: Literal['skill_effect_type_tag'], id: int
    ) -> M.SkillEffectTypeTag: ...
    @overload
    async def get(
        self, resource_name: Literal['eid_effect'], id: int
    ) -> M.EidEffect: ...
    @overload
    async def get(self, resource_name: Literal['peak_pool'], id: int) -> M.PeakPool: ...
    @overload
    async def get(
        self, resource_name: Literal['peak_expert_pool'], id: int
    ) -> M.PeakExpertPool: ...
    @overload
    async def get(
        self, resource_name: Literal['glossary_entry'], id: int
    ) -> M.GlossaryEntry: ...
    @overload
    async def get(
        self, resource_name: Literal['pet_advance'], id: int
    ) -> M.PetAdvance: ...
    @overload
    async def get(
        self, resource_name: Literal['peak_pool_vote'], id: int
    ) -> M.PeakPoolVote: ...
    @overload
    async def get(
        self, resource_name: Literal['avatar_head'], id: int
    ) -> M.AvatarHead: ...
    @overload
    async def get(
        self, resource_name: Literal['avatar_frame'], id: int
    ) -> M.AvatarFrame: ...
    @overload
    async def get(
        self, resource_name: Literal['namecard_background'], id: int
    ) -> M.NamecardBackground: ...
    @overload
    async def get(
        self, resource_name: Literal['nickname_background'], id: int
    ) -> M.NicknameBackground: ...
    @overload
    async def get(
        self, resource_name: Literal['homepage_background'], id: int
    ) -> M.HomepageBackground: ...
    @overload
    async def get(self, resource_name: Literal['emoji'], id: int) -> M.Emoji: ...
    @overload
    async def get(
        self, resource_name: Literal['peak_season'], id: int
    ) -> M.PeakSeason: ...
    @overload
    async def get(
        self, resource_name: Literal['error_code'], id: int
    ) -> M.ErrorCode: ...
    @overload
    @overload
    async def get(
        self, resource_name: type[T_ModelInstance], id: int
    ) -> T_ModelInstance: ...
    @overload
    async def get(
        self, resource_name: ResourceRef[T_ModelInstance]
    ) -> T_ModelInstance: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['achievement'], page_info: PageInfo
    ) -> PagedResponse[M.Achievement]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['achievement_branch'], page_info: PageInfo
    ) -> PagedResponse[M.AchievementBranch]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['achievement_category'], page_info: PageInfo
    ) -> PagedResponse[M.AchievementCategory]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['achievement_type'], page_info: PageInfo
    ) -> PagedResponse[M.AchievementType]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['title'], page_info: PageInfo
    ) -> PagedResponse[M.Title]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['battle_effect'], page_info: PageInfo
    ) -> PagedResponse[M.BattleEffect]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['battle_effect_type'], page_info: PageInfo
    ) -> PagedResponse[M.BattleEffectCategory]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['pet_effect'], page_info: PageInfo
    ) -> PagedResponse[M.PetEffect]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['pet_effect_group'], page_info: PageInfo
    ) -> PagedResponse[M.PetEffectGroup]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['pet_variation'], page_info: PageInfo
    ) -> PagedResponse[M.VariationEffect]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['energy_bead'], page_info: PageInfo
    ) -> PagedResponse[M.EnergyBead]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['equip'], page_info: PageInfo
    ) -> PagedResponse[M.Equip]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['suit'], page_info: PageInfo
    ) -> PagedResponse[M.Suit]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['equip_type'], page_info: PageInfo
    ) -> PagedResponse[M.EquipType]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['equip_effective_occasion'], page_info: PageInfo
    ) -> PagedResponse[M.EquipEffectiveOccasion]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['soulmark'], page_info: PageInfo
    ) -> PagedResponse[M.Soulmark]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['soulmark_tag'], page_info: PageInfo
    ) -> PagedResponse[M.SoulmarkTagCategory]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['element_type'], page_info: PageInfo
    ) -> PagedResponse[M.ElementType]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['element_type_combination'], page_info: PageInfo
    ) -> PagedResponse[M.TypeCombination]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['item'], page_info: PageInfo
    ) -> PagedResponse[M.Item]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['item_category'], page_info: PageInfo
    ) -> PagedResponse[M.ItemCategory]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['gem'], page_info: PageInfo
    ) -> PagedResponse[M.Gem]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['gem_category'], page_info: PageInfo
    ) -> PagedResponse[M.GemCategory]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['gem_generation_category'], page_info: PageInfo
    ) -> PagedResponse[M.GemGenCategory]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['skill_activation_item'], page_info: PageInfo
    ) -> PagedResponse[M.SkillActivationItem]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['skill_stone'], page_info: PageInfo
    ) -> PagedResponse[M.SkillStone]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['skill_stone_category'], page_info: PageInfo
    ) -> PagedResponse[M.SkillStoneCategory]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['mintmark'], page_info: PageInfo
    ) -> PagedResponse[M.Mintmark]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['ability_mintmark'], page_info: PageInfo
    ) -> PagedResponse[M.AbilityMintmark]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['skill_mintmark'], page_info: PageInfo
    ) -> PagedResponse[M.SkillMintmark]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['universal_mintmark'], page_info: PageInfo
    ) -> PagedResponse[M.UniversalMintmark]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['mintmark_class'], page_info: PageInfo
    ) -> PagedResponse[M.MintmarkClassCategory]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['mintmark_type'], page_info: PageInfo
    ) -> PagedResponse[M.MintmarkTypeCategory]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['mintmark_rarity'], page_info: PageInfo
    ) -> PagedResponse[M.MintmarkRarityCategory]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['pet'], page_info: PageInfo
    ) -> PagedResponse[M.Pet]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['pet_class'], page_info: PageInfo
    ) -> PagedResponse[M.PetClass]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['pet_gender'], page_info: PageInfo
    ) -> PagedResponse[M.PetGenderCategory]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['pet_vipbuff'], page_info: PageInfo
    ) -> PagedResponse[M.PetVipBuffCategory]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['pet_mount_type'], page_info: PageInfo
    ) -> PagedResponse[M.PetMountTypeCategory]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['pet_skin'], page_info: PageInfo
    ) -> PagedResponse[M.PetSkin]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['pet_skin_category'], page_info: PageInfo
    ) -> PagedResponse[M.PetSkinCategory]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['pet_skin_series'], page_info: PageInfo
    ) -> PagedResponse[M.PetSkinSeries]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['pet_skin_series_sub_type'], page_info: PageInfo
    ) -> PagedResponse[M.PetSkinSeriesSubType]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['pet_archive_story_entry'], page_info: PageInfo
    ) -> PagedResponse[M.PetArchiveStoryEntry]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['pet_archive_story_book'], page_info: PageInfo
    ) -> PagedResponse[M.PetArchiveStoryBook]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['pet_encyclopedia_entry'], page_info: PageInfo
    ) -> PagedResponse[M.PetEncyclopediaEntry]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['nature'], page_info: PageInfo
    ) -> PagedResponse[M.Nature]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['skill'], page_info: PageInfo
    ) -> PagedResponse[M.Skill]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['skill_effect_type'], page_info: PageInfo
    ) -> PagedResponse[M.SkillEffectType]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['skill_effect_param'], page_info: PageInfo
    ) -> PagedResponse[M.SkillEffectParam]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['skill_hide_effect'], page_info: PageInfo
    ) -> PagedResponse[M.SkillHideEffect]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['skill_category'], page_info: PageInfo
    ) -> PagedResponse[M.SkillCategory]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['skill_effect_type_tag'], page_info: PageInfo
    ) -> PagedResponse[M.SkillEffectTypeTag]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['eid_effect'], page_info: PageInfo
    ) -> PagedResponse[M.EidEffect]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['peak_pool'], page_info: PageInfo
    ) -> PagedResponse[M.PeakPool]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['peak_expert_pool'], page_info: PageInfo
    ) -> PagedResponse[M.PeakExpertPool]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['glossary_entry'], page_info: PageInfo
    ) -> PagedResponse[M.GlossaryEntry]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['pet_advance'], page_info: PageInfo
    ) -> PagedResponse[M.PetAdvance]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['peak_pool_vote'], page_info: PageInfo
    ) -> PagedResponse[M.PeakPoolVote]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['avatar_head'], page_info: PageInfo
    ) -> PagedResponse[M.AvatarHead]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['avatar_frame'], page_info: PageInfo
    ) -> PagedResponse[M.AvatarFrame]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['namecard_background'], page_info: PageInfo
    ) -> PagedResponse[M.NamecardBackground]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['nickname_background'], page_info: PageInfo
    ) -> PagedResponse[M.NicknameBackground]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['homepage_background'], page_info: PageInfo
    ) -> PagedResponse[M.HomepageBackground]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['emoji'], page_info: PageInfo
    ) -> PagedResponse[M.Emoji]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['error_code'], page_info: PageInfo
    ) -> PagedResponse[M.ErrorCode]: ...
    @overload
    async def paginated_list(
        self, resource_name: Literal['peak_season'], page_info: PageInfo
    ) -> PagedResponse[M.PeakSeason]: ...
    @overload
    async def paginated_list(
        self, resource_name: type[T_ModelInstance], page_info: PageInfo
    ) -> PagedResponse[T_ModelInstance]: ...
    @overload
    async def paginated_list(
        self, resource_name: ResourceRef[T_ModelInstance], page_info: PageInfo
    ) -> PagedResponse[T_ModelInstance]: ...
    @overload
    async def list(
        self, resource_name: Literal['achievement']
    ) -> AsyncGenerator[M.Achievement]: ...
    @overload
    async def list(
        self, resource_name: Literal['achievement_branch']
    ) -> AsyncGenerator[M.AchievementBranch]: ...
    @overload
    async def list(
        self, resource_name: Literal['achievement_category']
    ) -> AsyncGenerator[M.AchievementCategory]: ...
    @overload
    async def list(
        self, resource_name: Literal['achievement_type']
    ) -> AsyncGenerator[M.AchievementType]: ...
    @overload
    async def list(
        self, resource_name: Literal['title']
    ) -> AsyncGenerator[M.Title]: ...
    @overload
    async def list(
        self, resource_name: Literal['battle_effect']
    ) -> AsyncGenerator[M.BattleEffect]: ...
    @overload
    async def list(
        self, resource_name: Literal['battle_effect_type']
    ) -> AsyncGenerator[M.BattleEffectCategory]: ...
    @overload
    async def list(
        self, resource_name: Literal['pet_effect']
    ) -> AsyncGenerator[M.PetEffect]: ...
    @overload
    async def list(
        self, resource_name: Literal['pet_effect_group']
    ) -> AsyncGenerator[M.PetEffectGroup]: ...
    @overload
    async def list(
        self, resource_name: Literal['pet_variation']
    ) -> AsyncGenerator[M.VariationEffect]: ...
    @overload
    async def list(
        self, resource_name: Literal['energy_bead']
    ) -> AsyncGenerator[M.EnergyBead]: ...
    @overload
    async def list(
        self, resource_name: Literal['equip']
    ) -> AsyncGenerator[M.Equip]: ...
    @overload
    async def list(self, resource_name: Literal['suit']) -> AsyncGenerator[M.Suit]: ...
    @overload
    async def list(
        self, resource_name: Literal['equip_type']
    ) -> AsyncGenerator[M.EquipType]: ...
    @overload
    async def list(
        self, resource_name: Literal['equip_effective_occasion']
    ) -> AsyncGenerator[M.EquipEffectiveOccasion]: ...
    @overload
    async def list(
        self, resource_name: Literal['soulmark']
    ) -> AsyncGenerator[M.Soulmark]: ...
    @overload
    async def list(
        self, resource_name: Literal['soulmark_tag']
    ) -> AsyncGenerator[M.SoulmarkTagCategory]: ...
    @overload
    async def list(
        self, resource_name: Literal['element_type']
    ) -> AsyncGenerator[M.ElementType]: ...
    @overload
    async def list(
        self, resource_name: Literal['element_type_combination']
    ) -> AsyncGenerator[M.TypeCombination]: ...
    @overload
    async def list(self, resource_name: Literal['item']) -> AsyncGenerator[M.Item]: ...
    @overload
    async def list(
        self, resource_name: Literal['item_category']
    ) -> AsyncGenerator[M.ItemCategory]: ...
    @overload
    async def list(self, resource_name: Literal['gem']) -> AsyncGenerator[M.Gem]: ...
    @overload
    async def list(
        self, resource_name: Literal['gem_category']
    ) -> AsyncGenerator[M.GemCategory]: ...
    @overload
    async def list(
        self, resource_name: Literal['gem_generation_category']
    ) -> AsyncGenerator[M.GemGenCategory]: ...
    @overload
    async def list(
        self, resource_name: Literal['skill_activation_item']
    ) -> AsyncGenerator[M.SkillActivationItem]: ...
    @overload
    async def list(
        self, resource_name: Literal['skill_stone']
    ) -> AsyncGenerator[M.SkillStone]: ...
    @overload
    async def list(
        self, resource_name: Literal['skill_stone_category']
    ) -> AsyncGenerator[M.SkillStoneCategory]: ...
    @overload
    async def list(
        self, resource_name: Literal['mintmark']
    ) -> AsyncGenerator[M.Mintmark]: ...
    @overload
    async def list(
        self, resource_name: Literal['ability_mintmark']
    ) -> AsyncGenerator[M.AbilityMintmark]: ...
    @overload
    async def list(
        self, resource_name: Literal['skill_mintmark']
    ) -> AsyncGenerator[M.SkillMintmark]: ...
    @overload
    async def list(
        self, resource_name: Literal['universal_mintmark']
    ) -> AsyncGenerator[M.UniversalMintmark]: ...
    @overload
    async def list(
        self, resource_name: Literal['mintmark_class']
    ) -> AsyncGenerator[M.MintmarkClassCategory]: ...
    @overload
    async def list(
        self, resource_name: Literal['mintmark_type']
    ) -> AsyncGenerator[M.MintmarkTypeCategory]: ...
    @overload
    async def list(
        self, resource_name: Literal['mintmark_rarity']
    ) -> AsyncGenerator[M.MintmarkRarityCategory]: ...
    @overload
    async def list(self, resource_name: Literal['pet']) -> AsyncGenerator[M.Pet]: ...
    @overload
    async def list(
        self, resource_name: Literal['pet_class']
    ) -> AsyncGenerator[M.PetClass]: ...
    @overload
    async def list(
        self, resource_name: Literal['pet_gender']
    ) -> AsyncGenerator[M.PetGenderCategory]: ...
    @overload
    async def list(
        self, resource_name: Literal['pet_vipbuff']
    ) -> AsyncGenerator[M.PetVipBuffCategory]: ...
    @overload
    async def list(
        self, resource_name: Literal['pet_mount_type']
    ) -> AsyncGenerator[M.PetMountTypeCategory]: ...
    @overload
    async def list(
        self, resource_name: Literal['pet_skin']
    ) -> AsyncGenerator[M.PetSkin]: ...
    @overload
    async def list(
        self, resource_name: Literal['pet_skin_category']
    ) -> AsyncGenerator[M.PetSkinCategory]: ...
    @overload
    async def list(
        self, resource_name: Literal['pet_skin_series']
    ) -> AsyncGenerator[M.PetSkinSeries]: ...
    @overload
    async def list(
        self, resource_name: Literal['pet_skin_series_sub_type']
    ) -> AsyncGenerator[M.PetSkinSeriesSubType]: ...
    @overload
    async def list(
        self, resource_name: Literal['pet_archive_story_entry']
    ) -> AsyncGenerator[M.PetArchiveStoryEntry]: ...
    @overload
    async def list(
        self, resource_name: Literal['pet_archive_story_book']
    ) -> AsyncGenerator[M.PetArchiveStoryBook]: ...
    @overload
    async def list(
        self, resource_name: Literal['pet_encyclopedia_entry']
    ) -> AsyncGenerator[M.PetEncyclopediaEntry]: ...
    @overload
    async def list(
        self, resource_name: Literal['nature']
    ) -> AsyncGenerator[M.Nature]: ...
    @overload
    async def list(
        self, resource_name: Literal['skill']
    ) -> AsyncGenerator[M.Skill]: ...
    @overload
    async def list(
        self, resource_name: Literal['skill_effect_type']
    ) -> AsyncGenerator[M.SkillEffectType]: ...
    @overload
    async def list(
        self, resource_name: Literal['skill_effect_param']
    ) -> AsyncGenerator[M.SkillEffectParam]: ...
    @overload
    async def list(
        self, resource_name: Literal['skill_hide_effect']
    ) -> AsyncGenerator[M.SkillHideEffect]: ...
    @overload
    async def list(
        self, resource_name: Literal['skill_category']
    ) -> AsyncGenerator[M.SkillCategory]: ...
    @overload
    async def list(
        self, resource_name: Literal['skill_effect_type_tag']
    ) -> AsyncGenerator[M.SkillEffectTypeTag]: ...
    @overload
    async def list(
        self, resource_name: Literal['eid_effect']
    ) -> AsyncGenerator[M.EidEffect]: ...
    @overload
    async def list(
        self, resource_name: Literal['peak_pool']
    ) -> AsyncGenerator[M.PeakPool]: ...
    @overload
    async def list(
        self, resource_name: Literal['peak_expert_pool']
    ) -> AsyncGenerator[M.PeakExpertPool]: ...
    @overload
    async def list(
        self, resource_name: Literal['peak_season']
    ) -> AsyncGenerator[M.PeakSeason]: ...
    @overload
    async def list(
        self, resource_name: Literal['glossary_entry']
    ) -> AsyncGenerator[M.GlossaryEntry]: ...
    @overload
    async def list(
        self, resource_name: Literal['pet_advance']
    ) -> AsyncGenerator[M.PetAdvance]: ...
    @overload
    async def list(
        self, resource_name: Literal['peak_pool_vote']
    ) -> AsyncGenerator[M.PeakPoolVote]: ...
    @overload
    async def list(
        self, resource_name: Literal['avatar_head']
    ) -> AsyncGenerator[M.AvatarHead]: ...
    @overload
    async def list(
        self, resource_name: Literal['avatar_frame']
    ) -> AsyncGenerator[M.AvatarFrame]: ...
    @overload
    async def list(
        self, resource_name: Literal['namecard_background']
    ) -> AsyncGenerator[M.NamecardBackground]: ...
    @overload
    async def list(
        self, resource_name: Literal['nickname_background']
    ) -> AsyncGenerator[M.NicknameBackground]: ...
    @overload
    async def list(
        self, resource_name: Literal['homepage_background']
    ) -> AsyncGenerator[M.HomepageBackground]: ...
    @overload
    async def list(
        self, resource_name: Literal['emoji']
    ) -> AsyncGenerator[M.Emoji]: ...
    @overload
    async def list(
        self, resource_name: Literal['error_code']
    ) -> AsyncGenerator[M.ErrorCode]: ...
    @overload
    async def list(
        self, resource_name: type[T_ModelInstance]
    ) -> AsyncGenerator[T_ModelInstance]: ...
    @overload
    async def list(
        self, resource_name: ResourceRef[T_ModelInstance]
    ) -> AsyncGenerator[T_ModelInstance]: ...
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
        self, resource_name: Literal['title'], name: str
    ) -> NamedData[M.Title]: ...
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
        self, resource_name: Literal['pet_effect'], name: str
    ) -> NamedData[M.PetEffect]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet_effect_group'], name: str
    ) -> NamedData[M.PetEffectGroup]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet_variation'], name: str
    ) -> NamedData[M.VariationEffect]: ...
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
        self, resource_name: Literal['suit'], name: str
    ) -> NamedData[M.Suit]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['equip_type'], name: str
    ) -> NamedData[M.EquipType]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['soulmark_tag'], name: str
    ) -> NamedData[M.SoulmarkTagCategory]: ...
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
        self, resource_name: Literal['item'], name: str
    ) -> NamedData[M.Item]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['item_category'], name: str
    ) -> NamedData[M.ItemCategory]: ...
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
        self, resource_name: Literal['skill_activation_item'], name: str
    ) -> NamedData[M.SkillActivationItem]: ...
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
        self, resource_name: Literal['mintmark'], name: str
    ) -> NamedData[M.Mintmark]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['ability_mintmark'], name: str
    ) -> NamedData[M.AbilityMintmark]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['skill_mintmark'], name: str
    ) -> NamedData[M.SkillMintmark]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['universal_mintmark'], name: str
    ) -> NamedData[M.UniversalMintmark]: ...
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
        self, resource_name: Literal['pet'], name: str
    ) -> NamedData[M.Pet]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet_gender'], name: str
    ) -> NamedData[M.PetGenderCategory]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet_vipbuff'], name: str
    ) -> NamedData[M.PetVipBuffCategory]: ...
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
        self, resource_name: Literal['pet_archive_story_book'], name: str
    ) -> NamedData[M.PetArchiveStoryBook]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['pet_encyclopedia_entry'], name: str
    ) -> NamedData[M.PetEncyclopediaEntry]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['nature'], name: str
    ) -> NamedData[M.Nature]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['skill'], name: str
    ) -> NamedData[M.Skill]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['skill_hide_effect'], name: str
    ) -> NamedData[M.SkillHideEffect]: ...
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
        self, resource_name: Literal['soulmark'], name: str
    ) -> NamedData[M.Soulmark]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['glossary_entry'], name: str
    ) -> NamedData[M.GlossaryEntry]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['error_code'], name: str
    ) -> NamedData[M.ErrorCode]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['avatar_head'], name: str
    ) -> NamedData[M.AvatarHead]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['avatar_frame'], name: str
    ) -> NamedData[M.AvatarFrame]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['namecard_background'], name: str
    ) -> NamedData[M.NamecardBackground]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['nickname_background'], name: str
    ) -> NamedData[M.NicknameBackground]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['homepage_background'], name: str
    ) -> NamedData[M.HomepageBackground]: ...
    @overload
    async def get_by_name(
        self, resource_name: Literal['emoji'], name: str
    ) -> NamedData[M.Emoji]: ...
    @overload
    async def get_by_name(
        self, resource_name: type[T_NamedModelInstance], name: str
    ) -> NamedData[T_NamedModelInstance]: ...
    @overload
    async def get_by_name(
        self, resource_name: ResourceRef[T_NamedModelInstance], name: str
    ) -> NamedData[T_NamedModelInstance]: ...
