from functools import cached_property
from typing import TYPE_CHECKING

from seerapi_models.common import ResourceRef, SkillEffectInUse
from seerapi_models.items import (
	Gem,
	GemCategory,
	GemGen1,
	GemGen2,
	GemGenCategory,
	Item,
)

from solaris.analyze.analyzers.skill import BaseSkillEffectAnalyzer
from solaris.analyze.base import DataImportConfig
from solaris.analyze.typing_ import AnalyzeResult
from solaris.analyze.utils import CategoryMap

if TYPE_CHECKING:
	from solaris.parse.parsers.gems import GemItem as UnityGemItem


def _get_generation_id_from_category(category_id: int) -> int:
	"""根据宝石类别ID获取宝石世代"""
	if category_id < 100:
		return 1
	elif category_id > 100:
		return 2
	else:
		raise ValueError(f'Invalid category id: {category_id}')


if TYPE_CHECKING:

	class GemItem(UnityGemItem):
		fail_compensate_start: int
		fail_compensate_end: int
		equit_lv1_cnt1: int
		inlay_prob: int


class GemAnalyzer(BaseSkillEffectAnalyzer):
	"""刻印宝石数据解析器"""

	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		return super().get_data_import_config() + DataImportConfig(
			unity_paths=('gems.json',), flash_paths=('config.xml.GemsXMLInfo.xml',)
		)

	@classmethod
	def get_result_res_models(cls):
		return (Gem, GemCategory, GemGenCategory, GemGen1, GemGen2)

	@cached_property
	def gem_data(self) -> dict[int, 'GemItem']:
		unity_data: list['UnityGemItem'] = self._get_data('unity', 'gems.json')['gems'][
			'gem'
		]
		flash_data = self._get_data('flash', 'config.xml.GemsXMLInfo.xml')['Gems'][
			'Gem'
		]
		flash_data_map = {i['ID']: i for i in flash_data}
		result = {}
		for gem in unity_data:
			id_ = gem['id']
			result[id_] = {
				**gem,
				'fail_compensate_start': flash_data_map[id_]['FailCompensateStart'],
				'fail_compensate_end': flash_data_map[id_]['FailCompensateEnd'],
				'equit_lv1_cnt1': flash_data_map[id_]['EquitLv1Cnt1'],
				'inlay_prob': flash_data_map[id_]['InlayProb'],
			}

		return result

	def _create_gem_effect(self, data: 'GemItem') -> list[SkillEffectInUse]:
		effect = data['skill_effects'][0]['effect']
		if not effect:
			return []
		id_ = effect['effect_id']
		args = effect['param']
		effect_in_use_list = self.create_skill_effect(type_ids=[id_], args=args)
		if not effect_in_use_list:
			raise ValueError(f'宝石效果创建失败: {id_} {args}')

		return effect_in_use_list

	def analyze(self) -> tuple[AnalyzeResult, ...]:
		"""分析宝石数据并返回模式构建器列表"""
		gem_map: dict[int, Gem] = {}
		gem_category_map: CategoryMap[int, GemCategory, ResourceRef] = CategoryMap(
			'gem'
		)
		gem_gen_category_map: CategoryMap[int, GemGenCategory, ResourceRef] = (
			CategoryMap('gem_category')
		)
		for gem_id, gem_data in self.gem_data.items():
			category_id = gem_data['category']
			if category_id in gem_category_map:
				continue

			generation_id = _get_generation_id_from_category(category_id)
			name_slice = -3 if generation_id == 1 else -1
			category = GemCategory(
				id=category_id,
				name=gem_data['name'][:name_slice],
				generation_id=generation_id,
			)
			gem_category_map[category_id] = category

			if generation_id in gem_gen_category_map:
				continue
			gem_gen_category_map[generation_id] = GemGenCategory(
				id=generation_id,
			)

		for gem_id, gem_data in self.gem_data.items():
			category_id = gem_data['category']
			category_ref = ResourceRef.from_model(gem_category_map[category_id])

			generation_id = _get_generation_id_from_category(category_id)
			fail_compensate_range = None
			upgrade_cost = None
			equivalent_level1_count = None
			if generation_id == 1:
				fail_compensate_range = (
					gem_data['fail_compensate_start'],
					gem_data['fail_compensate_end'],
				)
				equivalent_level1_count = gem_data['equit_lv1_cnt1']
			else:
				upgrade_cost = gem_data['equit_lv1_cnt1']

			gem_obj = Gem(
				id=gem_id,
				name=gem_data['name'],
				level=gem_data['lv'],
				generation_id=generation_id,
				category=category_ref,
				inlay_rate=gem_data['inlay_prob'] / 100,
				equivalent_level1_count=equivalent_level1_count,
				effect=self._create_gem_effect(gem_data),
				upgrade_cost=upgrade_cost,
				fail_compensate_range=fail_compensate_range,
				item=ResourceRef.from_model(Item, id=gem_id),
			)
			gem_map[gem_id] = gem_obj

			gem_ref = ResourceRef.from_model(gem_obj)
			gem_category_map.add_element(category_id, gem_ref)
			gem_gen_category_map.add_element(generation_id, gem_ref)

		for gem_category in gem_category_map.values():
			for prev_ref, next_ref in zip(gem_category.gem, gem_category.gem[1:]):
				prev_model = gem_map[prev_ref.id]
				next_model = gem_map[next_ref.id]
				prev_model.next_level_gem = next_ref
				next_model.prev_level_gem = prev_ref

		return (
			AnalyzeResult(model=Gem, data=gem_map),
			AnalyzeResult(model=GemCategory, data=gem_category_map),
			AnalyzeResult(model=GemGenCategory, data=gem_gen_category_map),
			AnalyzeResult(
				model=GemGen1,
				data={
					gem_id: gem.to_detailed()
					for gem_id, gem in gem_map.items()
					if gem.generation_id == 1
				},
				output_mode='json',
			),
			AnalyzeResult(
				model=GemGen2,
				data={
					gem_id: gem.to_detailed()
					for gem_id, gem in gem_map.items()
					if gem.generation_id == 2
				},
				output_mode='json',
			),
		)
