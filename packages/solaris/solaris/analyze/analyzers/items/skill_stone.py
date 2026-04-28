from functools import cached_property
from typing import TYPE_CHECKING, cast

from seerapi_models.common import ResourceRef
from seerapi_models.element_type import TypeCombination
from seerapi_models.items import Item, SkillStone, SkillStoneCategory, SkillStoneEffect

from solaris.analyze.base import AnalyzeResult, DataImportConfig
from solaris.analyze.utils import CategoryMap
from solaris.utils import split_string_arg

from ..skill import BaseSkillEffectAnalyzer
from ._general import BaseItemAnalyzer

if TYPE_CHECKING:
	from solaris.parse.parsers.items_optimize import Item11


if TYPE_CHECKING:

	class SkillStoneDict(Item11):
		power: int
		max_pp: int
		accuracy: int
		effect: list['SkillStoneEffect']


class SkillStoneAnalyzer(BaseSkillEffectAnalyzer, BaseItemAnalyzer):
	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		config = DataImportConfig(
			flash_paths=('config.xml.SkillXMLInfo_skillStoneClass.xml',),
		)
		return (
			config
			+ BaseItemAnalyzer.get_data_import_config()
			+ BaseSkillEffectAnalyzer.get_data_import_config()
		)

	@classmethod
	def get_result_res_models(cls):
		return (SkillStone, SkillStoneCategory)

	@cached_property
	def skill_stone_data(self) -> dict[int, 'SkillStoneDict']:
		unity_data = cast(list['Item11'], self.get_category_items(11)['root']['items'])
		flash_data = self._get_data(
			'flash', 'config.xml.SkillXMLInfo_skillStoneClass.xml'
		)['MoveStones']['MoveStone']
		flash_data_map = {stone['ID']: stone for stone in flash_data}
		result = {}
		for stone in unity_data:
			id_ = stone['id'] - 1100000
			flash_stone = flash_data_map[id_]
			move_effects = [
				SkillStoneEffect(
					inner_id=effect['ID'],
					prob=effect['EffectProb'] / 100,
					effect=self.create_skill_effect(
						type_ids=split_string_arg(effect['SideEffect']),
						args=split_string_arg(effect['SideEffectArg']),
					),
				)
				for effect in flash_stone['MoveEffect']
			]
			result[id_] = {
				**stone,
				'power': flash_stone['Power'],
				'max_pp': flash_stone['MaxPP'],
				'accuracy': flash_stone['Accuracy'],
				'effect': move_effects,
			}
		return result

	def analyze(self) -> tuple[AnalyzeResult, ...]:
		skill_stone_data = self.skill_stone_data

		category_type_set = set()
		skill_stone_map: dict[int, SkillStone] = {}
		skill_stone_category_map: CategoryMap[
			int,
			SkillStoneCategory,
			SkillStone,
		] = CategoryMap('skill_stone')
		for id_, skill_stone in skill_stone_data.items():
			item_ref = ResourceRef.from_model(Item, id=id_ + 1100000)
			# 获取不带等级的技能石名称
			category_name = skill_stone['name'].split('级')[1]
			type_id = skill_stone['type']
			if type_id not in category_type_set:
				category_type_set.add(type_id)
				skill_stone_category_map[type_id] = SkillStoneCategory(
					id=type_id,
					name=category_name,
					type=ResourceRef.from_model(TypeCombination, id=type_id),
				)

			category = skill_stone_category_map[type_id]
			skill_stone_obj = SkillStone(
				id=id_,
				name=skill_stone['name'],
				rank=skill_stone['rank'],
				power=skill_stone['power'],
				max_pp=skill_stone['max_pp'],
				accuracy=skill_stone['accuracy'],
				item=item_ref,
				category=ResourceRef.from_model(category),
				effect=skill_stone['effect'],
			)
			category.skill_stone.append(ResourceRef.from_model(skill_stone_obj))
			skill_stone_map[id_] = skill_stone_obj

		return (
			AnalyzeResult(model=SkillStone, data=skill_stone_map),
			AnalyzeResult(model=SkillStoneCategory, data=skill_stone_category_map),
		)
