from typing import Any

from seerapi_models import PeakPoolVote, PetAdvance
from seerapi_models.common import ResourceRef, SixAttributes
from seerapi_models.element_type import TypeCombination
from seerapi_models.items import SkillActivationItem
from seerapi_models.peak_pool import PeakExpertPool, PeakPool
from seerapi_models.pet import (
	Pet,
	PetArchiveStoryEntry,
	PetClass,
	PetEncyclopediaEntry,
	PetGenderCategory,
	PetMountTypeCategory,
	PetVipBuffCategory,
	SkillInPet,
	Soulmark,
)
from seerapi_models.pet.pet import DiyStatsRange
from seerapi_models.skill import Skill

from solaris.analyze.analyzers.peak_pool import PeakPoolAnalyzer
from solaris.analyze.typing_ import AnalyzeResult, CsvTable
from solaris.analyze.utils import CategoryMap, create_category_map
from solaris.utils import get_nested_value

from ._general import BasePetAnalyzer


def _handle_yielding_ev(value: str | int) -> SixAttributes:
	if isinstance(value, str):
		if len(value) <= 6:
			value = ' '.join(s for s in value)
		return SixAttributes.from_string(value, hp_first=True)
	return SixAttributes.from_list(
		[int(s) for s in str(value).rjust(6, '0')],
		hp_first=True,
	)


def _deduplicate_pet_skills_by_id(
	skill_resources: list[SkillInPet],
) -> list[SkillInPet]:
	"""根据 skill.id 去重，保留第一个出现的"""
	seen_skill_ids = set()
	unique_skill_resources = []
	for item in skill_resources:
		skill_id = item.skill.id
		if skill_id not in seen_skill_ids:
			seen_skill_ids.add(skill_id)
			unique_skill_resources.append(item)
	return unique_skill_resources


