"""物品提示相关配置解析器

解析赛尔号客户端的物品提示数据文件。
"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 物品提示项数据结构
class ItemTipItem(TypedDict):
	"""物品提示项"""

	des: str
	id: int


# 根容器结构
class _Root(TypedDict):
	"""根容器"""

	item: list[ItemTipItem]


# 顶层数据结构
class ItemsTipConfig(TypedDict):
	"""物品提示配置数据"""

	root: _Root


class ItemsTipParser(BaseParser[ItemsTipConfig]):
	"""物品提示配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsTip.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsTip.json'

	def parse(self, data: bytes) -> ItemsTipConfig:
		reader = BytesReader(data)
		result: ItemsTipConfig = {'root': {'item': []}}

		# 检查是否有数据
		if not reader.ReadBoolean():
			return result

		# 解析物品数组
		if reader.ReadBoolean():
			item_count = reader.ReadSignedInt()
			for _ in range(item_count):
				# 严格按照 C# Parse 方法的顺序读取
				item: ItemTipItem = {
					'des': reader.ReadUTFBytesWithLength(),
					'id': reader.ReadSignedInt(),
				}
				result['root']['item'].append(item)

		return result
