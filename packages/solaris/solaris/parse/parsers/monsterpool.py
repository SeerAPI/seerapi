"""
解析赛尔号客户端的精灵抽奖池数据文件。
"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 精灵池物品数据结构
class ItemItem(TypedDict):
	"""精灵池物品项"""

	monstername: str
	isjustone: int
	kind: int
	monsterid: int


# 精灵池项数据结构
class PoolItem(TypedDict):
	"""精灵池项"""

	item: list[ItemItem]
	id: int


# 精灵池根容器结构
class _Root(TypedDict):
	"""精灵池根容器"""

	pool: list[PoolItem]


# 顶层数据结构
class MonsterpoolConfig(TypedDict):
	"""精灵池配置数据"""

	root: _Root


class MonsterpoolParser(BaseParser[MonsterpoolConfig]):
	"""精灵池配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'Monsterpool.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'monsterpool.json'

	def parse(self, data: bytes) -> MonsterpoolConfig:
		reader = BytesReader(data)
		result: MonsterpoolConfig = {'root': {'pool': []}}

		# 检查是否有精灵池数据
		if not reader.ReadBoolean():
			return result

		# 解析精灵池根容器
		if reader.ReadBoolean():
			pool_count = reader.ReadSignedInt()
			for _ in range(pool_count):
				# 解析精灵池项 - 按 C# 代码顺序读取
				pool_id = reader.ReadSignedInt()

				# 解析可选的物品数组
				item_list: list[ItemItem] = []
				if reader.ReadBoolean():
					item_count = reader.ReadSignedInt()
					for _ in range(item_count):
						# 解析物品项 - 按 C# 代码顺序读取
						isjustone = reader.ReadSignedInt()
						kind = reader.ReadSignedInt()
						monsterid = reader.ReadSignedInt()
						monstername = reader.ReadUTFBytesWithLength()

						item: ItemItem = {
							'monstername': monstername,
							'isjustone': isjustone,
							'kind': kind,
							'monsterid': monsterid,
						}
						item_list.append(item)

				pool_item: PoolItem = {'item': item_list, 'id': pool_id}
				result['root']['pool'].append(pool_item)

		return result
