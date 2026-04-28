from functools import cached_property
from typing import TYPE_CHECKING, Any, TypedDict, cast

from seerapi_models.common import EidEffect, EidEffectInUse, ResourceRef, SixAttributes
from seerapi_models.items import (
	Equip,
	EquipBonus,
	EquipEffectiveOccasion,
	EquipType,
	Item,
	Suit,
	SuitBonus,
)
from seerapi_models.items.equip import OtherAttribute, PkAttribute
from seerapi_models.pet import Pet

from solaris.analyze.analyzers.items._general import BaseItemAnalyzer
from solaris.analyze.base import DataImportConfig
from solaris.analyze.typing_ import AnalyzeResult
from solaris.analyze.utils import create_category_map
from solaris.utils import split_string_arg

if TYPE_CHECKING:
	from solaris.parse.parsers.equip import EquipItem as UnityEquipItem
	from solaris.parse.parsers.items_optimize import (
		Item1,
		Item13,
	)
	from solaris.parse.parsers.suit import SuitConfig


def _create_suit_attribute(
	suit_effect_id: int | None,
	suit_effect_args: list[int],
	add_args_string: str | None,
) -> SixAttributes | None:
	"""
	创建套装属性加成

	浴火之前的套装使用EffectID+EffectArgs来表示属性加成，
	从浴火开始使用独立的AddArgs字段，
	该字段第一个参数表示是否为百分比加成
	"""
	if suit_effect_id == 630:
		return SixAttributes.from_list(suit_effect_args, percent=True)
	elif suit_effect_id == 631:
		return SixAttributes.from_list(suit_effect_args, percent=False)
	elif add_args_string:
		add_args = split_string_arg(add_args_string)
		if not add_args:
			return None

		percent = bool(add_args.pop(0))
		if not any(add_args):
			return None

		return SixAttributes.from_list(add_args, percent=percent)

	return None


class SuitBonusItem(TypedDict):
	desc: str
	mon_id: list[int]
	effect_id: int | None
	effect_args: list[int]
	newse_id: int | None
	add_attr: SixAttributes | None


class EquipBonusItem(TypedDict):
	desc: str
	attribute: SixAttributes | None
	other_attribute: OtherAttribute | None
	effect_id: int | None
	effect_args: list[int]
	newse_id: int | None


if TYPE_CHECKING:

	class EquipItem(UnityEquipItem):
		occasion: int
		equip_bonus: EquipBonusItem | None
		suit_bonus: SuitBonusItem | None


EMPTY_EQUIP_BONUS_ITEM = {
	'Lv': 1,
	'Attribute': '0 0 0 0 0 0',
	'AddWay': 1,
	'BattleLv': '0 0 0 0 0 0',
	'OtherAttribute': '0 0 0',
	'EffectID': '',
	'EffectArgs': '',
	'Desc': '',
}


