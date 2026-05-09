import { sqliteTable, foreignKey, type AnySQLiteColumn, primaryKey, integer, numeric, text, customType, real } from "drizzle-orm/sqlite-core"
import { sql } from "drizzle-orm"

export const eidEffect = sqliteTable("eid_effect", {
	id: integer().primaryKey(),
	argsNum: integer("args_num").notNull(),
});

export const achievementType = sqliteTable("achievement_type", {
	id: integer().primaryKey(),
	name: text().notNull(),
	pointTotal: integer("point_total").notNull(),
});

export const battleEffect = sqliteTable("battle_effect", {
	id: integer().primaryKey(),
	name: text().notNull(),
	desc: text().notNull(),
});

export const battleEffectType = sqliteTable("battle_effect_type", {
	id: integer().primaryKey(),
	name: text().notNull(),
});

export const avatarHead = sqliteTable("avatar_head", {
	id: integer().notNull(),
	name: text().notNull(),
	desc: text().notNull(),
	iconId: integer("icon_id").notNull(),
},
(table) => [primaryKey({ columns: [table.id, table.iconId], name: "avatar_head_pk"}),
]);

export const avatarFrame = sqliteTable("avatar_frame", {
	id: integer().notNull(),
	name: text().notNull(),
	desc: text().notNull(),
	iconId: integer("icon_id").notNull(),
},
(table) => [primaryKey({ columns: [table.id, table.iconId], name: "avatar_frame_pk"}),
]);

export const namecardBackground = sqliteTable("namecard_background", {
	id: integer().notNull(),
	name: text().notNull(),
	desc: text().notNull(),
	iconId: integer("icon_id").notNull(),
},
(table) => [primaryKey({ columns: [table.id, table.iconId], name: "namecard_background_pk"}),
]);

export const nicknameBackground = sqliteTable("nickname_background", {
	id: integer().notNull(),
	name: text().notNull(),
	desc: text().notNull(),
	iconId: integer("icon_id").notNull(),
},
(table) => [primaryKey({ columns: [table.id, table.iconId], name: "nickname_background_pk"}),
]);

export const homepageBackground = sqliteTable("homepage_background", {
	id: integer().notNull(),
	name: text().notNull(),
	desc: text().notNull(),
	iconId: integer("icon_id").notNull(),
},
(table) => [primaryKey({ columns: [table.id, table.iconId], name: "homepage_background_pk"}),
]);

export const emoji = sqliteTable("emoji", {
	id: integer().notNull(),
	name: text().notNull(),
	desc: text().notNull(),
	iconId: integer("icon_id").notNull(),
},
(table) => [primaryKey({ columns: [table.id, table.iconId], name: "emoji_pk"}),
]);

export const petEffectGroup = sqliteTable("pet_effect_group", {
	id: integer().primaryKey(),
	name: text().notNull(),
});

export const elementType = sqliteTable("element_type", {
	id: integer().primaryKey(),
	name: text().notNull(),
	nameEn: text("name_en").notNull(),
});

export const errorCode = sqliteTable("error_code", {
	id: integer().primaryKey(),
	name: text().notNull(),
	message: text().notNull(),
});

export const glossaryEntry = sqliteTable("glossary_entry", {
	id: integer().primaryKey(),
	name: text().notNull(),
	desc: text().notNull(),
	kind: integer().notNull(),
});

export const itemCategory = sqliteTable("item_category", {
	id: integer().primaryKey(),
	name: text().notNull(),
	max: integer().notNull(),
});

export const suitBonusAttr = sqliteTable("suit_bonus_attr", {
	id: integer().primaryKey(),
	atk: numeric().notNull(),
	def: numeric().notNull(),
	spAtk: numeric("sp_atk").notNull(),
	spDef: numeric("sp_def").notNull(),
	spd: numeric().notNull(),
	hp: numeric().notNull(),
	percent: numeric().notNull(),
	total: numeric().notNull(),
});

export const equipBonusAttr = sqliteTable("equip_bonus_attr", {
	id: integer().primaryKey(),
	atk: numeric().notNull(),
	def: numeric().notNull(),
	spAtk: numeric("sp_atk").notNull(),
	spDef: numeric("sp_def").notNull(),
	spd: numeric().notNull(),
	hp: numeric().notNull(),
	percent: numeric().notNull(),
	total: numeric().notNull(),
});

