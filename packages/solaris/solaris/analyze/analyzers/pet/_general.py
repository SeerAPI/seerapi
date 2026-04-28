from collections import defaultdict
from functools import cached_property
from typing import TYPE_CHECKING, Any, cast

from solaris.analyze.analyzers.peak_pool import PeakPoolAnalyzer
from solaris.analyze.base import (
	BaseAnalyzer,
	BaseDataSourcePostAnalyzer,
	DataImportConfig,
)
from solaris.analyze.utils import merge_dict_item

if TYPE_CHECKING:
	from solaris.parse.parsers.awakendetail import TaskItem as AwakenDetailTaskItem
	from solaris.parse.parsers.effect_icon import EffectIconItem
	from solaris.parse.parsers.monsters import MonsterItem
	from solaris.parse.parsers.pet_skin import PetSkinConfig, _SkinItem
	from solaris.parse.parsers.petbook import ArchivesStoryConfig, ArchivesStoryInfo
	from solaris.parse.parsers.sp_hide_moves import SpHideMovesConfig, SpMovesItem


general_import_config = DataImportConfig(
	unity_paths=(
		'monsters.json',
		'spHideMoves.json',
		'petbook.json',
		'archivesStory.json',
		'petSkin.json',
		'effectag.json',
		'petEffectIcon.json',
		'effectIcon.json',
		'pvpBan.json',
		'pvpBanExpert.json',
		'awakenDetail.json',
	),
	flash_paths=(
		'config.xml.PetXMLInfo.xml',
		'config.xml.PetBookXMLInfo.xml',
		'config.xml.PetLeftAndRightXmlInfo_petClass.xml',
	),
	patch_paths=(
		'pet_gender.json',
		'pet_mount_type.json',
		'pet_vipbuff.json',
		'pet_archive_story_book.json',
	),
)


class BasePetAnalyzer(BaseDataSourcePostAnalyzer):
	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		return general_import_config

	@classmethod
	def get_input_analyzers(cls) -> tuple[type[BaseAnalyzer], ...]:
		return (PeakPoolAnalyzer,)

	@cached_property
	def pet_origin_data(self) -> dict[int, dict[str, Any]]:
		flash_data = self._get_data('flash', 'config.xml.PetXMLInfo.xml')['Monsters'][
			'Monster'
		]
		unity_data: list['MonsterItem'] = self._get_data('unity', 'monsters.json')[
			'monsters'
		]['monster']
		keys = (
			'YieldingExp',
			'YieldingEV',
			'CatchRate',
			'DiyRaceMin',
			'DiyRaceMax',
			'FuseMaster',
			'FuseSub',
			'Resist',
			'IsRareMon',
			'IsAbilityMon',
			'IsFuseMon',
			'BreedingMon',
			'VipBtlAdj',
		)
		flash_map = {pet['ID']: pet for pet in flash_data}
		result = {}
		for pet in unity_data:
			pet_id = pet['id']
			if pet_id > 9999:
				break

			for key in keys:
				merge_dict_item(cast(dict, pet), flash_map.get(pet_id, {}), key)

			result[pet_id] = pet

		return result

	@cached_property
	def pet_skin_data(self) -> dict[int, '_SkinItem']:
		data: PetSkinConfig = self._get_data('unity', 'petSkin.json')
		return {skin['id']: skin for skin in data['pet_skins']['skin']}

	@cached_property
	def skill_activation_data(self) -> dict[int, 'SpMovesItem']:
		data: SpHideMovesConfig = self._get_data('unity', 'spHideMoves.json')
		return {data['moves']: data for data in data['config']['sp_moves']}

	@cached_property
	def pet_encyclopedia_data(self) -> dict[int, dict[str, Any]]:
		return {
			book['ID']: book
			for book in self._get_data('flash', 'config.xml.PetBookXMLInfo.xml')[
				'root'
			]['Monster']
		}

	@cached_property
	def pet_archive_story_book_data(self) -> dict[int, 'ArchivesStoryInfo']:
		data: ArchivesStoryConfig = self._get_data('unity', 'archivesStory.json')
		return {book['id']: book for book in data['data']}

	@cached_property
	def pet_soulmark_data(self) -> dict[int, list[int]]:
		soulmark_data: list['EffectIconItem'] = self._get_data(
			'unity', 'effectIcon.json'
		)['root']['effect']

		result = defaultdict(list)
		for data in soulmark_data:
			pet_ids = data['pet_id']
			for pet_id in pet_ids:
				result[pet_id].append(data['id'])

		return dict(result)

	@cached_property
	def eid_to_soulmark_id_map(self) -> dict[int, list[int]]:
		data: list['EffectIconItem'] = self._get_data('unity', 'effectIcon.json')[
			'root'
		]['effect']
		result = defaultdict(list)
		for item in data:
			result[item['effect_id']].append(item['id'])

		return dict(result)

	@cached_property
	def pet_left_and_right_data(self) -> dict[int, int]:
		data = self._get_data('flash', 'config.xml.PetLeftAndRightXmlInfo_petClass.xml')
		return {int(key): value for key, value in data.items() if key.isdigit()}

	@cached_property
	def pet_advance_data(self) -> dict[int, 'AwakenDetailTaskItem']:
		data: list['AwakenDetailTaskItem'] = self._get_data(
			'unity', 'awakenDetail.json'
		)['root']['task']

		result = {}
		for task in data:
			if not (advances := task['advances']):
				continue

			result[advances['monster_id']] = task

		return result

	@cached_property
	def pet_advanced_skill_set(self) -> set[int]:
		data = self.pet_advance_data.values()
		result: set[int] = set()
		for task in data:
			if not (advances := task['advances']):
				continue

			if advances['ex_move']:
				result.add(advances['ex_move']['extra_moves'])

			if advances['sp_move']:
				result.update(advances['sp_move']['sp_moves'])

		return result
