from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class EnergyItem(TypedDict):
	"""能量收集项目"""

	collect_cnt: int
	collect_type: str
	dir: int
	name: str
	type: int
	unit: str


class _Root(TypedDict):
	"""根数据结构"""

	energy: list[EnergyItem]


class EnergyCollectConfig(TypedDict):
	"""顶层数据结构"""

	root: _Root


class EnergyCollectParser(BaseParser[EnergyCollectConfig]):
	"""能量收集解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'energyCollect.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'energyCollect.json'

	def parse(self, data: bytes) -> EnergyCollectConfig:
		reader = BytesReader(data)
		result: EnergyCollectConfig = {'root': {'energy': []}}

		# 检查根数据是否存在
		if not reader.ReadBoolean():
			return result

		# 检查能量数组是否存在
		if not reader.ReadBoolean():
			return result

		# 读取能量项目数量
		count = reader.ReadSignedInt()

		# 读取每个能量项目
		for _ in range(count):
			# 按照C#代码中的字段顺序读取
			item: EnergyItem = {
				'collect_cnt': reader.ReadSignedInt(),
				'collect_type': reader.ReadUTFBytesWithLength(),
				'dir': reader.ReadSignedInt(),
				'name': reader.ReadUTFBytesWithLength(),
				'type': reader.ReadSignedInt(),
				'unit': reader.ReadUTFBytesWithLength(),
			}
			result['root']['energy'].append(item)

		return result