export const suit = sqliteTable("suit", {
	id: integer().primaryKey(),
	name: text().notNull(),
	transform: numeric().notNull(),
	tranSpeed: real("tran_speed"),
	suitDesc: text("suit_desc").notNull(),
});

export const equipType = sqliteTable("equip_type", {
	id: integer().primaryKey(),
	name: text().notNull(),
});

export const equipEffectiveOccasion = sqliteTable("equip_effective_occasion", {
	id: integer().primaryKey(),
	description: text().notNull(),
});

export const gemGenerationCategory = sqliteTable("gem_generation_category", {
	id: integer().primaryKey(),
});

export const petBaseStats = sqliteTable("pet_base_stats", {
	atk: numeric().notNull(),
	def: numeric().notNull(),
	spAtk: numeric("sp_atk").notNull(),
	spDef: numeric("sp_def").notNull(),
	spd: numeric().notNull(),
	hp: numeric().notNull(),
	percent: numeric().notNull(),
	id: integer().primaryKey().references((): AnySQLiteColumn => pet.id),
	total: numeric().notNull(),
});

export const petYieldingEv = sqliteTable("pet_yielding_ev", {
	atk: numeric().notNull(),
	def: numeric().notNull(),
	spAtk: numeric("sp_atk").notNull(),
	spDef: numeric("sp_def").notNull(),
	spd: numeric().notNull(),
	hp: numeric().notNull(),
	percent: numeric().notNull(),
	id: integer().primaryKey().references((): AnySQLiteColumn => pet.id),
	total: numeric().notNull(),
});

export const petDiyStatsRange = sqliteTable("pet_diy_stats_range", {
	id: integer().primaryKey().references((): AnySQLiteColumn => pet.id),
	atkMin: integer("atk_min").notNull(),
	defMin: integer("def_min").notNull(),
	spAtkMin: integer("sp_atk_min").notNull(),
	spDefMin: integer("sp_def_min").notNull(),
	spdMin: integer("spd_min").notNull(),
	hpMin: integer("hp_min").notNull(),
	atkMax: integer("atk_max").notNull(),
	defMax: integer("def_max").notNull(),
	spAtkMax: integer("sp_atk_max").notNull(),
	spDefMax: integer("sp_def_max").notNull(),
	spdMax: integer("spd_max").notNull(),
	hpMax: integer("hp_max").notNull(),
});

export const pet = sqliteTable("pet", {
	id: integer().primaryKey(),
	name: text().notNull(),
	yieldingExp: integer("yielding_exp").notNull(),
	catchRate: integer("catch_rate").notNull(),
	evolvingLv: integer("evolving_lv"),
	releaseable: numeric().notNull(),
	fusionMaster: numeric("fusion_master").notNull(),
	fusionSub: numeric("fusion_sub").notNull(),
	hasResistance: numeric("has_resistance").notNull(),
	resourceId: integer("resource_id").notNull(),
	enemyResourceId: integer("enemy_resource_id"),
	typeId: integer("type_id").notNull().references(() => elementTypeCombination.id),
	genderId: integer("gender_id").notNull().references(() => petGender.id),
	petClassId: integer("pet_class_id").references(() => petClass.id),
	baseStatsId: integer("base_stats_id").notNull().references((): AnySQLiteColumn => petBaseStats.id),
	yieldingEvId: integer("yielding_ev_id").notNull().references((): AnySQLiteColumn => petYieldingEv.id),
	vipbuffId: integer("vipbuff_id").references(() => petVipbuff.id),
	mountTypeId: integer("mount_type_id").references(() => petMountType.id),
	diyStatsId: integer("diy_stats_id").references((): AnySQLiteColumn => petDiyStatsRange.id),
	peakPoolId: integer("peak_pool_id").references(() => peakPool.id),
	peakExpertPoolId: integer("peak_expert_pool_id").references(() => peakExpertPool.id),
	peakPoolVoteId: integer("peak_pool_vote_id").references(() => peakPoolVote.id),
});

