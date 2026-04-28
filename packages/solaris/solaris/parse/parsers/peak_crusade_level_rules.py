from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PeakCrusadeLevelRuleItem(TypedDict):
	"""巅峰十字军等级规则项"""

	dan_number: int  # 对应 C# 的 danNumber
	ladder_lv: int  # 对应 C# 的 ladderLv
	star: int
	star_lv: int  # 对应 C# 的 starLv
	title: str


class _PeakCrusadeLevelRoot(TypedDict):
	"""巅峰十字军等级规则根节点"""

	item: list[PeakCrusadeLevelRuleItem]


class PeakCrusadeLevelRulesConfig(TypedDict):
	"""巅峰十字军等级规则顶层数据"""

	root: _PeakCrusadeLevelRoot


class PeakCrusadeLevelRulesParser(BaseParser[PeakCrusadeLevelRulesConfig]):
	"""巅峰十字军等级规则配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'peakCrusade_levelRules.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'peakCrusadeLevelRules.json'

	def parse(self, data: bytes) -> PeakCrusadeLevelRulesConfig:
		reader = BytesReader(data)
		result: PeakCrusadeLevelRulesConfig = {'root': {'item': []}}

		# 检查header - 根据IRootInterface.Parse逻辑
		if not reader.ReadBoolean():
			return result

		# 根据IRoot.Parse逻辑，先读布尔标志，然后读item数组
		if reader.ReadBoolean():
			item_count = reader.ReadSignedInt()

			for _ in range(item_count):
				# 按照IItemItem.Parse的顺序读取字段
				dan_number = reader.ReadSignedInt()
				ladder_lv = reader.ReadSignedInt()
				star = reader.ReadSignedInt()
				star_lv = reader.ReadSignedInt()
				title = reader.ReadUTFBytesWithLength()

				item = PeakCrusadeLevelRuleItem(
					dan_number=dan_number,
					ladder_lv=ladder_lv,
					star=star,
					star_lv=star_lv,
					title=title,
				)
				result['root']['item'].append(item)

		return result
