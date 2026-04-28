"""物品用户信息相关配置解析器

解析赛尔号客户端的物品用户信息数据文件。
"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 物品项数据结构
class ItemItem(TypedDict):
	"""物品用户信息项"""

	desc: str
	itemid: int
	type: int


# 根容器结构
class _Root(TypedDict):
	"""根容器"""

	item: list[ItemItem]


# 顶层数据结构
class ItemUserInfoConfig(TypedDict):
	"""物品用户信息配置数据"""

	root: _Root


class ItemUserInfoParser(BaseParser[ItemUserInfoConfig]):
	"""物品用户信息配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'item_user_info.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemUserInfo.json'

	def parse(self, data: bytes) -> ItemUserInfoConfig:
		reader = BytesReader(data)
		result: ItemUserInfoConfig = {'root': {'item': []}}

		# 检查是否有数据
		if not reader.ReadBoolean():
			return result

		# 解析物品数组
		if reader.ReadBoolean():
			item_count = reader.ReadSignedInt()
			for _ in range(item_count):
				# 严格按照 C# Parse 方法的顺序读取
				item: ItemItem = {
					'type': reader.ReadSignedInt(),
					'desc': reader.ReadUTFBytesWithLength(),
					'itemid': reader.ReadSignedInt(),
				}
				result['root']['item'].append(item)

		return result