export const petClass = sqliteTable("pet_class", {
	id: integer().primaryKey(),
	isVariantPet: numeric("is_variant_pet").notNull(),
	isDarkPet: numeric("is_dark_pet").notNull(),
	isShinePet: numeric("is_shine_pet").notNull(),
	isRarePet: numeric("is_rare_pet").notNull(),
	isBreedingPet: numeric("is_breeding_pet").notNull(),
	isFusionPet: numeric("is_fusion_pet").notNull(),
});

export const petGender = sqliteTable("pet_gender", {
	id: integer().primaryKey(),
	name: text().notNull(),
	description: text().notNull(),
});

export const petVipbuff = sqliteTable("pet_vipbuff", {
	id: integer().primaryKey(),
	name: text().notNull(),
	description: text().notNull(),
});

export const petMountType = sqliteTable("pet_mount_type", {
	id: integer().primaryKey(),
	name: text().notNull(),
	description: text().notNull(),
});

export const petSkinSeries = sqliteTable("pet_skin_series", {
	id: integer().primaryKey(),
	name: text().notNull(),
});

export const petSkinCategory = sqliteTable("pet_skin_category", {
	id: integer().primaryKey(),
});

export const petArchiveStoryBook = sqliteTable("pet_archive_story_book", {
	id: integer().primaryKey(),
	name: text().notNull(),
});

export const soulmarkTag = sqliteTable("soulmark_tag", {
	id: integer().primaryKey(),
	name: text().notNull(),
});

export const skillEffectParam = sqliteTable("skill_effect_param", {
	id: integer().primaryKey(),
	infos: customType({ dataType: () => 'JSON' })(),
});

export const skillEffectType = sqliteTable("skill_effect_type", {
	id: integer().primaryKey(),
	argsNum: integer("args_num").notNull(),
	info: text().notNull(),
	infoFormattingAdjustment: text("info_formatting_adjustment"),
	analyzeInfo: text("analyze_info").notNull(),
	pveEffective: numeric("pve_effective").notNull(),
});

export const skillCategory = sqliteTable("skill_category", {
	id: integer().primaryKey(),
	name: text().notNull(),
});

export const skillHideEffect = sqliteTable("skill_hide_effect", {
	id: integer().primaryKey(),
	name: text().notNull(),
	description: text().notNull(),
});

export const skillEffectTypeTag = sqliteTable("skill_effect_type_tag", {
	id: integer().primaryKey(),
	name: text().notNull(),
});

export const apiMetadata = sqliteTable("api_metadata", {
	apiUrl: text("api_url").notNull(),
	apiVersion: text("api_version").notNull(),
	generatorName: text("generator_name").notNull(),
	generatorVersion: text("generator_version").notNull(),
	generateTime: numeric("generate_time").notNull(),
	dataSource: text("data_source").notNull(),
	dataVersion: text("data_version").notNull(),
	patchSource: text("patch_source").notNull(),
	patchVersion: text("patch_version").notNull(),
	id: integer().primaryKey(),
});

export const mintmarkMaxAttr = sqliteTable("mintmark_max_attr", {
	id: integer().primaryKey(),
	atk: numeric().notNull(),
	def: numeric().notNull(),
	spAtk: numeric("sp_atk").notNull(),
	spDef: numeric("sp_def").notNull(),
	spd: numeric().notNull(),
	hp: numeric().notNull(),
	percent: numeric().notNull(),
	total: numeric().notNull(),
});

export const mintmarkBaseAttr = sqliteTable("mintmark_base_attr", {
	id: integer().primaryKey(),
	atk: numeric().notNull(),
	def: numeric().notNull(),
	spAtk: numeric("sp_atk").notNull(),
	spDef: numeric("sp_def").notNull(),
	spd: numeric().notNull(),
	hp: numeric().notNull(),
	percent: numeric().notNull(),
	total: numeric().notNull(),
});

export const mintmarkExtraAttr = sqliteTable("mintmark_extra_attr", {
	id: integer().primaryKey(),
	atk: numeric().notNull(),
	def: numeric().notNull(),
	spAtk: numeric("sp_atk").notNull(),
	spDef: numeric("sp_def").notNull(),
	spd: numeric().notNull(),
	hp: numeric().notNull(),
	percent: numeric().notNull(),
	total: numeric().notNull(),
});

export const mintmarkRarity = sqliteTable("mintmark_rarity", {
	id: integer().primaryKey(),
});

