from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ElementItem(TypedDict):
	"""邮件元素项目"""

	text: str
	id: int
	type: str


class _Elements(TypedDict):
	"""邮件元素集合"""

	element: list[ElementItem]


class _Root(TypedDict):
	"""根数据结构"""

	elements: _Elements


class EmailConfig(TypedDict):
	"""顶层数据结构"""

	root: _Root


class EmailParser(BaseParser[EmailConfig]):
	"""邮件配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'email.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'email.json'

	def parse(self, data: bytes) -> EmailConfig:
		reader = BytesReader(data)
		result: EmailConfig = {'root': {'elements': {'element': []}}}

		# 检查根数据是否存在
		if not reader.ReadBoolean():
			return result

		# 检查元素集合是否存在
		if not reader.ReadBoolean():
			return result

		# 检查element数组是否存在
		if not reader.ReadBoolean():
			return result

		# 读取元素数量
		count = reader.ReadSignedInt()

		# 读取每个元素项
		for _ in range(count):
			# 按照C#代码中的字段顺序读取: _text -> id -> type
			element_item: ElementItem = {
				'text': reader.ReadUTFBytesWithLength(),
				'id': reader.ReadSignedInt(),
				'type': reader.ReadUTFBytesWithLength(),
			}
			result['root']['elements']['element'].append(element_item)

		return result
