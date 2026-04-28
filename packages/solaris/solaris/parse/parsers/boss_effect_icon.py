from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# BOSS效果图标项结构定义
class BossEffectItem(TypedDict):
	"""BOSS效果图标项数据结构"""

	args: str
	tips: str
	eid: int
	icon_id: int
	rows: int
	sort: int


# 内部根结构
class _Root(TypedDict):
	boss_effect: list[BossEffectItem]


# 顶层数据结构
class BossEffectIconConfig(TypedDict):
	root: _Root


# BOSS效果图标Parser实现
class BossEffectIconParser(BaseParser[BossEffectIconConfig]):
	"""解析BOSS效果图标配置数据"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'bossEffectIcon.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'bossEffectIcon.json'

	def parse(self, data: bytes) -> BossEffectIconConfig:
		reader = BytesReader(data)
		result: BossEffectIconConfig = {'root': {'boss_effect': []}}

		# 检查根布尔标志
		if not reader.read_bool():
			return result

		# 检查bossEffect数组存在标志
		if not reader.read_bool():
			return result

		# 读取数组数量
		count = reader.read_i32()

		# 循环读取boss效果项
		for _ in range(count):
			item: BossEffectItem = {
				'args': reader.ReadUTFBytesWithLength(),
				'eid': reader.read_i32(),
				'icon_id': reader.read_i32(),
				'rows': reader.read_i32(),
				'sort': reader.read_i32(),
				'tips': reader.ReadUTFBytesWithLength(),
			}
			result['root']['boss_effect'].append(item)

		return result
