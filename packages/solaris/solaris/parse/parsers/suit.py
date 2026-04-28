"""套装相关配置解析器

解析赛尔号客户端的套装数据文件，包含套装项信息。
"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 套装项数据结构
class ItemItem(TypedDict):
	"""套装项"""

	name: str
	suitdes: str
	cloths: list[int]
	id: int
	transform: int
	tran_speed: float


# 套装根容器结构
class _Root(TypedDict):
	"""套装根容器"""

	item: list[ItemItem]


# 顶层数据结构
class SuitConfig(TypedDict):
	"""套装配置数据"""

	root: _Root


class SuitParser(BaseParser[SuitConfig]):
	"""套装配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'suit.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'suit.json'

	def parse(self, data: bytes) -> SuitConfig:
		reader = BytesReader(data)
		result: SuitConfig = {'root': {'item': []}}

		# 检查是否有套装数据
		if not reader.ReadBoolean():
			return result

		# 解析套装根容器
		if reader.ReadBoolean():
			item_count = reader.ReadSignedInt()
			for _ in range(item_count):
				# 解析套装项 - 按C#代码顺序读取

				# 解析可选的服装数组
				cloths_list: list[int] = []
				if reader.ReadBoolean():
					cloths_count = reader.ReadSignedInt()
					cloths_list = [reader.ReadSignedInt() for _ in range(cloths_count)]

				id_value = reader.ReadSignedInt()
				name = reader.ReadUTFBytesWithLength()
				suitdes = reader.ReadUTFBytesWithLength()
				tran_speed = reader.ReadFloat()
				transform = reader.ReadSignedInt()

				item: ItemItem = {
					'name': name,
					'suitdes': suitdes,
					'cloths': cloths_list,
					'id': id_value,
					'transform': transform,
					'tran_speed': tran_speed,
				}
				result['root']['item'].append(item)

		return result
