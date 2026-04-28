from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ItemItem(TypedDict):
	"""活动时间控制项目"""

	end_time: str
	id: int
	start_time: str


class _Config(TypedDict):
	"""配置数据结构"""

	item: list[ItemItem]


class ActivityTimeControlConfig(TypedDict):
	"""顶层数据结构"""

	config: _Config


class ActivityTimeControlParser(BaseParser[ActivityTimeControlConfig]):
	"""活动时间控制解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'activityTimeControl.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'activityTimeControl.json'

	def parse(self, data: bytes) -> ActivityTimeControlConfig:
		reader = BytesReader(data)
		result: ActivityTimeControlConfig = {'config': {'item': []}}

		# 检查配置数据是否存在
		if not reader.ReadBoolean():
			return result

		# 检查项目数组是否存在
		if not reader.ReadBoolean():
			return result

		# 读取项目数量
		count = reader.ReadSignedInt()

		# 读取每个项目
		for _ in range(count):
			# 按照C#代码中的字段顺序读取: endTime -> id -> startTime
			item: ItemItem = {
				'end_time': reader.ReadUTFBytesWithLength(),
				'id': reader.ReadSignedInt(),
				'start_time': reader.ReadUTFBytesWithLength(),
			}
			result['config']['item'].append(item)

		return result
