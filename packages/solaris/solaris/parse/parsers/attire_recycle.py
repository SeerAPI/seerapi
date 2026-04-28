from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AttirerecycleItem(TypedDict):
	"""套装回收项目"""

	item_name: str
	id: int
	item_id: int
	output_num: int


class _Attirerecycles(TypedDict):
	"""套装回收集合"""

	attirerecycle: list[AttirerecycleItem]


class AttirerecycleConfig(TypedDict):
	"""顶层数据结构"""

	attirerecycles: _Attirerecycles


class AttirerecycleParser(BaseParser[AttirerecycleConfig]):
	"""套装回收解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'Attirerecycle.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'Attirerecycle.json'

	def parse(self, data: bytes) -> AttirerecycleConfig:
		reader = BytesReader(data)
		result: AttirerecycleConfig = {'attirerecycles': {'attirerecycle': []}}

		# 检查套装回收集合是否存在
		if not reader.ReadBoolean():
			return result

		# 检查项目数组是否存在
		if not reader.ReadBoolean():
			return result

		# 读取项目数量
		count = reader.ReadSignedInt()

		# 读取每个项目
		for _ in range(count):
			# 按照C#代码中的字段顺序读取: ID -> ItemID -> ItemName -> OutputNum
			item: AttirerecycleItem = {
				'id': reader.ReadSignedInt(),
				'item_id': reader.ReadSignedInt(),
				'item_name': reader.ReadUTFBytesWithLength(),
				'output_num': reader.ReadSignedInt(),
			}
			result['attirerecycles']['attirerecycle'].append(item)

		return result
