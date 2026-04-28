from functools import cached_property
from string import Formatter
from typing import TYPE_CHECKING

from seerapi_models import PetAdvance
from seerapi_models.common import ResourceRef, SkillEffectInUse
from seerapi_models.element_type import TypeCombination
from seerapi_models.skill import (
	Skill,
	SkillCategory,
	SkillEffectParam,
	SkillEffectParamInType,
	SkillEffectType,
	SkillEffectTypeTag,
	SkillHideEffect,
)

from solaris.analyze.analyzers.element_type import ElementTypeAnalyzer
from solaris.analyze.analyzers.pet.pet_advance import PetAdvanceAnalyzer
from solaris.analyze.base import (
	BaseAnalyzer,
	BaseDataSourcePostAnalyzer,
	DataImportConfig,
)
from solaris.analyze.typing_ import AnalyzeResult
from solaris.analyze.utils import CategoryMap, create_category_map

from .effect_handlers import (
	INFO_HANDLER_MAP,
	EffectArgs,
	InfoArgs,
	effect_handler_default,
)

if TYPE_CHECKING:
	from solaris.parse.parsers.effect_info import EffectInfoItem, ParamTypeItem
	from solaris.parse.parsers.moves import UnityMoveItem
	from solaris.parse.parsers.skill_effect import SkillEffectItem


_formatter = Formatter()


def _safe_format(template: str, args: list[object] | tuple[object, ...]) -> str:
	"""尽可能多地格式化参数，缺失的占位符保留原样。"""
	parts: list[str] = []
	for literal_text, field_name, _, _ in _formatter.parse(template):
		parts.append(literal_text)
		if field_name is None:
			continue
		try:
			parts.append(str(args[int(field_name)]))
		except (ValueError, IndexError):
			parts.append('{' + field_name + '}')
	return ''.join(parts)


def _slice_args(args: EffectArgs, args_nums: list[int]) -> list[EffectArgs]:
	"""
	将args按args_nums以切片。
	最后一个切片会包含所有剩余的参数。
	"""
	if not args_nums:
		return []

	result = []
	start_index = 0

	# 处理到倒数第二个切片
	for num in args_nums[:-1]:
		end_index = start_index + num
		result.append(args[start_index:end_index])
		start_index = end_index

	# 最后一个切片包含所有剩余的参数
	result.append(args[start_index:])
	return result


def add_condition_labels(
	formatting_adjustment: str, condition_strings: list[str]
) -> str | None:
	import re

	if not formatting_adjustment:
		return None

	if not condition_strings:
		return formatting_adjustment

	result = formatting_adjustment
	for condition in condition_strings:
		# 为每个condition string添加标签包围
		if not condition:
			continue
		pattern = re.escape(condition)
		replacement = f'<condition>{condition}</condition>'
		result = re.sub(pattern, replacement, result)

	return result