export const mintmarkType = sqliteTable("mintmark_type", {
	id: integer().primaryKey(),
	name: text().notNull(),
});

export const mintmarkClass = sqliteTable("mintmark_class", {
	id: integer().primaryKey(),
	name: text().notNull(),
});

export const nature = sqliteTable("nature", {
	id: integer().primaryKey(),
	name: text().notNull(),
	des: text().notNull(),
	des2: text().notNull(),
});

export const peakSeason = sqliteTable("peak_season", {
	id: integer().primaryKey(),
	startTime: numeric("start_time").notNull(),
	endTime: numeric("end_time").notNull(),
});

export const peakPool = sqliteTable("peak_pool", {
	id: integer().primaryKey(),
	count: integer().notNull(),
	startTime: numeric("start_time").notNull(),
	endTime: numeric("end_time").notNull(),
});

export const peakExpertPool = sqliteTable("peak_expert_pool", {
	id: integer().primaryKey(),
	count: integer().notNull(),
	startTime: numeric("start_time").notNull(),
	endTime: numeric("end_time").notNull(),
});

export const peakPoolVote = sqliteTable("peak_pool_vote", {
	id: integer().primaryKey(),
	startTime: numeric("start_time").notNull(),
	endTime: numeric("end_time").notNull(),
	count: integer().notNull(),
	subkey: integer().notNull(),
});

export const eidEffectInUse = sqliteTable("eid_effect_in_use", {
	id: integer().primaryKey(),
	effectArgs: customType({ dataType: () => 'JSON' })("effect_args"),
	eid: integer().notNull().references(() => eidEffect.id),
});

export const skillEffectInUse = sqliteTable("skill_effect_in_use", {
	id: integer().primaryKey(),
	info: text().notNull(),
	analyzeInfo: text("analyze_info").notNull(),
	args: customType({ dataType: () => 'JSON' })().notNull(),
	effectId: integer("effect_id").notNull().references(() => skillEffectType.id),
});

export const achievementBranch = sqliteTable("achievement_branch", {
	id: integer().primaryKey(),
	name: text().notNull(),
	pointTotal: integer("point_total").notNull(),
	isSeries: numeric("is_series").notNull(),
	typeId: integer("type_id").notNull().references(() => achievementType.id),
});

export const battleeffectcategorylink = sqliteTable("battleeffectcategorylink", {
	battleEffectId: integer("battle_effect_id").notNull().references(() => battleEffect.id),
	typeId: integer("type_id").notNull().references(() => battleEffectType.id),
},
(table) => [primaryKey({ columns: [table.battleEffectId, table.typeId], name: "battleeffectcategorylink_pk"}),
]);

export const elementtyperelationorm = sqliteTable("elementtyperelationorm", {
	sourceId: integer("source_id").notNull().references(() => elementType.id),
	targetId: integer("target_id").notNull().references(() => elementType.id),
	multiple: real().notNull(),
},
(table) => [primaryKey({ columns: [table.sourceId, table.targetId], name: "elementtyperelationorm_pk"}),
]);

export const elementTypeCombination = sqliteTable("element_type_combination", {
	id: integer().primaryKey(),
	name: text().notNull(),
	nameEn: text("name_en").notNull(),
	primaryId: integer("primary_id").notNull().references(() => elementType.id),
	secondaryId: integer("secondary_id").references(() => elementType.id),
	isDouble: numeric("is_double").notNull(),
});

export const glossaryentrylink = sqliteTable("glossaryentrylink", {
	sourceId: integer("source_id").notNull().references(() => glossaryEntry.id),
	targetId: integer("target_id").notNull().references(() => glossaryEntry.id),
},
(table) => [primaryKey({ columns: [table.sourceId, table.targetId], name: "glossaryentrylink_pk"}),
]);

export const petglossaryentrylink = sqliteTable("petglossaryentrylink", {
	petId: integer("pet_id").notNull().references(() => pet.id),
	glossaryEntryId: integer("glossary_entry_id").notNull().references(() => glossaryEntry.id),
},
(table) => [primaryKey({ columns: [table.petId, table.glossaryEntryId], name: "petglossaryentrylink_pk"}),
]);

export const item = sqliteTable("item", {
	id: integer().primaryKey(),
	name: text().notNull(),
	desc: text(),
	max: integer().notNull(),
	categoryId: integer("category_id").notNull().references(() => itemCategory.id),
});