class PetAnalyzer(BasePetAnalyzer):
	@classmethod
	def get_result_res_models(cls):
		return (
			Pet,
			PetClass,
			PetGenderCategory,
			PetVipBuffCategory,
			PetMountTypeCategory,
		)

	def get_skill_activation_item(
		self, skill_id: int, pet_id: int
	) -> ResourceRef['SkillActivationItem'] | None:
		if skill_id in self.skill_activation_data:
			data = self.skill_activation_data[skill_id]
			if data['monster'] == pet_id:
				return ResourceRef.from_model(SkillActivationItem, id=data['item'])
		return None

	def extract_skills_from_list(
		self,
		pet_id: int,
		skills_data: list | dict | None,
		*,
		is_special: bool = False,
		is_advanced: bool = False,
		is_fifth: bool = False,
	) -> list[SkillInPet]:
		"""从技能数据中生成SkillInPet列表"""
		if not skills_data:
			return []

		# 确保数据是列表格式
		if isinstance(skills_data, dict):
			skills_data = [skills_data]

		result: list[SkillInPet] = []
		skill_id_set: set[int] = set()
		for skill_data in skills_data:
			skill_id = skill_data['id']
			learning_level = skill_data.get('learning_lv')
			data = SkillInPet(
				skill=ResourceRef.from_model(Skill, id=skill_id),
				learning_level=learning_level,
				is_special=is_special,
				is_advanced=is_advanced,
				is_fifth=is_fifth,
				skill_activation_item=self.get_skill_activation_item(skill_id, pet_id),
			)
			if skill_id in skill_id_set:
				continue

			skill_id_set.add(skill_id)
			result.append(data)

		return result

	def analyze(self) -> tuple[AnalyzeResult, ...]:
		pet_gender_table: CsvTable = self._get_data('patch', 'pet_gender.json')
		vipbuff_table: CsvTable = self._get_data('patch', 'pet_vipbuff.json')
		mount_type_table: CsvTable = self._get_data('patch', 'pet_mount_type.json')

		story_entry_data_with_pet_id = {
			v['monid']: v for v in self.pet_archive_story_book_data.values()
		}

		# 记录 PetClass，key为PetClass的ID，value为PetClass对象
		pet_class_map: dict[int, PetClass] = {}
		# 记录性别，key为性别id
		pet_gender_map = create_category_map(
			pet_gender_table, model_cls=PetGenderCategory, array_key='pet'
		)
		# 记录VIP加成，key为buff id
		pet_vipbuff_map = create_category_map(
			vipbuff_table, model_cls=PetVipBuffCategory, array_key='pet'
		)
		# 记录精灵骑乘模式
		pet_mount_type_map: CategoryMap[int, PetMountTypeCategory, Any] = (
			create_category_map(
				mount_type_table, model_cls=PetMountTypeCategory, array_key='pet'
			)
		)
		id_to_peak_pool_map = {
			pet_ref.id: k
			for k, v in self._get_input_data(PeakPoolAnalyzer, PeakPool).items()
			for pet_ref in v.pet
		}
		id_to_peak_expert_pool_map = {
			pet_ref.id: k
			for k, v in self._get_input_data(PeakPoolAnalyzer, PeakExpertPool).items()
			for pet_ref in v.pet
		}
		id_to_peak_pool_vote_map = {
			pet_ref.id: k
			for k, v in self._get_input_data(PeakPoolAnalyzer, PeakPoolVote).items()
			for pet_ref in v.pet
		}

		pet_map = {}
		for pet_id, pet_dict in self.pet_origin_data.items():
			if pet_id > 9999:
				break
			pet_name = pet_dict['def_name']
			pet_ref = ResourceRef.from_model(Pet, id=pet_id)
			pet_type = ResourceRef.from_model(TypeCombination, id=pet_dict['type'])
			pet_gender_id = pet_dict.get('gender', 0)
			if pet_gender_id > 2:
				pet_gender_id = 0
			pet_gender_ref = ResourceRef.from_model(pet_gender_map[pet_gender_id])
			releaseable = not bool(pet_dict.get('free_forbidden', 0))
			# 处理精灵类别
			cls_info = {
				'is_rare_pet': bool(pet_dict.get('IsRareMon', False)),
				'is_variant_pet': bool(pet_dict.get('IsAbilityMon', False)),
				'is_breeding_pet': bool(pet_dict.get('BreedingMon', False)),
				'is_fusion_pet': bool(pet_dict.get('IsFuseMon', False)),
			}
			if vipbuff_id := int(pet_dict.get('VipBtlAdj', 0)):
				if vipbuff_id == 1:
					cls_info['is_shine_pet'] = True
				elif vipbuff_id == 2:
					cls_info['is_dark_pet'] = True
				else:
					raise ValueError(f'Unknown VIP buff ID: {vipbuff_id}')

			pet_cls_ref = None
			evolution_chain_index = 0
			if pet_cls_id := pet_dict.get('pet_class'):
				if pet_cls := pet_class_map.get(pet_cls_id):
					pet_cls.evolution_chain.append(pet_ref)
				else:
					pet_class_map[pet_cls_id] = PetClass(
						id=pet_cls_id,
						evolution_chain=[pet_ref],
						**cls_info,  # type: ignore[arg-type]
					)
				pet_cls = pet_class_map[pet_cls_id]
				pet_cls_ref = ResourceRef.from_model(pet_cls)
				evolution_chain_index = len(pet_cls.evolution_chain) - 1

			# 转换种族值对象
			base_stats = SixAttributes(
				hp=pet_dict['hp'],
				atk=pet_dict['atk'],
				def_=pet_dict['def'],
				sp_atk=pet_dict['sp_atk'],
				sp_def=pet_dict['sp_def'],
				spd=pet_dict['spd'],
			)

			# 转换YieldingEV
			yielding_ev = _handle_yielding_ev(pet_dict['YieldingEV'])

			diy_stats: DiyStatsRange | None = None
			if (diy_min := pet_dict.get('DiyRaceMin')) and (
				diy_max := pet_dict.get('DiyRaceMax')
			):
				diy_stats = DiyStatsRange(
					min=SixAttributes.from_string(diy_min, hp_first=True),
					max=SixAttributes.from_string(diy_max, hp_first=True),
				)
			# 处理坐骑类型
			mount_type = 0
			if pet_dict.get('is_ride_pet', False):
				mount_type = 1
			elif pet_dict.get('is_fly_pet', False):
				mount_type = 2
			mount_type_ref = None
			if mount_type:
				mount_type_ref = ResourceRef.from_model(pet_mount_type_map[mount_type])

			# 准备处理技能相关
			pet_skill_resources: list[SkillInPet] = []
			pet_normal_skills = pet_dict.get('learnable_moves') or pet_dict.get('move')
			if pet_normal_skills:
				# 获取普通技能
				normal_moves = pet_normal_skills.get('move', [])
				pet_skill_resources.extend(
					self.extract_skills_from_list(pet_id, normal_moves)
				)

				# 获取特训技能
				moves = pet_normal_skills.get('sp_move', [])
				pet_skill_resources.extend(
					self.extract_skills_from_list(pet_id, moves, is_special=True)
				)

				# 获取觉醒技能
				moves = pet_normal_skills.get('adv_move', [])
				pet_skill_resources.extend(
					self.extract_skills_from_list(pet_id, moves, is_advanced=True)
				)

			# 获取第五技能
			if fifth_skill := get_nested_value(pet_dict, 'extra_moves.move'):
				pet_skill_resources.extend(
					self.extract_skills_from_list(
						pet_id,
						fifth_skill,
						is_fifth=True,
						is_special=False,
					)
				)

			# 获取特训/觉醒第五技能（U端特训/觉醒第五在同一个字段中，需要单独分辨）
			moves = get_nested_value(pet_dict, 'sp_extra_moves.move') or []
			for move in moves:
				if move['id'] in self.pet_advanced_skill_set:
					kw = {'is_advanced': True}
				else:
					kw = {'is_special': True}
				pet_skill_resources.extend(
					self.extract_skills_from_list(pet_id, move, is_fifth=True, **kw)
				)

			moves = get_nested_value(pet_dict, 'show_extra_moves.move') or []
			for move in moves:
				pet_skill_resources.extend(
					self.extract_skills_from_list(
						pet_id, move, is_fifth=True, is_special=True
					)
				)

			pet_skill_resources = _deduplicate_pet_skills_by_id(pet_skill_resources)

			encyclopedia_entry = None
			if pet_id in self.pet_encyclopedia_data:
				encyclopedia_entry = ResourceRef.from_model(
					PetEncyclopediaEntry,
					id=pet_id,
				)

			archive_story_entry = None
			if pet_id in story_entry_data_with_pet_id:
				story_entry_data = story_entry_data_with_pet_id[pet_id]
				archive_story_entry = ResourceRef.from_model(
					PetArchiveStoryEntry,
					id=story_entry_data['id'],
				)

			advance = None
			if advance_data := self.pet_advance_data.get(pet_id):
				advance = ResourceRef.from_model(PetAdvance, id=advance_data['id'])

			pet_resource = Pet(
				id=pet_id,
				name=pet_name,
				type=pet_type,
				gender=pet_gender_ref,
				base_stats=base_stats,
				evolving_lv=pet_dict.get('evolving_lv'),
				pet_class=pet_cls_ref,
				evolution_chain_index=evolution_chain_index,
				yielding_exp=pet_dict['YieldingExp'],
				yielding_ev=yielding_ev,
				catch_rate=pet_dict['CatchRate'],
				vipbuff=ResourceRef.from_model(pet_vipbuff_map[vipbuff_id])
				if vipbuff_id
				else None,
				mount_type=mount_type_ref,
				diy_stats=diy_stats,
				releaseable=releaseable,
				fusion_master=pet_dict.get('FuseMaster', False),
				fusion_sub=pet_dict.get('FuseSub', False),
				has_resistance=bool(pet_dict.get('Resist', 0)),
				skill=pet_skill_resources,
				soulmark=[
					ResourceRef.from_model(Soulmark, id=soulmark_id)
					for soulmark_id in self.pet_soulmark_data.get(pet_id, [])
				],
				resource_id=pet_dict.get('real_id') or pet_id,  # TODO: 需要对手侧资源id
				enemy_resource_id=self.pet_left_and_right_data.get(pet_id),
				encyclopedia_entry=encyclopedia_entry,
				archive_story_entry=archive_story_entry,
				advance=advance,
			)
			pet_map[pet_id] = pet_resource
			if (peak_pool_id := id_to_peak_pool_map.get(pet_id)) is not None:
				pet_resource.peak_pool = ResourceRef.from_model(
					PeakPool, id=peak_pool_id
				)
			if (expert_pool_id := id_to_peak_expert_pool_map.get(pet_id)) is not None:
				pet_resource.peak_expert_pool = ResourceRef.from_model(
					PeakExpertPool, id=expert_pool_id
				)
			pet_resource.peak_pool_vote_id = id_to_peak_pool_vote_map.get(pet_id)

			pet_gender_map.add_element(pet_gender_id, pet_ref)
			pet_vipbuff_map.add_element(vipbuff_id, pet_ref)
			pet_mount_type_map.add_element(mount_type, pet_ref)

		return (
			AnalyzeResult(model=Pet, data=pet_map),
			AnalyzeResult(model=PetClass, data=pet_class_map),
			AnalyzeResult(model=PetGenderCategory, data=pet_gender_map),
			AnalyzeResult(model=PetVipBuffCategory, data=pet_vipbuff_map),
			AnalyzeResult(model=PetMountTypeCategory, data=pet_mount_type_map),
		)