class BaseSkillEffectAnalyzer(BaseDataSourcePostAnalyzer):
	@classmethod
	def get_input_analyzers(cls) -> tuple[type[BaseAnalyzer], ...]:
		return (ElementTypeAnalyzer, PetAdvanceAnalyzer)

	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		return DataImportConfig(
			unity_paths=('effectInfo.json', 'skillEffect.json'),
			patch_paths=('skill_effect.json', 'effect_info.json'),
		)

	@cached_property
	def other_effect_map(self) -> dict[int, 'SkillEffectItem']:
		other_effect_data: list['SkillEffectItem'] = self._get_data(
			'unity', 'skillEffect.json'
		)['data']
		return {item['id']: item for item in other_effect_data}

	@cached_property
	def effect_type_tag_map(self) -> dict[str, SkillEffectTypeTag]:
		import anycrc

		crc16 = anycrc.Model('CRC16')
		tag_set = {
			tag
			for key in ('tagA', 'tagB', 'tagC')
			for item in self.other_effect_map.values()
			if (tag := item[key])
		}
		return {
			tag_str: SkillEffectTypeTag(
				id=crc16.calc(tag_str.encode('utf-8')), name=tag_str
			)
			for tag_str in tag_set
		}

	@cached_property
	def effect_param_map(self) -> dict[int, SkillEffectParam]:
		effect_param_data: list['ParamTypeItem'] = self._get_data(
			'unity', 'effectInfo.json'
		)['root']['param_type']

		effect_param_map: dict[int, SkillEffectParam] = {}
		for effect_param in effect_param_data:
			id_ = effect_param['id']
			infos = None
			if param_str := effect_param.get('params'):
				infos = param_str.split('|')
			effect_param_map[id_] = SkillEffectParam(
				id=id_,
				infos=infos,
			)

		return effect_param_map

	@cached_property
	def effect_type_map(self) -> dict[int, SkillEffectType]:
		effect_type_data: list['EffectInfoItem'] = self._get_data(
			'unity', 'effectInfo.json'
		)['root']['effect']

		effect_type_map: dict[int, SkillEffectType] = {}
		for effect_type in effect_type_data:
			if (info := effect_type.get('info')) is None:
				continue
			id_ = effect_type['id']
			params: list[SkillEffectParamInType] | None = None
			if param_list := effect_type['param']:
				params = [
					SkillEffectParamInType(
						position=start_index,
						param=ResourceRef.from_model(self.effect_param_map[id_]),
					)
					for id_, start_index, _ in [
						param_list[i : i + 3] for i in range(0, len(param_list), 3)
					]
				]
			other_effect_data = self.other_effect_map.get(id_)
			other_data_kwargs = {
				'tag': [],
				'pve_effective': False,
			}
			tags = []
			if other_effect_data:
				info_formatting_adj = add_condition_labels(
					other_effect_data['formattingAdjustment'],
					other_effect_data['ifTextItalic'].split('|'),
				)
				tags = [
					self.effect_type_tag_map[tag]
					for index in ('tagA', 'tagB', 'tagC')
					if (tag := other_effect_data[index])
				]
				other_data_kwargs = {
					'info_formatting_adjustment': info_formatting_adj,
					'tag': [ResourceRef.from_model(tag) for tag in tags],
					'pve_effective': not bool(other_effect_data['Bosseffective']),
				}
			skill_effect_type = SkillEffectType(
				id=id_,
				args_num=effect_type['args_num'],
				param=params,
				info=info,
				skill=[],
				analyze_info=effect_type.get('analyze', info),
				**other_data_kwargs,
			)
			for tag in tags:
				tag.effect.append(ResourceRef.from_model(skill_effect_type))

			effect_type_map[id_] = skill_effect_type

		return effect_type_map

	@property
	def type_combination_map(self) -> dict[int, TypeCombination]:
		return self._get_input_data(ElementTypeAnalyzer, TypeCombination)

	@property
	def type_combination_name_map(self) -> dict[int, str]:
		return {
			type_combination.id: type_combination.name
			for type_combination in self.type_combination_map.values()
		}

	def create_skill_effect(
		self, type_ids: list[int], args: EffectArgs
	) -> list[SkillEffectInUse]:
		"""根据效果类型ID和参数列表，创建技能效果对象列表。

		Args:
			type_ids: 技能效果的类型ID列表。
			args: 所有技能效果的参数列表。

		Returns:
			一个包含SkillEffectInUse对象的列表。如果出现未知效果类型或参数错误，则返回空元组。
		"""
		new_type_ids: list[int] = []
		args_nums: list[int] = []
		# 遍历每个效果类型ID，从effect_type_map中获取所需参数数量
		for i in type_ids:
			if i == 0:
				continue
			new_type_ids.append(i)
			args_nums.append(self.effect_type_map[i].args_num)

		# 使用_slice_args辅助函数，根据每个效果所需的参数数量，将扁平的args列表
		# 切分为嵌套列表

		sliced_args: list[list[int]] = _slice_args(list(args), args_nums)
		results = []
		# 遍历切分后的参数和对应的效果类型ID
		for type_id, effect_args in zip(new_type_ids, sliced_args):
			type_ = self.effect_type_map[type_id]
			# info_args用于格式化效果描述字符串，初始值为效果参数的副本
			info_args: InfoArgs = list(effect_args)
			# 处理需要特殊格式化的参数
			for p in type_.param or []:
				param: SkillEffectParam = self.effect_param_map[p.param.id]
				info_args = effect_handler_default(
					effect_args,
					param,
					p.position,
					info_args,
					type_combination_map=self.type_combination_name_map,
				)

			if type_id in INFO_HANDLER_MAP:
				info_args = INFO_HANDLER_MAP[type_id](effect_args, info_args)

			info = _safe_format(type_.info, info_args)
			analyze_info = _safe_format(type_.analyze_info, info_args)

			results.append(
				SkillEffectInUse(
					effect=ResourceRef.from_model(type_),
					args=effect_args,
					info=info,
					analyze_info=analyze_info,
				)
			)

		return results


def clac_crit_rate(crit_rate: int) -> float:
	if crit_rate == 0:
		return 0
	return crit_rate / 16 * 100