export const gemCategory = sqliteTable("gem_category", {
	id: integer().primaryKey(),
	name: text().notNull(),
	generationId: integer("generation_id").notNull().references(() => gemGenerationCategory.id),
});

export const petSkinSeriesSubType = sqliteTable("pet_skin_series_sub_type", {
	id: integer().primaryKey(),
	name: text().notNull(),
	seriesId: integer("series_id").notNull().references(() => petSkinSeries.id),
});

export const petEncyclopediaEntry = sqliteTable("pet_encyclopedia_entry", {
	id: integer().primaryKey().references(() => pet.id),
	name: text().notNull(),
	hasSound: numeric("has_sound").notNull(),
	height: real(),
	weight: real(),
	foundin: text(),
	food: text(),
	introduction: text().notNull(),
});

export const petArchiveStoryEntry = sqliteTable("pet_archive_story_entry", {
	id: integer().primaryKey(),
	content: text().notNull(),
	petId: integer("pet_id").notNull().references(() => pet.id),
	bookId: integer("book_id").notNull().references(() => petArchiveStoryBook.id),
});

export const skilleffecttypetaglink = sqliteTable("skilleffecttypetaglink", {
	effectId: integer("effect_id").notNull().references(() => skillEffectType.id),
	tagId: integer("tag_id").notNull().references(() => skillEffectTypeTag.id),
},
(table) => [primaryKey({ columns: [table.effectId, table.tagId], name: "skilleffecttypetaglink_pk"}),
]);

export const skillEffectParamInType = sqliteTable("skill_effect_param_in_type", {
	id: integer().primaryKey(),
	position: integer().notNull(),
	paramId: integer("param_id").notNull().references(() => skillEffectParam.id),
});

export const mintmark = sqliteTable("mintmark", {
	id: integer().primaryKey(),
	name: text().notNull(),
	desc: text().notNull(),
	typeId: integer("type_id").notNull().references(() => mintmarkType.id),
	rarityId: integer("rarity_id").notNull().references(() => mintmarkRarity.id),
});

export const natureAttr = sqliteTable("nature_attr", {
	atk: numeric().notNull(),
	def: numeric().notNull(),
	spAtk: numeric("sp_atk").notNull(),
	spDef: numeric("sp_def").notNull(),
	spd: numeric().notNull(),
	hp: numeric().notNull(),
	percent: numeric().notNull(),
	id: integer().primaryKey().references(() => nature.id),
	total: numeric().notNull(),
});

export const achievement = sqliteTable("achievement", {
	id: integer().primaryKey(),
	name: text().notNull(),
	point: integer().notNull(),
	desc: text().notNull(),
	isHide: numeric("is_hide").notNull(),
	typeId: integer("type_id").notNull().references(() => achievementType.id),
	branchId: integer("branch_id").notNull().references(() => achievementBranch.id),
	nextLevelAchievementId: integer("next_level_achievement_id").references((): AnySQLiteColumn => achievement.id),
});

export const petVariation = sqliteTable("pet_variation", {
	id: integer().primaryKey(),
	name: text().notNull(),
	desc: text().notNull(),
	effectInUseId: integer("effect_in_use_id").references(() => eidEffectInUse.id),
});

export const petEffect = sqliteTable("pet_effect", {
	id: integer().primaryKey(),
	name: text().notNull(),
	desc: text().notNull(),
	effectInUseId: integer("effect_in_use_id").references(() => eidEffectInUse.id),
	starLevel: integer("star_level").notNull(),
	effectGroupId: integer("effect_group_id").notNull().references(() => petEffectGroup.id),
});

export const energyBead = sqliteTable("energy_bead", {
	id: integer().primaryKey().references(() => item.id),
	name: text().notNull(),
	desc: text().notNull(),
	idx: integer().notNull(),
	useTimes: integer("use_times").notNull(),
	effectInUseId: integer("effect_in_use_id").references(() => eidEffectInUse.id),
});

export const equipBonus = sqliteTable("equip_bonus", {
	id: integer().primaryKey(),
	desc: text().notNull(),
	effectInUseId: integer("effect_in_use_id").references(() => eidEffectInUse.id),
	newseId: integer("newse_id"),
	attributeId: integer("attribute_id").references(() => equipBonusAttr.id),
	hitRate: integer("hit_rate"),
	dodgeRate: integer("dodge_rate"),
	critRate: integer("crit_rate"),
});

