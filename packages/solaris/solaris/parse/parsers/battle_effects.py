from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 子效果项结构定义
class SubEffectItem(TypedDict):
	"""子效果项数据结构"""

	efftype: int
	name: str
	id: int
	ctrl: int
	dependent: int
	derivation: int
	restriction: int
	unctrl: int
	undependent: int
	underivation: int
	unrestriction: int
	unweaken: int
	weaken: int


# 战斗效果项结构定义
class BattleEffectItem(TypedDict):
	"""战斗效果项数据结构"""

	sub_effect: list[SubEffectItem]
	type: int


# 战斗效果容器结构
class _BattleEffects(TypedDict):
	battle_effect: list[BattleEffectItem]


# 顶层数据结构
class BattleEffectsConfig(TypedDict):
	battle_effects: _BattleEffects


# 战斗效果Parser实现
class BattleEffectsParser(BaseParser[BattleEffectsConfig]):
	"""解析战斗效果配置数据"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'battle_effects.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'battleEffects.json'

	def parse(self, data: bytes) -> BattleEffectsConfig:
		"""解析战斗效果二进制数据

		数据结构说明：
		- 根布尔标志：标识是否有数据
		- BattleEffects存在标志：标识战斗效果容器是否存在
		- BattleEffect数组：包含多个战斗效果项
		  - 每个战斗效果项包含：
		    - SubEffect数组：子效果列表（可选）
		      - efftype: 效果类型ID
		      - id: 效果ID
		      - name: 效果名称
		    - type: 战斗效果类型

		Args:
			data: 二进制数据

		Returns:
			解析后的战斗效果配置数据
		"""
		reader = BytesReader(data)
		result: BattleEffectsConfig = {'battle_effects': {'battle_effect': []}}

		# 检查根布尔标志
		if not reader.read_bool():
			return result

		# 检查BattleEffects存在标志
		if not reader.read_bool():
			return result

		# 读取BattleEffect数组数量
		count = reader.read_i32()

		# 循环读取战斗效果项
		for _ in range(count):
			sub_effects: list[SubEffectItem] = []
			# 检查SubEffect数组存在标志
			if reader.read_bool():
				sub_count = reader.read_i32()
				for _ in range(sub_count):
					sub_item: SubEffectItem = {
						'ctrl': reader.read_i32(),
						'dependent': reader.read_i32(),
						'derivation': reader.read_i32(),
						'efftype': reader.read_i32(),
						'id': reader.read_i32(),
						'name': reader.ReadUTFBytesWithLength(),
						'restriction': reader.read_i32(),
						'unctrl': reader.read_i32(),
						'undependent': reader.read_i32(),
						'underivation': reader.read_i32(),
						'unrestriction': reader.read_i32(),
						'unweaken': reader.read_i32(),
						'weaken': reader.read_i32(),
					}
					sub_effects.append(sub_item)

			# 构建战斗效果项
			battle_item: BattleEffectItem = {
				'sub_effect': sub_effects,
				'type': reader.read_i32(),
			}
			result['battle_effects']['battle_effect'].append(battle_item)

		return result
