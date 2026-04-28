from typing import TYPE_CHECKING

from seerapi_models.common import ResourceRef
from seerapi_models.items import Item, SkillActivationItem
from seerapi_models.pet import Pet
from seerapi_models.skill import Skill

from solaris.analyze.base import BaseDataSourceAnalyzer, DataImportConfig
from solaris.analyze.typing_ import AnalyzeResult

if TYPE_CHECKING:
	from solaris.parse.parsers.sp_hide_moves import SpMovesItem


class SkillActivationItemAnalyzer(BaseDataSourceAnalyzer):
	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		return DataImportConfig(unity_paths=('spHideMoves.json',))

	@classmethod
	def get_result_res_models(cls):
		return (SkillActivationItem,)

	def analyze(self) -> tuple[AnalyzeResult, ...]:
		skill_activation_data: dict[int, 'SpMovesItem'] = {
			data['item']: data
			for data in self._get_data('unity', 'spHideMoves.json')['config'][
				'sp_moves'
			]
		}

		skill_activation_map: dict[int, SkillActivationItem] = {}
		for item_id, data in skill_activation_data.items():
			skill_ref = ResourceRef.from_model(Skill, id=data['moves'])
			pet_ref = ResourceRef.from_model(Pet, id=data['monster'])
			item_ref = ResourceRef.from_model(Item, id=item_id)
			skill_activation_map[item_id] = SkillActivationItem(
				id=item_id,
				name=data['itemname'],
				item_number=data['itemnumber'],
				item=item_ref,
				skill=skill_ref,
				pet=pet_ref,
			)

		return (AnalyzeResult(model=SkillActivationItem, data=skill_activation_map),)