export const suitBonus = sqliteTable("suit_bonus", {
	id: integer().primaryKey().references(() => suit.id),
	desc: text().notNull(),
	newseId: integer("newse_id"),
	effectInUseId: integer("effect_in_use_id").references(() => eidEffectInUse.id),
	attributeId: integer("attribute_id").references(() => suitBonusAttr.id),
});

export const gem = sqliteTable("gem", {
	id: integer().primaryKey().references(() => item.id),
	name: text().notNull(),
	level: integer().notNull(),
	generationId: integer("generation_id").notNull().references(() => gemGenerationCategory.id),
	nextLevelGemId: integer("next_level_gem_id").references((): AnySQLiteColumn => gem.id),
	categoryId: integer("category_id").notNull().references(() => gemCategory.id),
	skillEffectInUseId: integer("skill_effect_in_use_id").references(() => skillEffectInUse.id),
});

export const petSkin = sqliteTable("pet_skin", {
	id: integer().primaryKey(),
	name: text().notNull(),
	resourceId: integer("resource_id").notNull(),
	enemyResourceId: integer("enemy_resource_id"),
	cardPrice: integer("card_price"),
	petId: integer("pet_id").notNull().references(() => pet.id),
	categoryId: integer("category_id").notNull().references(() => petSkinCategory.id),
	seriesId: integer("series_id").references(() => petSkinSeries.id),
	subTypeId: integer("sub_type_id").references(() => petSkinSeriesSubType.id),
});

export const soulmark = sqliteTable("soulmark", {
	id: integer().primaryKey(),
	desc: text().notNull(),
	descFormattingAdjustment: text("desc_formatting_adjustment"),
	analyzeDesc: text("analyze_desc"),
	pveEffective: numeric("pve_effective"),
	intensified: numeric().notNull(),
	isAdv: numeric("is_adv").notNull(),
	effectInUseId: integer("effect_in_use_id").references(() => eidEffectInUse.id),
	intensifiedToId: integer("intensified_to_id").references((): AnySQLiteColumn => soulmark.id),
});

export const effectparamlink = sqliteTable("effectparamlink", {
	effectId: integer("effect_id").notNull().references(() => skillEffectType.id),
	paramInTypeId: integer("param_in_type_id").notNull().references(() => skillEffectParamInType.id),
},
(table) => [primaryKey({ columns: [table.effectId, table.paramInTypeId], name: "effectparamlink_pk"}),
]);

export const skillActivationItem = sqliteTable("skill_activation_item", {
	id: integer().primaryKey().references(() => item.id),
	name: text().notNull(),
	itemNumber: integer("item_number").notNull(),
});

export const skillStoneCategory = sqliteTable("skill_stone_category", {
	id: integer().primaryKey(),
	name: text().notNull(),
	typeId: integer("type_id").notNull().references(() => elementTypeCombination.id),
});

export const petmintmarklink = sqliteTable("petmintmarklink", {
	petId: integer("pet_id").notNull().references(() => pet.id),
	mintmarkId: integer("mintmark_id").notNull().references(() => mintmark.id),
},
(table) => [primaryKey({ columns: [table.petId, table.mintmarkId], name: "petmintmarklink_pk"}),
]);

export const abilityMintmarkPart = sqliteTable("ability_mintmark_part", {
	id: integer().primaryKey(),
	mintmarkId: integer("mintmark_id").notNull().references(() => mintmark.id),
	maxAttrValueId: integer("max_attr_value_id").references(() => mintmarkMaxAttr.id),
});

export const skillMintmarkPart = sqliteTable("skill_mintmark_part", {
	id: integer().primaryKey(),
	mintmarkId: integer("mintmark_id").notNull().references(() => mintmark.id),
	effect: integer().notNull(),
	arg: integer(),
});

