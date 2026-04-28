from typing import Any

from seerapi_models.common import EidEffect, EidEffectInUse, ResourceRef
from seerapi_models.effect import (
	PetEffect,
	PetEffectGroup,
	VariationEffect,
)

from solaris.analyze.base import BaseDataSourceAnalyzer, DataImportConfig
from solaris.analyze.typing_ import AnalyzeResult
from solaris.utils import split_string_arg


def _generate_effect_alias(effect: EidEffectInUse) -> str | None:
	return '_'.join(
		[str(arg) for arg in [effect.effect.id, *(effect.effect_args or [])]]
	)


class NewSeAnalyzer(BaseDataSourceAnalyzer):
	"""分析并提取特性/特质数据"""

	@classmethod
	def get_data_import_config(cls) -> DataImportConfig:
		return DataImportConfig(unity_paths=('new_se.json',))

	@classmethod
	def get_result_res_models(cls):
		return (PetEffect, PetEffectGroup, VariationEffect)

	def analyze(self):
		"""分析特性和特质数据

		处理流程：
		1. 加载 new_se.json 数据
		2. 遍历效果数据，根据 Stat 字段区分类型：
		   - Stat=1: 精灵特性（PetEffect）
		     - 按名称分组到 PetEffectGroup
		     - 包含星级信息
		   - Stat=4: 精灵特质（VariationEffect）
		3. 为每个效果生成别名（用于快速查找）
		4. 建立特性与特性组的双向引用关系

		数据字段说明：
		- Idx: 效果ID
		- Desc: 效果名称
		- Intro/Des: 效果描述
		- Eid: 效果类型ID
		- Args: 效果参数（字符串，需要解析为数字列表）
		- Stat: 效果状态类型（1=特性，4=特质）
		- StarLevel: 星级（仅特性有）

		Returns:
			包含 PetEffect、PetEffectGroup 和 VariationEffect 的分析结果元组
		"""
		# 加载效果数据
		effect_data: list[dict[str, Any]] = self._get_data('unity', 'new_se.json')[
			'NewSe'
		]['NewSeIdx']
		effect_map: dict[int, PetEffect] = {}
		effect_group_map: dict[str, PetEffectGroup] = {}

		variation_map: dict[int, VariationEffect] = {}
		group_id = 1

		for effect in effect_data:
			# 构建效果对象（包含效果ID和参数）
			effect_obj = EidEffectInUse(
				effect=ResourceRef.from_model(EidEffect, id=effect['Eid']),
				effect_args=split_string_arg(effect['Args']),
			)

			# 提取基础数据（特性和特质共用）
			base_data = {
				'id': effect['Idx'],
				'name': effect.get('Desc', ''),
				'desc': effect.get('Intro') or effect.get('Des') or '',
				'effect': effect_obj,
				'effect_alias': _generate_effect_alias(effect_obj),
			}

			# 处理特性（Stat=1）
			if effect['Stat'] == 1:
				name = base_data['name']
				# 如果特性组不存在，则创建新组
				if name not in effect_group_map:
					effect_group_map[name] = PetEffectGroup(
						id=group_id, name=name, effect=[]
					)
					group_id += 1

				# 创建特性对象
				pet_effect = PetEffect(
					**base_data,
					star_level=effect['StarLevel'],
					effect_group=ResourceRef.from_model(effect_group_map[name]),
				)
				effect_map[pet_effect.id] = pet_effect

				# 在特性组中添加对该特性的引用
				effect_group_map[name].effect.append(ResourceRef.from_model(pet_effect))

			# 处理特质（Stat=4）
			elif effect['Stat'] == 4:
				variation = VariationEffect(**base_data)
				variation_map[variation.id] = variation

		return (
			AnalyzeResult(model=PetEffect, data=effect_map),
			AnalyzeResult(
				model=PetEffectGroup,
				data={group.id: group for group in effect_group_map.values()},
			),
			AnalyzeResult(model=VariationEffect, data=variation_map),
		)