class SkillAnalyzer(BaseSkillEffectAnalyzer):
	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		super_config = super().get_data_import_config()
		config = DataImportConfig(
			unity_paths=('moves.json',),
			flash_paths=('config.xml.SkillXMLInfo.xml',),
			patch_paths=(
				'skill_hide_effect.json',
				'skill_category.json',
				'moves.json',
			),
		)
		return super_config + config

	@classmethod
	def get_result_res_models(cls):
		return (
			Skill,
			SkillEffectType,
			SkillEffectParam,
			SkillHideEffect,
			SkillCategory,
			SkillEffectTypeTag,
		)

	@cached_property
	def moves_data(self) -> dict[int, 'UnityMoveItem']:
		unity_data: list['UnityMoveItem'] = self._get_data('unity', 'moves.json')[
			'root'
		]['moves']['move']
		flash_data = self._get_data('flash', 'config.xml.SkillXMLInfo.xml')['root'][
			'item'
		]
		flash_data_map = {i['ID']: i for i in flash_data}

		result = {}
		for move in unity_data:
			move_id = move['id']
			crit_rate = None
			if move['category'] != 4:
				crit_rate = clac_crit_rate(flash_data_map[move_id].get('CritRate', 1))

			result[move_id] = {
				**move,
				'crit_rate': crit_rate,
				**flash_data_map[move_id],
			}

		return result

	def analyze(self) -> tuple[AnalyzeResult, ...]:
		hide_effect_table = self._get_data('patch', 'skill_hide_effect.json')
		category_table = self._get_data('patch', 'skill_category.json')

		skill_data = self.moves_data
		category_map: CategoryMap[int, SkillCategory, ResourceRef] = (
			create_category_map(
				category_table,
				model_cls=SkillCategory,
				array_key='skill',
			)
		)
		hide_effect_map: CategoryMap[int, SkillHideEffect, ResourceRef] = (
			create_category_map(
				hide_effect_table,
				model_cls=SkillHideEffect,
				array_key='skill',
			)
		)
		skill_map: dict[int, Skill] = {}
		for skill_id, skill in skill_data.items():
			skill_name = skill['name']
			skill_type = ResourceRef.from_model(TypeCombination, id=skill['type'])
			skill_category = ResourceRef.from_model(category_map[skill['category']])
			skill_side_effect = self.create_skill_effect(
				skill['side_effect'],
				skill['side_effect_arg'],
			)
			skill_friend_side_effect = self.create_skill_effect(
				skill['friend_side_effect'],
				skill['friend_side_effect_arg'],
			)

			advance: ResourceRef[PetAdvance] | None = None
			advance_resoures = self._get_input_result(PetAdvanceAnalyzer, PetAdvance)
			for _id, advance_resource in advance_resoures.data.items():
				for skill_ref in advance_resource.skill:
					if skill_ref.id == skill_id:
						advance = ResourceRef.from_model(PetAdvance, id=_id)
						break

			skill_model = Skill(
				id=skill_id,
				name=skill_name,
				type=skill_type,
				category=skill_category,
				skill_effect=skill_side_effect,
				friend_skill_effect=skill_friend_side_effect,
				hide_effect=None,
				power=skill['power'],
				max_pp=skill['max_pp'],
				accuracy=skill['accuracy'],
				crit_rate=skill['crit_rate'],
				priority=skill['priority'],
				atk_num=skill['atk_num'] or 1,
				must_hit=bool(skill['must_hit']),
				info=skill['info'] or None,
				advance=advance,
			)
			skill_map[skill_id] = skill_model
			skill_ref = ResourceRef.from_model(skill_model)
			# 将技能添加到技能效果列表
			for effect in skill_model.skill_effect:
				effect_id = effect.effect.id
				self.effect_type_map[effect_id].skill.append(skill_ref)

			# 将技能添加到技能分类
			category_map.add_element(skill_model.category.id, skill_ref)

			# 处理技能隐藏效果
			for id_, effect in hide_effect_table.items():
				original_name = effect['original']
				if enum_value := skill.get(original_name, None):
					# PwrBindDv 有两种效果，对应相同字段的不同的值
					if original_name == 'PwrBindDv':
						hide_effect_id = 7 if enum_value == 1 else 8
					else:
						hide_effect_id = id_
					skill_model.hide_effect = ResourceRef.from_model(
						SkillHideEffect,
						id=hide_effect_id,
					)
					hide_effect_map.add_element(hide_effect_id, skill_ref)
					break

		return (
			AnalyzeResult(model=Skill, data=skill_map),
			AnalyzeResult(model=SkillEffectType, data=self.effect_type_map),
			AnalyzeResult(model=SkillEffectParam, data=self.effect_param_map),
			AnalyzeResult(model=SkillHideEffect, data=hide_effect_map),
			AnalyzeResult(model=SkillCategory, data=category_map),
			AnalyzeResult(
				model=SkillEffectTypeTag,
				data={
					tag.id: tag
					for tag in sorted(  # 不排序的话顺序是随机的，每次运行都不一样
						self.effect_type_tag_map.values(), key=lambda x: x.id
					)
				},
			),
		)