export const universalMintmarkPart = sqliteTable("universal_mintmark_part", {
	id: integer().primaryKey(),
	mintmarkId: integer("mintmark_id").notNull().references(() => mintmark.id),
	mintmarkClassId: integer("mintmark_class_id").references(() => mintmarkClass.id),
	baseAttrValueId: integer("base_attr_value_id").references(() => mintmarkBaseAttr.id),
	maxAttrValueId: integer("max_attr_value_id").references(() => mintmarkMaxAttr.id),
	extraAttrValueId: integer("extra_attr_value_id").references(() => mintmarkExtraAttr.id),
});

export const titlePart = sqliteTable("title_part", {
	name: text().notNull(),
	originalName: text("original_name").notNull(),
	id: integer().primaryKey(),
	abilityDesc: text("ability_desc"),
	achievementId: integer("achievement_id").notNull().references(() => achievement.id),
});

export const energyBeadBuffAttr = sqliteTable("energy_bead_buff_attr", {
	atk: numeric().notNull(),
	def: numeric().notNull(),
	spAtk: numeric("sp_atk").notNull(),
	spDef: numeric("sp_def").notNull(),
	spd: numeric().notNull(),
	hp: numeric().notNull(),
	percent: numeric().notNull(),
	id: integer().primaryKey().references(() => energyBead.id),
	total: numeric().notNull(),
});

export const petsuitlink = sqliteTable("petsuitlink", {
	petId: integer("pet_id").notNull().references(() => pet.id),
	suitId: integer("suit_id").notNull().references(() => suitBonus.id),
},
(table) => [primaryKey({ columns: [table.petId, table.suitId], name: "petsuitlink_pk"}),
]);

export const equip = sqliteTable("equip", {
	id: integer().primaryKey().references(() => item.id),
	name: text().notNull(),
	speed: real(),
	partTypeId: integer("part_type_id").notNull().references(() => equipType.id),
	suitId: integer("suit_id").references(() => suit.id),
	bonusId: integer("bonus_id").references(() => equipBonus.id),
	occasionId: integer("occasion_id").references(() => equipEffectiveOccasion.id),
	pkHp: integer("pk_hp"),
	pkAtk: integer("pk_atk"),
	pkFireRange: integer("pk_fire_range"),
});

export const gemeffectlink = sqliteTable("gemeffectlink", {
	gemId: integer("gem_id").notNull().references(() => gem.id),
	skillEffectInUseId: integer("skill_effect_in_use_id").notNull().references(() => skillEffectInUse.id),
},
(table) => [primaryKey({ columns: [table.gemId, table.skillEffectInUseId], name: "gemeffectlink_pk"}),
]);

export const gemGen1Part = sqliteTable("gem_gen1_part", {
	id: integer().primaryKey().references(() => gem.id),
	inlayRate: real("inlay_rate").notNull(),
	equivalentLevel1Count: integer("equivalent_level1_count").notNull(),
	failCompensateLevelStart: integer("fail_compensate_level_start").notNull(),
	failCompensateLevelEnd: integer("fail_compensate_level_end").notNull(),
});

export const gemGen2Part = sqliteTable("gem_gen2_part", {
	id: integer().primaryKey().references(() => gem.id),
	upgradeCost: integer("upgrade_cost").notNull(),
});

export const petAdvance = sqliteTable("pet_advance", {
	id: integer().primaryKey(),
	petId: integer("pet_id").notNull().references(() => pet.id),
	soulmarkId: integer("soulmark_id").notNull().references(() => soulmark.id),
});

export const petsoulmarklink = sqliteTable("petsoulmarklink", {
	petId: integer("pet_id").notNull().references(() => pet.id),
	soulmarkId: integer("soulmark_id").notNull().references(() => soulmark.id),
},
(table) => [primaryKey({ columns: [table.petId, table.soulmarkId], name: "petsoulmarklink_pk"}),
]);

export const soulmarktaglink = sqliteTable("soulmarktaglink", {
	soulmarkId: integer("soulmark_id").notNull().references(() => soulmark.id),
	tagId: integer("tag_id").notNull().references(() => soulmarkTag.id),
},
(table) => [primaryKey({ columns: [table.soulmarkId, table.tagId], name: "soulmarktaglink_pk"}),
]);

export const skillStone = sqliteTable("skill_stone", {
	id: integer().primaryKey(),
	name: text().notNull(),
	rank: integer().notNull(),
	power: integer().notNull(),
	maxPp: integer("max_pp").notNull(),
	accuracy: integer().notNull(),
	categoryId: integer("category_id").notNull().references(() => skillStoneCategory.id),
	itemId: integer("item_id").notNull().references(() => item.id),
});

