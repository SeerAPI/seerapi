from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 效果描述项结构定义
class EffectDesItem(TypedDict):
	"""效果描述项数据结构"""

	desc: str
	kinddes: str
	monster: str
	icon: int
	id: int
	kind: int
	tab: int
	link: str


# 内部根结构
class _Root(TypedDict):
	item: list[EffectDesItem]


# 顶层数据结构
class EffectDesConfig(TypedDict):
	root: _Root


# 效果描述Parser实现
class EffectDesParser(BaseParser[EffectDesConfig]):
	"""解析效果描述配置数据"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'effectDes.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'effectDes.json'

	def parse(self, data: bytes) -> EffectDesConfig:
		reader = BytesReader(data)
		result: EffectDesConfig = {'root': {'item': []}}

		# 检查根布尔标志
		if not reader.read_bool():
			return result

		# 检查item数组存在标志
		if not reader.read_bool():
			return result

		# 读取数组数量
		count = reader.read_i32()

		# 循环读取效果描述项（严格按照C#解析顺序）
		for _ in range(count):
			item: EffectDesItem = {
				'desc': reader.read_utf(reader.read_u16()),  # desc: 先读长度再读字符串
				'icon': reader.read_i32(),  # icon
				'id': reader.read_i32(),  # id
				'kind': reader.read_i32(),  # kind
				'kinddes': reader.read_utf(
					reader.read_u16()
				),  # kinddes: 先读长度再读字符串
				'link': reader.ReadUTFBytesWithLength(),
				'monster': reader.read_utf(
					reader.read_u16()
				),  # monster: 先读长度再读字符串
				'tab': reader.read_i32(),  # tab
			}
			result['root']['item'].append(item)

		return result
