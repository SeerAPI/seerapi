from typing import TYPE_CHECKING

from seerapi_models.achievement import (
	Achievement,
	AchievementBranch,
	AchievementCategory,
	AchievementType,
	Title,
)
from seerapi_models.achievement import (
	AchievementCategoryNameEnum as CatNameEnum,
)
from seerapi_models.common import ResourceRef, SixAttributes

from solaris.analyze.base import BaseDataSourceAnalyzer, DataImportConfig
from solaris.analyze.typing_ import AnalyzeResult, CsvTable
from solaris.analyze.utils import CategoryMap, create_category_map

if TYPE_CHECKING:
	from solaris.parse.parsers.achievements import AchievementsConfig


def _from_desc_analyze_attr_bonus(desc: str) -> SixAttributes | None:
	"""从描述中分析能力加成属性"""
	if not desc:
		return None

	import re

	attr_mapping = {
		'攻击': 'atk',
		'防御': 'def',
		'特攻': 'sp_atk',
		'特防': 'sp_def',
		'速度': 'spd',
		'体力': 'hp',
	}

	# 初始化属性字典
	attributes: dict[str, int] = dict.fromkeys(attr_mapping.values(), 0)
	percent = False

	match = re.search(r'全属性[+＋](\d+)', desc)
	if match:
		kwargs: dict[str, int] = dict.fromkeys(
			attr_mapping.values(), int(match.group(1))
		)
		return SixAttributes(**kwargs, percent=False)

	# 批量匹配所有属性
	for chinese_name, english_name in attr_mapping.items():
		match = re.search(rf'{chinese_name}[+＋](\d+)', desc)
		if match:
			value = int(match.group(1))
			# 检查是否有百分比符号
			percent_match = re.search(rf'{chinese_name}[+＋]\d+%', desc)
			if percent_match:
				# 如果有百分比符号，设置百分比标签
				percent = True

			attributes[english_name] = value

	# 如果没有匹配到任何属性，返回None
	if not any(attributes.values()):
		return None

	attr_bonus = SixAttributes(**attributes, percent=percent)
	return attr_bonus


def _achievement_classifier(achievement: Achievement) -> set[CatNameEnum]:
	"""根据成就分类器"""
	category_names = set[CatNameEnum]()
	if achievement.is_hide:
		category_names.add(CatNameEnum.hide_achievement)
	if achievement.is_ability_bonus:
		category_names.add(CatNameEnum.ability_achievement)

	return category_names


def _achievement_id_generator(type_id: int, branch_id: int, achievement_id: int) -> int:
	return (type_id + 1) * 1000000 + branch_id * 1000 + achievement_id


CATEGORY_NAME_MAP: CsvTable[dict] = {
	id_: {'id': id_, 'name': enum.value} for id_, enum in enumerate(CatNameEnum)
}


CATEGORY_ID_MAP: dict[CatNameEnum, int] = {
	enum.value: id_ for id_, enum in enumerate(CatNameEnum)
}


class AchievementAnalyzer(BaseDataSourceAnalyzer):
	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		return DataImportConfig(
			unity_paths=('achievements.json',),
		)

	@classmethod
	def get_result_res_models(cls):
		return (
			Achievement,
			AchievementBranch,
			AchievementType,
			AchievementCategory,
			Title,
		)

	def analyze(self):
		data: 'AchievementsConfig' = self._get_data('unity', 'achievements.json')
		achievement_map: dict[int, Achievement] = {}
		title_map: dict[int, Title] = {}
		achievement_branch_map: dict[int, AchievementBranch] = {}
		achievement_type_map: dict[int, AchievementType] = {}
		category_map: CategoryMap[int, AchievementCategory, ResourceRef] = (
			create_category_map(
				CATEGORY_NAME_MAP,
				model_cls=AchievementCategory,
				array_key='achievement',
			)
		)
		for type_ in data['achievement_rules']['type']:
			type_id = type_['id']
			type_model = AchievementType(
				id=type_id,
				name=type_['desc'],
				point_total=0,
			)
			for branch_ in type_['branches']:
				for rule_ in branch_['branch']:
					branch_point_total = 0
					branch_id = rule_['id']
					branch_model = AchievementBranch(
						id=branch_id,
						name=rule_['desc'],
						point_total=0,
						is_series=rule_['is_show_pro'] == 1,
						type=ResourceRef.from_model(AchievementType, id=type_id),
					)
					for achievement in rule_['rule']:
						achievement_id = _achievement_id_generator(
							type_id, branch_id, achievement['id']
						)
						original_title = achievement['title']
						title = original_title.replace('|', '')
						name = achievement['ach_name']
						if not name and achievement['hide'] != 1:
							name = rule_['desc']

						achievement_model = Achievement(
							id=achievement_id,
							title_id=achievement['spe_name_bonus'] or None,
							name=name,
							point=achievement['achievement_point'],
							desc=achievement['desc'],
							original_title=original_title or None,
							title=title or None,
							is_ability_bonus=achievement['ability_title'] == 1,
							ability_desc=achievement['abtext'] or None,
							is_hide=achievement['hide'] == 1,
							type=ResourceRef.from_model(AchievementType, id=type_id),
							branch=ResourceRef.from_model(
								AchievementBranch, id=branch_id
							),
							attr_bonus=_from_desc_analyze_attr_bonus(
								achievement['abtext']
							),
						)

						# 有两个title_id为79的称号，为其中一个分配新序号解决这个问题
						if (
							achievement_model.title_id == 79
							and achievement_model.name == '战斗圣光斗士'
						):
							achievement_model.title_id = 10079

						title_model = achievement_model.to_title()
						if title_model is not None:
							title_map[title_model.id] = title_model
						ref = ResourceRef.from_model(achievement_model)
						category_names = _achievement_classifier(achievement_model)
						for category_name in category_names:
							category_map.add_element(
								CATEGORY_ID_MAP[category_name], ref
							)

						achievement_map[achievement_id] = achievement_model
						branch_point_total += achievement_model.point
						branch_model.achievement.append(ref)

					branch_model.point_total = branch_point_total
					type_model.point_total += branch_model.point_total
					type_model.branch.append(ResourceRef.from_model(branch_model))
					achievement_branch_map[branch_id] = branch_model

			achievement_type_map[type_id] = type_model

		# 添加下一级成就和上一级成就
		for achievement in achievement_branch_map.values():
			if not achievement.is_series:
				continue
			for prev_ref, next_ref in zip(
				achievement.achievement, achievement.achievement[1:]
			):
				prev_model = achievement_map[prev_ref.id]
				next_model = achievement_map[next_ref.id]
				prev_model.next_level_achievement = next_ref
				next_model.prev_level_achievement = prev_ref

		for category in category_map.values():
			category.name = category.name.value
		return (
			AnalyzeResult(Achievement, achievement_map),
			AnalyzeResult(AchievementBranch, achievement_branch_map),
			AnalyzeResult(AchievementType, achievement_type_map),
			AnalyzeResult(AchievementCategory, category_map, output_mode='json'),
			AnalyzeResult(Title, title_map, output_mode='json'),
		)