export const titleAttrBonus = sqliteTable("title_attr_bonus", {
	atk: numeric().notNull(),
	def: numeric().notNull(),
	spAtk: numeric("sp_atk").notNull(),
	spDef: numeric("sp_def").notNull(),
	spd: numeric().notNull(),
	hp: numeric().notNull(),
	percent: numeric().notNull(),
	id: integer().primaryKey().references(() => titlePart.id),
	total: numeric().notNull(),
});

export const petAdvanceBaseStats = sqliteTable("pet_advance_base_stats", {
	atk: numeric().notNull(),
	def: numeric().notNull(),
	spAtk: numeric("sp_atk").notNull(),
	spDef: numeric("sp_def").notNull(),
	spd: numeric().notNull(),
	hp: numeric().notNull(),
	percent: numeric().notNull(),
	id: integer().primaryKey().references(() => petAdvance.id),
	total: numeric().notNull(),
});

export const skill = sqliteTable("skill", {
	id: integer().primaryKey(),
	name: text().notNull(),
	power: integer().notNull(),
	maxPp: integer("max_pp").notNull(),
	accuracy: integer().notNull(),
	critRate: real("crit_rate"),
	priority: integer().notNull(),
	mustHit: numeric("must_hit").notNull(),
	atkNum: integer("atk_num").notNull(),
	info: text(),
	categoryId: integer("category_id").notNull().references(() => skillCategory.id),
	typeId: integer("type_id").notNull().references(() => elementTypeCombination.id),
	hideEffectId: integer("hide_effect_id").references(() => skillHideEffect.id),
	advanceId: integer("advance_id").references(() => petAdvance.id),
});

export const skillStoneEffect = sqliteTable("skill_stone_effect", {
	id: integer().primaryKey(),
	innerId: integer("inner_id").notNull(),
	prob: real().notNull(),
	skillStoneId: integer("skill_stone_id").notNull().references(() => skillStone.id),
});

export const skillinpetorm = sqliteTable("skillinpetorm", {
	learningLevel: integer("learning_level"),
	isSpecial: numeric("is_special").notNull(),
	isAdvanced: numeric("is_advanced").notNull(),
	isFifth: numeric("is_fifth").notNull(),
	skillId: integer("skill_id").notNull().references(() => skill.id),
	petId: integer("pet_id").notNull().references(() => pet.id),
	skillActivationItemId: integer("skill_activation_item_id").references(() => skillActivationItem.id),
},
(table) => [primaryKey({ columns: [table.skillId, table.petId], name: "skillinpetorm_pk"}),
]);

export const skilleffectlink = sqliteTable("skilleffectlink", {
	skillId: integer("skill_id").notNull().references(() => skill.id),
	effectInUseId: integer("effect_in_use_id").notNull().references(() => skillEffectInUse.id),
},
(table) => [primaryKey({ columns: [table.skillId, table.effectInUseId], name: "skilleffectlink_pk"}),
]);

export const skillfriendskilleffectlink = sqliteTable("skillfriendskilleffectlink", {
	skillId: integer("skill_id").notNull().references(() => skill.id),
	effectInUseId: integer("effect_in_use_id").notNull().references(() => skillEffectInUse.id),
},
(table) => [primaryKey({ columns: [table.skillId, table.effectInUseId], name: "skillfriendskilleffectlink_pk"}),
]);

export const skillstoneeffectlink = sqliteTable("skillstoneeffectlink", {
	skillStoneEffectId: integer("skill_stone_effect_id").notNull().references(() => skillStoneEffect.id),
	effectInUseId: integer("effect_in_use_id").notNull().references(() => skillEffectInUse.id),
},
(table) => [primaryKey({ columns: [table.skillStoneEffectId, table.effectInUseId], name: "skillstoneeffectlink_pk"}),
]);

export const skillmintmarklink = sqliteTable("skillmintmarklink", {
	skillId: integer("skill_id").notNull().references(() => skill.id),
	mintmarkId: integer("mintmark_id").notNull().references(() => mintmark.id),
},
(table) => [primaryKey({ columns: [table.skillId, table.mintmarkId], name: "skillmintmarklink_pk"}),
]);

