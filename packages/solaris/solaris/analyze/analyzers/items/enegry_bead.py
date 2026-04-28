from functools import cached_property
from typing import TYPE_CHECKING, cast

from seerapi_models.common import EidEffect, EidEffectInUse, ResourceRef, SixAttributes
from seerapi_models.items import EnergyBead, Item

from solaris.analyze.base import DataImportConfig
from solaris.analyze.typing_ import AnalyzeResult
from solaris.utils import split_string_arg

from ._general import BaseItemAnalyzer

if TYPE_CHECKING:
	from solaris.parse.parsers.items_optimize import Item3
	from solaris.parse.parsers.new_se import NewSeItem as UnityNewSeItem


def _convert_beads_arg(args: list[int], primary: bool = False) -> SixAttributes:
	"""将能量珠加成项的参数转换为六维属性"""
	ability_args = [0 for _ in range(6)]
	position, value = args[0], args[1]
	# 初级能量珠表示加成项的参数与其他等级不同
	if primary:
		if position == 2:
			position = 3
		elif position == 3:
			position = 0
		elif position == 4:
			position = 2
		elif position == 5:
			position = 4
	else:
		position -= 1
	ability_args[position] = value
	return SixAttributes.from_list(ability_args)


if TYPE_CHECKING:

	class NewSeItem(UnityNewSeItem):
		AddType: int
		Times: int


class EnergyBeadAnalyzer(BaseItemAnalyzer):
	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		return (
			DataImportConfig(
				unity_paths=(
					'new_se.json',
					'itemsTip.json',
				),
				flash_paths=('config.xml.PetEffectXMLInfo.xml',),
			)
			+ super().get_data_import_config()
		)

	@classmethod
	def get_result_res_models(cls):
		return (EnergyBead,)

	@cached_property
	def bead_effect_data(self) -> dict[int, 'NewSeItem']:
		unity_data: list['UnityNewSeItem'] = self._get_data('unity', 'new_se.json')[
			'NewSe'
		]['NewSeIdx']
		flash_data = self._get_data('flash', 'config.xml.PetEffectXMLInfo.xml')[
			'NewSe'
		]['NewSeIdx']
		flash_data_map = {i['Idx']: i for i in flash_data}
		return {
			data['ItemId']: {
				'AddType': flash_data_map[data['Idx']].get('AddType', 0),
				'Times': flash_data_map[data['Idx']]['Times'],
				**data,
			}
			for data in unity_data
			if data['Stat'] == 2
		}

	def analyze(self) -> tuple[AnalyzeResult, ...]:
		bead_map: dict[int, EnergyBead] = {}
		bead_effect_data: dict[int, 'NewSeItem'] = self.bead_effect_data
		pet_item_data: dict[int, 'Item3'] = {
			data['id']: cast('Item3', data)
			for data in self.get_category_items(3)['root']['items']
		}
		desc_data: dict[int, str] = {
			data['id']: data['des']
			for data in self._get_data('unity', 'itemsTip.json')['root']['item']
		}

		for item_id, effect in bead_effect_data.items():
			effect_obj = EidEffectInUse(
				effect=ResourceRef.from_model(EidEffect, id=effect['Eid']),
				effect_args=split_string_arg(effect['Args']),
			)

			effect_args = cast(list[int], effect_obj.effect_args).copy()
			ability_buff = None
			if effect['AddType'] == 1:
				ability_buff = SixAttributes.from_list(effect_args, hp_first=True)
			elif effect_obj.effect.id == 26:
				ability_buff = _convert_beads_arg(
					effect_args, primary=effect['Idx'] < 1006
				)
			bead = EnergyBead(
				id=item_id,
				name=pet_item_data[item_id]['name'],
				desc=desc_data[item_id],
				effect=effect_obj,
				idx=effect['Idx'],
				item=ResourceRef.from_model(
					Item,
					id=effect['ItemId'],
				),
				use_times=effect['Times'],
				ability_buff=ability_buff,
			)
			bead_map[bead.id] = bead

		return (AnalyzeResult(model=EnergyBead, data=bead_map),)
