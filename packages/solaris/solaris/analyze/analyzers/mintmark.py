from typing import TYPE_CHECKING, Any, cast

from seerapi_models.common import ResourceRef, SixAttributes
from seerapi_models.mintmark import (
	AbilityMintmark,
	Mintmark,
	MintmarkClassCategory,
	MintmarkRarityCategory,
	MintmarkTypeCategory,
	SkillMintmark,
	SkillMintmarkEffect,
	UniversalMintmark,
)
from seerapi_models.pet import Pet
from seerapi_models.skill import Skill

from ..base import BaseDataSourceAnalyzer, DataImportConfig
from ..typing_ import AnalyzeResult
from ..utils import CategoryMap, create_category_map

if TYPE_CHECKING:
	from solaris.parse.parsers.mintmark import MintmarkConfig, MintMarkItem


def _create_attr_values(data: 'MintMarkItem') -> dict[str, Any]:
	kwargs = {}
	for k, name in [
		('base_attri_value', 'base_attr_value'),
		('max_attri_value', 'max_attr_value'),
		('extra_attri_value', 'extra_attr_value'),
	]:
		if value := data[k]:
			kwargs[name] = SixAttributes.from_list(value)

	return kwargs


class MintmarkAnalyzer(BaseDataSourceAnalyzer):
	"""刻印相关数据分析器"""

	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		return DataImportConfig(
			unity_paths=('mintmark.json',),
			flash_paths=('config.xml.CountermarkXMLInfo.xml',),
			patch_paths=('mintmark_type.json',),
		)

	@classmethod
	def get_result_res_models(cls):
		return (
			Mintmark,
			AbilityMintmark,
			SkillMintmark,
			UniversalMintmark,
			MintmarkClassCategory,
			MintmarkTypeCategory,
			MintmarkRarityCategory,
		)

	def analyze(self) -> tuple[AnalyzeResult, ...]:
		"""分析刻印数据并返回模式构建器列表"""
		mintmark_data: MintmarkConfig = self._get_data('unity', 'mintmark.json')
		mintmark_type_csv = self._get_data('patch', 'mintmark_type.json')
		mintmark_list = mintmark_data['mint_marks']['mint_mark']
		classes_map: CategoryMap[int, MintmarkClassCategory, ResourceRef] = CategoryMap(
			'mintmark'
		)
		classes_map.update(
			{
				i['id']: MintmarkClassCategory(id=i['id'], name=i['class_name'])
				for i in mintmark_data['mint_marks']['mintmark_class']
			}
		)
		type_map: CategoryMap[int, MintmarkTypeCategory, ResourceRef] = (
			create_category_map(
				mintmark_type_csv,
				model_cls=MintmarkTypeCategory,
				array_key='mintmark',
			)
		)
		rarity_map: CategoryMap[int, MintmarkRarityCategory, ResourceRef] = CategoryMap(
			'mintmark'
		)
		rarity_map.update({i: MintmarkRarityCategory(id=i) for i in range(1, 6)})
		effect_map: dict[int, int] = {
			i['ID']: i['Effect']
			for i in self._get_data('flash', 'config.xml.CountermarkXMLInfo.xml')[
				'MintMarks'
			]['MintMark']
			if 'Effect' in i
		}
		mintmark_map: dict[int, Mintmark] = {}
		ability_mintmark_map: dict[int, AbilityMintmark] = {}
		skill_mintmark_map: dict[int, SkillMintmark] = {}
		universal_mintmark_map: dict[int, UniversalMintmark] = {}
		for mintmark in mintmark_list:
			id_ = mintmark['id']
			# 跳过最后三个刻印（大，中，小碎片）
			if id_ > 49999:
				continue
			name = mintmark['des']
			type_id = mintmark['type']
			mintmark_ref = ResourceRef.from_model(
				Mintmark,
				id=id_,
			)
			type_ref = ResourceRef.from_model(
				MintmarkTypeCategory,
				id=type_id,
			)
			rarity_ref = ResourceRef.from_model(
				MintmarkRarityCategory,
				id=(rarity_id := mintmark['rare']),
			)
			pet_refs = None
			if pet_ids := mintmark['monster_id']:
				pet_refs = [ResourceRef.from_model(Pet, id=id_) for id_ in pet_ids]
			skill_refs = None
			if skill_ids := mintmark['move_id']:
				skill_refs = [
					ResourceRef.from_model(Skill, id=id_) for id_ in skill_ids
				]
			# 飓风利袭刻印的Arg字段是错误的，删除它
			if id_ == 20187:
				mintmark['arg'].clear()

			skill_effect = None
			max_attr_value = None
			attr_kwargs = _create_attr_values(mintmark)
			if type_id == 0:
				max_attr_value = SixAttributes.from_list(mintmark['arg'])
				attr_kwargs['max_attr_value'] = max_attr_value
			elif type_id == 1:
				skill_effect = SkillMintmarkEffect(
					effect=effect_map[id_],
					arg=mintmark['arg'][0] if mintmark['arg'] else None,
				)

			class_ref = None
			if classes_id := mintmark['mintmark_class']:
				classes_map.add_element(classes_id, mintmark_ref)
				class_ref = ResourceRef.from_model(
					MintmarkClassCategory,
					id=classes_id,
				)
			mintmark_obj = Mintmark(
				id=id_,
				name=name,
				type=type_ref,
				rarity=rarity_ref,
				pet=pet_refs,
				effect=skill_effect,
				desc=mintmark['effect_des'],
				mintmark_class=class_ref,
				skill=skill_refs,
				**attr_kwargs,
			)
			mintmark_map[id_] = mintmark_obj
			type_map.add_element(type_id, mintmark_ref)
			rarity_map.add_element(rarity_id, mintmark_ref)
			if type_id == 0:
				ability_mintmark_map[id_] = cast(
					AbilityMintmark, mintmark_obj.to_detailed()
				)
			elif type_id == 1:
				skill_mintmark_map[id_] = cast(
					SkillMintmark, mintmark_obj.to_detailed()
				)
			elif type_id == 3:
				universal_mintmark_map[id_] = cast(
					UniversalMintmark, mintmark_obj.to_detailed()
				)
		return (
			AnalyzeResult(model=Mintmark, data=mintmark_map),
			AnalyzeResult(model=AbilityMintmark, data=ability_mintmark_map),
			AnalyzeResult(model=SkillMintmark, data=skill_mintmark_map),
			AnalyzeResult(model=UniversalMintmark, data=universal_mintmark_map),
			AnalyzeResult(model=MintmarkClassCategory, data=classes_map),
			AnalyzeResult(model=MintmarkTypeCategory, data=type_map),
			AnalyzeResult(model=MintmarkRarityCategory, data=rarity_map),
		)
