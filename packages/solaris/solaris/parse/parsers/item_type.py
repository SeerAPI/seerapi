"""物品类型相关配置解析器

解析赛尔号客户端的物品类型数据文件。
"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 物品项数据结构
class ItemItem(TypedDict):
	"""物品类型项"""

	id: int


# 列表项数据结构
class ListItem(TypedDict):
	"""类型列表项"""

	item: list[ItemItem]
	type: int


# 根容器结构
class _Root(TypedDict):
	"""根容器"""

	list: list[ListItem]


# 顶层数据结构
class ItemTypeConfig(TypedDict):
	"""物品类型配置数据"""

	root: _Root


class ItemTypeParser(BaseParser[ItemTypeConfig]):
	"""物品类型配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemType.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemType.json'

	def parse(self, data: bytes) -> ItemTypeConfig:
		reader = BytesReader(data)
		result: ItemTypeConfig = {'root': {'list': []}}

		# 检查是否有数据
		if not reader.ReadBoolean():
			return result

		# 解析列表数组
		if reader.ReadBoolean():
			list_count = reader.ReadSignedInt()
			for _ in range(list_count):
				# 解析 ListItem

				# 可选的物品数组
				item_list: list[ItemItem] = []
				if reader.ReadBoolean():
					item_count = reader.ReadSignedInt()
					for _ in range(item_count):
						# 解析 ItemItem
						item: ItemItem = {'id': reader.ReadSignedInt()}
						item_list.append(item)

				# 类型字段
				type_value = reader.ReadSignedInt()

				list_item: ListItem = {'item': item_list, 'type': type_value}
				result['root']['list'].append(list_item)

		return result
