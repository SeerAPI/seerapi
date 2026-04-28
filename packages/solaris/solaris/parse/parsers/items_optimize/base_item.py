"""
道具优化解析器基类模块

定义了道具优化解析器的通用结构和基础字段，
用于减少重复代码并提供一致的解析模式。
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from typing_extensions import TypedDict

from ...base import BaseParser
from ...bytes_reader import BytesReader


# 基础道具项类型 - 包含所有道具都有的核心字段
class BaseItemData(TypedDict):
	"""基础道具数据 - 所有道具类别都包含的核心字段"""

	id: int
	name: str
	max: int
	cat_id: int


# 扩展道具项类型 - 包含大部分道具都有的常见字段
class ExtendedItemData(BaseItemData):
	"""扩展道具数据 - 大部分道具类别都包含的常见字段"""

	bean: int
	hide: int
	purpose: int
	sort: int
	use_max: int
	wd: int


TItem = TypeVar('TItem', bound=BaseItemData)


class Item(TypedDict, Generic[TItem]):
	"""道具项"""

	items: list[TItem]


class DataRoot(TypedDict, Generic[TItem]):
	"""数据根节点"""

	root: Item[TItem]


class BaseItemParser(BaseParser[DataRoot[TItem]], ABC):
	"""
	道具优化解析器基类

	提供通用的解析框架和字段读取方法，
	子类只需要实现具体的字段读取逻辑。
	"""

	@abstractmethod
	def parse_item_fields(self, reader: BytesReader) -> TItem:
		"""
		解析单个道具项的字段

		Args:
			reader: 字节读取器

		Returns:
			解析完成的道具项
		"""
		pass

	def parse(self, data: bytes):
		reader = BytesReader(data)
		result: DataRoot[TItem] = {'root': {'items': []}}

		# 检查头部标志
		if reader.ReadBoolean():
			# 读取道具数量
			count = reader.ReadSignedInt()

			# 循环读取每个道具项
			for _ in range(count):
				item = self.parse_item_fields(reader)
				result['root']['items'].append(item)

		return result


# 具体解析器基类 - 处理不同复杂度的道具
class SimpleItemParser(BaseItemParser, ABC):
	"""简单道具解析器基类 - 只包含核心字段"""

	def parse_base_fields(self, reader: BytesReader) -> dict:
		"""解析基础字段 (ID, Max, Name, catID)"""
		return {
			'id': reader.ReadSignedInt(),
			'max': reader.ReadSignedInt(),
			'name': reader.ReadUTFBytesWithLength(),
			'cat_id': reader.ReadSignedInt(),
		}


class ExtendedItemParser(BaseItemParser, ABC):
	"""扩展道具解析器基类 - 包含大部分通用字段"""

	def parse_extended_base_fields(self, reader: BytesReader) -> dict:
		"""解析扩展基础字段"""
		return {
			'bean': reader.ReadSignedInt(),
			'hide': reader.ReadSignedInt(),
			'id': reader.ReadSignedInt(),
			'max': reader.ReadSignedInt(),
			'name': reader.ReadUTFBytesWithLength(),
			'sort': reader.ReadSignedInt(),
			'use_max': reader.ReadSignedInt(),
			'cat_id': reader.ReadSignedInt(),
			'purpose': reader.ReadSignedInt(),
			'wd': reader.ReadSignedInt(),
		}
