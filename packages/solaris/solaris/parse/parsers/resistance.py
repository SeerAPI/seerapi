from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class HurtItem(TypedDict):
	"""伤害抗性项"""

	level: int
	need: int
	present: int


class _ResistanceRoot(TypedDict):
	"""抗性根节点"""

	hurt: list[HurtItem]  # 伤害数组
	resistance: list[HurtItem]  # 抗性数组


class ResistanceConfig(TypedDict):
	"""抗性顶层数据"""

	root: _ResistanceRoot


class ResistanceParser(BaseParser[ResistanceConfig]):
	"""抗性配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'resistance.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'resistance.json'

	def parse(self, data: bytes) -> ResistanceConfig:
		reader = BytesReader(data)
		result: ResistanceConfig = {'root': {'hurt': [], 'resistance': []}}

		# 检查header - 根据IRootInterface.Parse逻辑
		if not reader.ReadBoolean():
			return result

		# 读取hurt数组 - 根据IRoot.Parse逻辑
		if reader.ReadBoolean():
			hurt_count = reader.ReadSignedInt()

			for _ in range(hurt_count):
				# 按照IHurtItem.Parse的顺序读取字段
				level = reader.ReadSignedInt()
				need = reader.ReadSignedInt()
				present = reader.ReadSignedInt()

				hurt_item = HurtItem(level=level, need=need, present=present)
				result['root']['hurt'].append(hurt_item)

		# 读取resistance数组
		if reader.ReadBoolean():
			resistance_count = reader.ReadSignedInt()

			for _ in range(resistance_count):
				# 按照IHurtItem.Parse的顺序读取字段
				level = reader.ReadSignedInt()
				need = reader.ReadSignedInt()
				present = reader.ReadSignedInt()

				resistance_item = HurtItem(level=level, need=need, present=present)
				result['root']['resistance'].append(resistance_item)

		return result
