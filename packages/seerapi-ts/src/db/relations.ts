import { defineRelations } from "drizzle-orm";
import * as schema from "./schema.js";

export const relations = defineRelations(schema, (r) => ({
	petBaseStats: {
		pet: r.one.pet({
			from: r.petBaseStats.id,
			to: r.pet.id,
			alias: "petBaseStats_id_pet_id"
		}),
		pets: r.many.pet({
			alias: "pet_baseStatsId_petBaseStats_id"
		}),
	},
	pet: {
		petBaseStats: r.many.petBaseStats({
			alias: "petBaseStats_id_pet_id"
		}),
		petYieldingEvs: r.many.petYieldingEv({
			alias: "petYieldingEv_id_pet_id"
		}),
		petDiyStatsRanges: r.many.petDiyStatsRange({
			alias: "petDiyStatsRange_id_pet_id"
		}),
		peakPoolVote: r.one.peakPoolVote({
			from: r.pet.peakPoolVoteId,
			to: r.peakPoolVote.id
		}),
		peakExpertPool: r.one.peakExpertPool({
			from: r.pet.peakExpertPoolId,
			to: r.peakExpertPool.id
		}),
		peakPool: r.one.peakPool({
			from: r.pet.peakPoolId,
			to: r.peakPool.id
		}),
		petDiyStatsRange: r.one.petDiyStatsRange({
			from: r.pet.diyStatsId,
			to: r.petDiyStatsRange.id,
			alias: "pet_diyStatsId_petDiyStatsRange_id"
		}),
		petMountType: r.one.petMountType({
			from: r.pet.mountTypeId,
			to: r.petMountType.id
		}),
		petVipbuff: r.one.petVipbuff({
			from: r.pet.vipbuffId,
			to: r.petVipbuff.id
		}),
		petYieldingEv: r.one.petYieldingEv({
			from: r.pet.yieldingEvId,
			to: r.petYieldingEv.id,
			alias: "pet_yieldingEvId_petYieldingEv_id"
		}),
		petBaseStat: r.one.petBaseStats({
			from: r.pet.baseStatsId,
			to: r.petBaseStats.id,
			alias: "pet_baseStatsId_petBaseStats_id"
		}),
		petClass: r.one.petClass({
			from: r.pet.petClassId,
			to: r.petClass.id
		}),
		petGender: r.one.petGender({
			from: r.pet.genderId,
			to: r.petGender.id
		}),
		elementTypeCombination: r.one.elementTypeCombination({
			from: r.pet.typeId,
			to: r.elementTypeCombination.id
		}),
		glossaryEntries: r.many.glossaryEntry(),
		petEncyclopediaEntries: r.many.petEncyclopediaEntry(),
		petArchiveStoryBooks: r.many.petArchiveStoryBook(),
		petSkins: r.many.petSkin(),
		mintmarks: r.many.mintmark(),
		suitBonuses: r.many.suitBonus(),
		soulmarksViaPetAdvance: r.many.soulmark({
			alias: "soulmark_id_pet_id_via_petAdvance"
		}),
		soulmarksViaPetsoulmarklink: r.many.soulmark({
			alias: "soulmark_id_pet_id_via_petsoulmarklink"
		}),
		skillinpetorms: r.many.skillinpetorm(),
	},
	petYieldingEv: {
		pet: r.one.pet({
			from: r.petYieldingEv.id,
			to: r.pet.id,
			alias: "petYieldingEv_id_pet_id"
		}),
		pets: r.many.pet({
			alias: "pet_yieldingEvId_petYieldingEv_id"
		}),
	},
	petDiyStatsRange: {
		pet: r.one.pet({
			from: r.petDiyStatsRange.id,
			to: r.pet.id,
			alias: "petDiyStatsRange_id_pet_id"
		}),
		pets: r.many.pet({
			alias: "pet_diyStatsId_petDiyStatsRange_id"
		}),
	},
	peakPoolVote: {
		pets: r.many.pet(),
	},
	peakExpertPool: {
		pets: r.many.pet(),
	},
	peakPool: {
		pets: r.many.pet(),
	},
	petMountType: {
		pets: r.many.pet(),
	},
	petVipbuff: {
		pets: r.many.pet(),
	},
	petClass: {
		pets: r.many.pet(),
	},
	petGender: {
		pets: r.many.pet(),
	},
	elementTypeCombination: {
		pets: r.many.pet(),
		skillStoneCategories: r.many.skillStoneCategory(),
		skills: r.many.skill(),
	},
	eidEffectInUse: {
		eidEffect: r.one.eidEffect({
			from: r.eidEffectInUse.eid,
			to: r.eidEffect.id
		}),
		petVariations: r.many.petVariation(),
		petEffectGroups: r.many.petEffectGroup(),
		items: r.many.item({
			from: r.eidEffectInUse.id.through(r.energyBead.effectInUseId),
			to: r.item.id.through(r.energyBead.id)
		}),
		equipBonusAttrs: r.many.equipBonusAttr(),
		suitBonuses: r.many.suitBonus(),
		soulmarks: r.many.soulmark(),
	},
	eidEffect: {
		eidEffectInUses: r.many.eidEffectInUse(),
	},
	skillEffectInUse: {
		skillEffectType: r.one.skillEffectType({
			from: r.skillEffectInUse.effectId,
			to: r.skillEffectType.id
		}),
		gemsSkillEffectInUseId: r.many.gem({
			alias: "gem_skillEffectInUseId_skillEffectInUse_id"
		}),
		gemsViaGemeffectlink: r.many.gem({
			from: r.skillEffectInUse.id.through(r.gemeffectlink.skillEffectInUseId),
			to: r.gem.id.through(r.gemeffectlink.gemId),
			alias: "skillEffectInUse_id_gem_id_via_gemeffectlink"
		}),
		skillsViaSkilleffectlink: r.many.skill({
			from: r.skillEffectInUse.id.through(r.skilleffectlink.effectInUseId),
			to: r.skill.id.through(r.skilleffectlink.skillId),
			alias: "skillEffectInUse_id_skill_id_via_skilleffectlink"
		}),
		skillsViaSkillfriendskilleffectlink: r.many.skill({
			from: r.skillEffectInUse.id.through(r.skillfriendskilleffectlink.effectInUseId),
			to: r.skill.id.through(r.skillfriendskilleffectlink.skillId),
			alias: "skillEffectInUse_id_skill_id_via_skillfriendskilleffectlink"
		}),
		skillStoneEffects: r.many.skillStoneEffect({
			from: r.skillEffectInUse.id.through(r.skillstoneeffectlink.effectInUseId),
			to: r.skillStoneEffect.id.through(r.skillstoneeffectlink.skillStoneEffectId)
		}),
	},
	skillEffectType: {
		skillEffectInUses: r.many.skillEffectInUse(),
		skillEffectTypeTags: r.many.skillEffectTypeTag(),
		skillEffectParamInTypes: r.many.skillEffectParamInType(),
	},
	achievementBranch: {
		achievementType: r.one.achievementType({
			from: r.achievementBranch.typeId,
			to: r.achievementType.id
		}),
		achievements: r.many.achievement(),
	},
	achievementType: {
		achievementBranches: r.many.achievementBranch(),
		achievements: r.many.achievement(),
	},
	battleEffectType: {
		battleEffects: r.many.battleEffect({
			from: r.battleEffectType.id.through(r.battleeffectcategorylink.typeId),
			to: r.battleEffect.id.through(r.battleeffectcategorylink.battleEffectId)
		}),
	},
	battleEffect: {
		battleEffectTypes: r.many.battleEffectType(),
	},
	glossaryEntry: {
		pets: r.many.pet({
			from: r.glossaryEntry.id.through(r.petglossaryentrylink.glossaryEntryId),
			to: r.pet.id.through(r.petglossaryentrylink.petId)
		}),
	},
	item: {
		itemCategory: r.one.itemCategory({
			from: r.item.categoryId,
			to: r.itemCategory.id
		}),
		eidEffectInUses: r.many.eidEffectInUse(),
		gems: r.many.gem(),
		skillActivationItems: r.many.skillActivationItem(),
		equips: r.many.equip(),
		skillStoneCategories: r.many.skillStoneCategory({
			from: r.item.id.through(r.skillStone.itemId),
			to: r.skillStoneCategory.id.through(r.skillStone.categoryId)
		}),
	},
	itemCategory: {
		items: r.many.item(),
	},
	gemCategory: {
		gemGenerationCategory: r.one.gemGenerationCategory({
			from: r.gemCategory.generationId,
			to: r.gemGenerationCategory.id
		}),
		gems: r.many.gem(),
	},
	gemGenerationCategory: {
		gemCategories: r.many.gemCategory(),
		gems: r.many.gem(),
	},
	petSkinSeriesSubType: {
		petSkinSery: r.one.petSkinSeries({
			from: r.petSkinSeriesSubType.seriesId,
			to: r.petSkinSeries.id
		}),
		petSkins: r.many.petSkin(),
	},
	petSkinSeries: {
		petSkinSeriesSubTypes: r.many.petSkinSeriesSubType(),
		petSkins: r.many.petSkin(),
	},
	petEncyclopediaEntry: {
		pet: r.one.pet({
			from: r.petEncyclopediaEntry.id,
			to: r.pet.id
		}),
	},
	petArchiveStoryBook: {
		pets: r.many.pet({
			from: r.petArchiveStoryBook.id.through(r.petArchiveStoryEntry.bookId),
			to: r.pet.id.through(r.petArchiveStoryEntry.petId)
		}),
	},
	skillEffectTypeTag: {
		skillEffectTypes: r.many.skillEffectType({
			from: r.skillEffectTypeTag.id.through(r.skilleffecttypetaglink.tagId),
			to: r.skillEffectType.id.through(r.skilleffecttypetaglink.effectId)
		}),
	},
	skillEffectParamInType: {
		skillEffectParam: r.one.skillEffectParam({
			from: r.skillEffectParamInType.paramId,
			to: r.skillEffectParam.id
		}),
		skillEffectTypes: r.many.skillEffectType({
			from: r.skillEffectParamInType.id.through(r.effectparamlink.paramInTypeId),
			to: r.skillEffectType.id.through(r.effectparamlink.effectId)
		}),
	},
	skillEffectParam: {
		skillEffectParamInTypes: r.many.skillEffectParamInType(),
	},
	mintmarkRarity: {
		mintmarkTypes: r.many.mintmarkType({
			from: r.mintmarkRarity.id.through(r.mintmark.rarityId),
			to: r.mintmarkType.id.through(r.mintmark.typeId)
		}),
	},
	mintmarkType: {
		mintmarkRarities: r.many.mintmarkRarity(),
	},
	natureAttr: {
		nature: r.one.nature({
			from: r.natureAttr.id,
			to: r.nature.id
		}),
	},
	nature: {
		natureAttrs: r.many.natureAttr(),
	},
	achievement: {
		achievement: r.one.achievement({
			from: r.achievement.nextLevelAchievementId,
			to: r.achievement.id,
			alias: "achievement_nextLevelAchievementId_achievement_id"
		}),
		achievements: r.many.achievement({
			alias: "achievement_nextLevelAchievementId_achievement_id"
		}),
		achievementBranch: r.one.achievementBranch({
			from: r.achievement.branchId,
			to: r.achievementBranch.id
		}),
		achievementType: r.one.achievementType({
			from: r.achievement.typeId,
			to: r.achievementType.id
		}),
		titleParts: r.many.titlePart(),
	},
	petVariation: {
		eidEffectInUse: r.one.eidEffectInUse({
			from: r.petVariation.effectInUseId,
			to: r.eidEffectInUse.id
		}),
	},
	petEffectGroup: {
		eidEffectInUses: r.many.eidEffectInUse({
			from: r.petEffectGroup.id.through(r.petEffect.effectGroupId),
			to: r.eidEffectInUse.id.through(r.petEffect.effectInUseId)
		}),
	},
	equipBonusAttr: {
		eidEffectInUses: r.many.eidEffectInUse({
			from: r.equipBonusAttr.id.through(r.equipBonus.attributeId),
			to: r.eidEffectInUse.id.through(r.equipBonus.effectInUseId)
		}),
	},
	suitBonus: {
		suitBonusAttr: r.one.suitBonusAttr({
			from: r.suitBonus.attributeId,
			to: r.suitBonusAttr.id
		}),
		eidEffectInUse: r.one.eidEffectInUse({
			from: r.suitBonus.effectInUseId,
			to: r.eidEffectInUse.id
		}),
		suit: r.one.suit({
			from: r.suitBonus.id,
			to: r.suit.id
		}),
		pets: r.many.pet({
			from: r.suitBonus.id.through(r.petsuitlink.suitId),
			to: r.pet.id.through(r.petsuitlink.petId)
		}),
	},
	suitBonusAttr: {
		suitBonuses: r.many.suitBonus(),
	},
	suit: {
		suitBonuses: r.many.suitBonus(),
		equips: r.many.equip(),
	},
	gem: {
		skillEffectInUse: r.one.skillEffectInUse({
			from: r.gem.skillEffectInUseId,
			to: r.skillEffectInUse.id,
			alias: "gem_skillEffectInUseId_skillEffectInUse_id"
		}),
		gemCategory: r.one.gemCategory({
			from: r.gem.categoryId,
			to: r.gemCategory.id
		}),
		gem: r.one.gem({
			from: r.gem.nextLevelGemId,
			to: r.gem.id,
			alias: "gem_nextLevelGemId_gem_id"
		}),
		gems: r.many.gem({
			alias: "gem_nextLevelGemId_gem_id"
		}),
		gemGenerationCategory: r.one.gemGenerationCategory({
			from: r.gem.generationId,
			to: r.gemGenerationCategory.id
		}),
		item: r.one.item({
			from: r.gem.id,
			to: r.item.id
		}),
		skillEffectInUses: r.many.skillEffectInUse({
			alias: "skillEffectInUse_id_gem_id_via_gemeffectlink"
		}),
		gemGen1Parts: r.many.gemGen1Part(),
		gemGen2Parts: r.many.gemGen2Part(),
	},
	petSkin: {
		petSkinSeriesSubType: r.one.petSkinSeriesSubType({
			from: r.petSkin.subTypeId,
			to: r.petSkinSeriesSubType.id
		}),
		petSkinSery: r.one.petSkinSeries({
			from: r.petSkin.seriesId,
			to: r.petSkinSeries.id
		}),
		petSkinCategory: r.one.petSkinCategory({
			from: r.petSkin.categoryId,
			to: r.petSkinCategory.id
		}),
		pet: r.one.pet({
			from: r.petSkin.petId,
			to: r.pet.id
		}),
	},
	petSkinCategory: {
		petSkins: r.many.petSkin(),
	},
	soulmark: {
		eidEffectInUses: r.many.eidEffectInUse({
			from: r.soulmark.id.through(r.soulmark.intensifiedToId),
			to: r.eidEffectInUse.id.through(r.soulmark.effectInUseId)
		}),
		petsViaPetAdvance: r.many.pet({
			from: r.soulmark.id.through(r.petAdvance.soulmarkId),
			to: r.pet.id.through(r.petAdvance.petId),
			alias: "soulmark_id_pet_id_via_petAdvance"
		}),
		petsViaPetsoulmarklink: r.many.pet({
			from: r.soulmark.id.through(r.petsoulmarklink.soulmarkId),
			to: r.pet.id.through(r.petsoulmarklink.petId),
			alias: "soulmark_id_pet_id_via_petsoulmarklink"
		}),
		soulmarkTags: r.many.soulmarkTag(),
	},
	skillActivationItem: {
		item: r.one.item({
			from: r.skillActivationItem.id,
			to: r.item.id
		}),
		skillinpetorms: r.many.skillinpetorm(),
	},
	skillStoneCategory: {
		elementTypeCombination: r.one.elementTypeCombination({
			from: r.skillStoneCategory.typeId,
			to: r.elementTypeCombination.id
		}),
		items: r.many.item(),
	},
	mintmark: {
		pets: r.many.pet({
			from: r.mintmark.id.through(r.petmintmarklink.mintmarkId),
			to: r.pet.id.through(r.petmintmarklink.petId)
		}),
		mintmarkMaxAttrs: r.many.mintmarkMaxAttr(),
		skillMintmarkParts: r.many.skillMintmarkPart(),
		universalMintmarkParts: r.many.universalMintmarkPart(),
		skills: r.many.skill({
			from: r.mintmark.id.through(r.skillmintmarklink.mintmarkId),
			to: r.skill.id.through(r.skillmintmarklink.skillId)
		}),
	},
	mintmarkMaxAttr: {
		mintmarks: r.many.mintmark({
			from: r.mintmarkMaxAttr.id.through(r.abilityMintmarkPart.maxAttrValueId),
			to: r.mintmark.id.through(r.abilityMintmarkPart.mintmarkId)
		}),
		universalMintmarkParts: r.many.universalMintmarkPart(),
	},
	skillMintmarkPart: {
		mintmark: r.one.mintmark({
			from: r.skillMintmarkPart.mintmarkId,
			to: r.mintmark.id
		}),
	},
	universalMintmarkPart: {
		mintmarkExtraAttr: r.one.mintmarkExtraAttr({
			from: r.universalMintmarkPart.extraAttrValueId,
			to: r.mintmarkExtraAttr.id
		}),
		mintmarkMaxAttr: r.one.mintmarkMaxAttr({
			from: r.universalMintmarkPart.maxAttrValueId,
			to: r.mintmarkMaxAttr.id
		}),
		mintmarkBaseAttr: r.one.mintmarkBaseAttr({
			from: r.universalMintmarkPart.baseAttrValueId,
			to: r.mintmarkBaseAttr.id
		}),
		mintmarkClass: r.one.mintmarkClass({
			from: r.universalMintmarkPart.mintmarkClassId,
			to: r.mintmarkClass.id
		}),
		mintmark: r.one.mintmark({
			from: r.universalMintmarkPart.mintmarkId,
			to: r.mintmark.id
		}),
	},
	mintmarkExtraAttr: {
		universalMintmarkParts: r.many.universalMintmarkPart(),
	},
	mintmarkBaseAttr: {
		universalMintmarkParts: r.many.universalMintmarkPart(),
	},
	mintmarkClass: {
		universalMintmarkParts: r.many.universalMintmarkPart(),
	},
	titlePart: {
		achievement: r.one.achievement({
			from: r.titlePart.achievementId,
			to: r.achievement.id
		}),
		titleAttrBonuses: r.many.titleAttrBonus(),
	},
	energyBeadBuffAttr: {
		energyBead: r.one.energyBead({
			from: r.energyBeadBuffAttr.id,
			to: r.energyBead.id
		}),
	},
	energyBead: {
		energyBeadBuffAttrs: r.many.energyBeadBuffAttr(),
	},
	equip: {
		equipEffectiveOccasion: r.one.equipEffectiveOccasion({
			from: r.equip.occasionId,
			to: r.equipEffectiveOccasion.id
		}),
		equipBonus: r.one.equipBonus({
			from: r.equip.bonusId,
			to: r.equipBonus.id
		}),
		suit: r.one.suit({
			from: r.equip.suitId,
			to: r.suit.id
		}),
		equipType: r.one.equipType({
			from: r.equip.partTypeId,
			to: r.equipType.id
		}),
		item: r.one.item({
			from: r.equip.id,
			to: r.item.id
		}),
	},
	equipEffectiveOccasion: {
		equips: r.many.equip(),
	},
	equipBonus: {
		equips: r.many.equip(),
	},
	equipType: {
		equips: r.many.equip(),
	},
	gemGen1Part: {
		gem: r.one.gem({
			from: r.gemGen1Part.id,
			to: r.gem.id
		}),
	},
	gemGen2Part: {
		gem: r.one.gem({
			from: r.gemGen2Part.id,
			to: r.gem.id
		}),
	},
	soulmarkTag: {
		soulmarks: r.many.soulmark({
			from: r.soulmarkTag.id.through(r.soulmarktaglink.tagId),
			to: r.soulmark.id.through(r.soulmarktaglink.soulmarkId)
		}),
	},
	titleAttrBonus: {
		titlePart: r.one.titlePart({
			from: r.titleAttrBonus.id,
			to: r.titlePart.id
		}),
	},
	petAdvanceBaseStats: {
		petAdvance: r.one.petAdvance({
			from: r.petAdvanceBaseStats.id,
			to: r.petAdvance.id
		}),
	},
	petAdvance: {
		petAdvanceBaseStats: r.many.petAdvanceBaseStats(),
		skills: r.many.skill(),
	},
	skill: {
		petAdvance: r.one.petAdvance({
			from: r.skill.advanceId,
			to: r.petAdvance.id
		}),
		skillHideEffect: r.one.skillHideEffect({
			from: r.skill.hideEffectId,
			to: r.skillHideEffect.id
		}),
		elementTypeCombination: r.one.elementTypeCombination({
			from: r.skill.typeId,
			to: r.elementTypeCombination.id
		}),
		skillCategory: r.one.skillCategory({
			from: r.skill.categoryId,
			to: r.skillCategory.id
		}),
		skillinpetorms: r.many.skillinpetorm(),
		skillEffectInUsesViaSkilleffectlink: r.many.skillEffectInUse({
			alias: "skillEffectInUse_id_skill_id_via_skilleffectlink"
		}),
		skillEffectInUsesViaSkillfriendskilleffectlink: r.many.skillEffectInUse({
			alias: "skillEffectInUse_id_skill_id_via_skillfriendskilleffectlink"
		}),
		mintmarks: r.many.mintmark(),
	},
	skillHideEffect: {
		skills: r.many.skill(),
	},
	skillCategory: {
		skills: r.many.skill(),
	},
	skillStoneEffect: {
		skillStone: r.one.skillStone({
			from: r.skillStoneEffect.skillStoneId,
			to: r.skillStone.id
		}),
		skillEffectInUses: r.many.skillEffectInUse(),
	},
	skillStone: {
		skillStoneEffects: r.many.skillStoneEffect(),
	},
	skillinpetorm: {
		skillActivationItem: r.one.skillActivationItem({
			from: r.skillinpetorm.skillActivationItemId,
			to: r.skillActivationItem.id
		}),
		pet: r.one.pet({
			from: r.skillinpetorm.petId,
			to: r.pet.id
		}),
		skill: r.one.skill({
			from: r.skillinpetorm.skillId,
			to: r.skill.id
		}),
	},
}))