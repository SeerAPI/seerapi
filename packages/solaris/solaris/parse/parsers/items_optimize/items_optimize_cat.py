from typing import TypedDict

from ...base import BaseParser
from ...bytes_reader import BytesReader


class CatItem(TypedDict):
	"""道具类别项"""

	db_cat_id: int
	id: int
	max: int
	name: str
	url: str


class _Root(TypedDict):
	"""根容器"""

	cats: list[CatItem]


class ItemsOptimizeCatConfig(TypedDict):
	"""顶层数据结构"""

	root: _Root


class ItemsOptimizeCatParser(BaseParser[ItemsOptimizeCatConfig]):
	"""道具优化类别配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCat.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCat.json'

	def parse(self, data: bytes) -> ItemsOptimizeCatConfig:
		reader = BytesReader(data)
		result: ItemsOptimizeCatConfig = {'root': {'cats': []}}

		# 检查头部标志
		if reader.ReadBoolean():
			# 读取类别数量
			count = reader.ReadSignedInt()

			# 循环读取每个类别项
			for _ in range(count):
				cat_item: CatItem = {
					'db_cat_id': reader.ReadSignedInt(),
					'id': reader.ReadSignedInt(),
					'max': reader.ReadUnsignedInt(),
					'name': reader.ReadUTFBytesWithLength(),
					'url': reader.ReadUTFBytesWithLength(),
				}
				result['root']['cats'].append(cat_item)

		return result