class EquipAnalyzer(BaseItemAnalyzer):
	"""装备数据解析器"""

	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		return (
			DataImportConfig(
				flash_paths=(
					'config.xml.ItemSeXMLInfo.xml',
					'config.xml.ItemXMLInfo.xml',
				),
				unity_paths=('suit.json', 'equip.json'),
				patch_paths=('equip_effective_occasion.json', 'equip_type.json'),
			)
			+ super().get_data_import_config()
		)

	@classmethod
	def get_result_res_models(cls):
		return (Equip, Suit, EquipType, EquipEffectiveOccasion)

	def _create_equip_bonus_item(
		self, flash_equip: dict[str, Any]
	) -> EquipBonusItem | None:
		rank_data = flash_equip['Rank']
		if isinstance(rank_data, dict):
			equip_bonus_data = rank_data
		elif isinstance(rank_data, list):
			equip_bonus_data = rank_data[-1]
		else:
			raise ValueError(f'Invalid rank data: {rank_data}')

		if equip_bonus_data == EMPTY_EQUIP_BONUS_ITEM:
			return None

		add_way = bool(equip_bonus_data['AddWay'])
		other_attr_args = split_string_arg(equip_bonus_data['OtherAttribute'])
		other_attr = (
			OtherAttribute.from_list(other_attr_args) if any(other_attr_args) else None
		)
		attr_args = split_string_arg(equip_bonus_data['Attribute'])
		equip_attr = SixAttributes.from_list(attr_args, percent=add_way)
		return EquipBonusItem(
			desc=equip_bonus_data['Desc'],
			attribute=equip_attr,
			other_attribute=other_attr,
			effect_id=equip_bonus_data['EffectID'],
			effect_args=split_string_arg(equip_bonus_data['EffectArgs']),
			newse_id=equip_bonus_data.get('EquipNewseId'),
		)

	def _create_suit_bonus_item(
		self, flash_equip: dict[str, Any]
	) -> SuitBonusItem | None:
		suit_effect_id = flash_equip.get('SuitEffectID')
		suit_effect_args = split_string_arg(flash_equip.get('SuitEffectArgs', ''))
		suit_newse_id = flash_equip.get('SuitNewseId')
		if not any((suit_effect_id, suit_effect_args, suit_newse_id)):
			return None

		suit_attr = _create_suit_attribute(
			suit_effect_id,
			suit_effect_args,
			flash_equip.get('AddArgs'),
		)
		mon_id = args if any(args := split_string_arg(flash_equip['MonID'])) else []
		return SuitBonusItem(
			desc=flash_equip['Desc'],
			mon_id=mon_id,
			effect_id=suit_effect_id,
			effect_args=suit_effect_args,
			newse_id=suit_newse_id,
			add_attr=suit_attr,
		)

	@cached_property
	def ability_equip_map(self) -> dict[int, 'EquipItem']:
		unity_data: list['UnityEquipItem'] = self._get_data('unity', 'equip.json')[
			'equips'
		]['equip']
		flash_data = self._get_data('flash', 'config.xml.ItemSeXMLInfo.xml')['Equips'][
			'Equip'
		]
		flash_data_map = {i['ItemID']: i for i in flash_data}

		result: dict[int, 'EquipItem'] = {}
		for equip in unity_data:
			flash_equip = flash_data_map[equip['item_id']]
			item_id = equip['item_id']
			equip_item: 'EquipItem' = {
				**equip,
				'occasion': flash_equip['Occasion'],
				'equip_bonus': self._create_equip_bonus_item(flash_equip),
				'suit_bonus': self._create_suit_bonus_item(flash_equip),
			}
			result[item_id] = equip_item
		return result

	def _get_equip_to_suit_map(self, suit_data: 'SuitConfig') -> dict[int, Suit]:
		"""
		获取装备到套装的映射关系
		"""
		suit_map: dict[int, Suit] = {}
		for suit in suit_data['root']['item']:
			suit_id = suit['id']
			suit_bonus: SuitBonus | None = None
			equip_ids = suit['cloths']
			if (part_dict := self.ability_equip_map.get(equip_ids[0])) and (
				suit_bonus_dict := part_dict['suit_bonus']
			):
				eid_effect_id = suit_bonus_dict['effect_id']
				eid_effect_args = suit_bonus_dict['effect_args']

				eid_effect = None
				if eid_effect_id and eid_effect_args:
					eid_effect = EidEffectInUse(
						effect=ResourceRef.from_model(EidEffect, id=eid_effect_id),
						effect_args=eid_effect_args,
					)
				suit_bonus = SuitBonus(
					id=suit_id,
					desc=suit_bonus_dict['desc'],
					attribute=suit_bonus_dict['add_attr'],
					eid_effect=eid_effect,
					newse_id=suit_bonus_dict.get('newse_id'),
					effective_pets=[
						ResourceRef.from_model(Pet, id=mon_id)
						for mon_id in suit_bonus_dict['mon_id']
					],
				)
			suit_obj = Suit(
				id=suit_id,
				name=suit['name'],
				suit_desc=suit['suitdes'],
				equips=[
					ResourceRef.from_model(Equip, id=equip_id) for equip_id in equip_ids
				],
				transform=bool(suit.get('transform')),
				tran_speed=suit.get('tran_speed'),
				bonus=suit_bonus,
			)
			suit_map[suit_id] = suit_obj

		return suit_map

	@cached_property
	def flash_equip_items_data(self) -> dict[int, dict[str, Any]]:
		flash_data = self._get_data('flash', 'config.xml.ItemXMLInfo.xml')['root'][
			'items'
		]
		return {
			item['ID']: item
			for category in flash_data
			if category['Name'] == '个人装扮'
			for item in category['item']
		}

	def _create_pk_attribute(self, equip_id: int) -> 'PkAttribute | None':
		equip = self.flash_equip_items_data[equip_id]
		pk_hp = equip.pop('PkHp', 0)
		pk_atk = equip.pop('PkAtk', 0)
		pk_fire_range = equip.pop('PkFireRange', 0)
		if pk_hp or pk_atk or pk_fire_range:
			return PkAttribute(
				pk_hp=pk_hp,
				pk_atk=pk_atk,
				pk_fire_range=pk_fire_range,
			)

		return None

	def _get_equip_items_data(self) -> 'dict[int, Item1 | Item13]':
		items_data_part1 = cast(
			list['Item1'], self.get_category_items(1)['root']['items']
		)
		items_data_part2 = cast(
			list['Item13'], self.get_category_items(13)['root']['items']
		)
		return {item['id']: item for item in items_data_part1 + items_data_part2}

	def analyze(self) -> tuple[AnalyzeResult, ...]:
		suit_data: 'SuitConfig' = self._get_data('unity', 'suit.json')

		part_type_patch = self._get_data('patch', 'equip_type.json')
		occasion_patch = self._get_data('patch', 'equip_effective_occasion.json')

		equip_items_map = self._get_equip_items_data()
		suit_map = self._get_equip_to_suit_map(suit_data)
		equip_to_suit_map = {
			equip_ref.id: suit_obj
			for suit_obj in suit_map.values()
			for equip_ref in suit_obj.equips
		}

		# 处理部件
		part_type_map_for_name = {row['name']: row for row in part_type_patch.values()}
		part_type_map = create_category_map(
			part_type_patch,
			model_cls=EquipType,
			array_key='equip',
		)
		occasion_map = create_category_map(
			occasion_patch,
			model_cls=EquipEffectiveOccasion,
			array_key='equip',
		)
		equip_map: dict[int, Equip] = {}
		for equip_id, equip_dict in equip_items_map.items():
			equip_name = equip_dict['name']
			equip_ref = ResourceRef.from_model(Equip, id=equip_id)
			equip_bonus = None
			occasion = None

			# 处理部件加成
			if (ability_equip := self.ability_equip_map.get(equip_id)) and (
				bonus_dict := ability_equip['equip_bonus']
			):
				occasion = ResourceRef.from_model(
					occasion_map[ability_equip['occasion']]
				)
				eid_effect_id = bonus_dict['effect_id']
				eid_effect_args = bonus_dict['effect_args']
				eid_effect = None
				if eid_effect_id and eid_effect_args:
					eid_effect = EidEffectInUse(
						effect=ResourceRef.from_model(EidEffect, id=eid_effect_id),
						effect_args=eid_effect_args,
					)
				equip_bonus = EquipBonus(
					desc=bonus_dict['desc'],
					attribute=bonus_dict['attribute'],
					other_attribute=bonus_dict['other_attribute'],
					eid_effect=eid_effect,
					newse_id=bonus_dict.get('newse_id'),
				)
				occasion_map.add_element(occasion.id, equip_ref)

			suit_ref = None
			if suit_obj := equip_to_suit_map.get(equip_id):
				suit_ref = ResourceRef.from_model(suit_obj)

			part_type_name = equip_dict.get('type')
			part_type_id = part_type_map_for_name[part_type_name]['id']
			part_type_ref = ResourceRef.from_model(part_type_map[part_type_id])

			speed = equip_dict.get('speed')  # int or null
			equip_map[equip_id] = Equip(
				id=equip_id,
				name=equip_name,
				part_type=part_type_ref,
				speed=speed,
				pk_attribute=self._create_pk_attribute(equip_id),
				suit=suit_ref,
				bonus=equip_bonus,
				occasion=occasion,
				item=ResourceRef.from_model(Item, id=equip_id),
			)
			part_type_map.add_element(part_type_id, equip_ref)

		return (
			AnalyzeResult(model=Equip, data=equip_map),
			AnalyzeResult(model=Suit, data=suit_map),
			AnalyzeResult(
				model=SuitBonus,
				data={
					suit_id: suit_obj.bonus
					for suit_id, suit_obj in suit_map.items()
					if suit_obj.bonus
				},
				output_mode='db',
			),
			AnalyzeResult(model=EquipType, data=part_type_map),
			AnalyzeResult(model=EquipEffectiveOccasion, data=occasion_map),
		)
