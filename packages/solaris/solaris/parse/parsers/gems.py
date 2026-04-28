from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _Effect(TypedDict):
	effect_id: int
	param: list[int]


class _SkillEffectsItem(TypedDict):
	effect: _Effect | None


class GemItem(TypedDict):
	category: int
	decompose_prob: int
	des: str
	equit_lv1_cnt1: int
	id: int
	lv: int
	name: str
	skill_effects: list[_SkillEffectsItem]
	upgrade_gem_id: int


class _Gems(TypedDict):
	gem: list[GemItem]


class GemsConfig(TypedDict):
	gems: _Gems


class GemsParser(BaseParser[GemsConfig]):
	@classmethod
	def source_config_filename(cls) -> str:
		return 'gems.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'gems.json'

	def parse(self, data: bytes) -> GemsConfig:
		reader = BytesReader(data)
		result: GemsConfig = {'gems': {'gem': []}}

		if not (reader.read_bool() and reader.read_bool()):
			return result

		gem_count = reader.read_i32()
		for _ in range(gem_count):
			# 按 C# 顺序读取基础字段
			category = reader.read_i32()
			decompose_prob = reader.read_i32()
			des = reader.ReadUTFBytesWithLength()
			equit_lv1_cnt1 = reader.read_i32()
			gid = reader.read_i32()
			lv = reader.read_i32()
			name = reader.ReadUTFBytesWithLength()

			# 读取可选的 SkillEffects 数组
			skill_effects: list[_SkillEffectsItem] = []
			if reader.read_bool():
				skill_count = reader.read_i32()
				for _ in range(skill_count):
					effect: _Effect | None = None
					if reader.read_bool():
						effect_id = reader.read_i32()
						param: list[int] = []
						if reader.read_bool():
							param_count = reader.read_i32()
							param = [reader.read_i32() for _ in range(param_count)]
						effect = {'effect_id': effect_id, 'param': param}
					skill_effects.append({'effect': effect})

			upgrade_gem_id = reader.read_i32()

			gem_item: GemItem = {
				'category': category,
				'decompose_prob': decompose_prob,
				'des': des,
				'equit_lv1_cnt1': equit_lv1_cnt1,
				'id': gid,
				'lv': lv,
				'name': name,
				'skill_effects': skill_effects,
				'upgrade_gem_id': upgrade_gem_id,
			}
			result['gems']['gem'].append(gem_item)

		return result
