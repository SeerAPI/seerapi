from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 效果增益项结构定义
class EffectBuffItem(TypedDict):
	"""效果增益项数据结构"""

	desc: str
	name: str
	id: int
	kind: int


# 内部根结构
class _Root(TypedDict):
	buff: list[EffectBuffItem]


# 顶层数据结构
class EffectBuffConfig(TypedDict):
	root: _Root


# 效果增益Parser实现
class EffectBuffParser(BaseParser[EffectBuffConfig]):
	"""解析效果增益配置数据"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'effectbuff.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'effectBuff.json'

	def parse(self, data: bytes) -> EffectBuffConfig:
		reader = BytesReader(data)
		result: EffectBuffConfig = {'root': {'buff': []}}

		# 检查根布尔标志
		if not reader.read_bool():
			return result

		# 检查buff数组存在标志
		if not reader.read_bool():
			return result

		# 读取数组数量
		count = reader.read_i32()

		# 循环读取效果增益项（严格按照C#解析顺序）
		for _ in range(count):
			item: EffectBuffItem = {
				'desc': reader.ReadUTFBytesWithLength(),
				'id': reader.read_i32(),
				'kind': reader.read_i32(),
				'name': reader.ReadUTFBytesWithLength(),
			}
			result['root']['buff'].append(item)

		return result
