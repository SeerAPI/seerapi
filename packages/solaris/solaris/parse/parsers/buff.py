"""Buff 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class BuffInfo(TypedDict):
	"""Buff 信息条目"""

	desc: str
	tag: str
	desc_tag: str
	icon: list[int]
	icontype: int
	id: int


class BuffConfig(TypedDict):
	"""Buff 配置数据"""

	data: list[BuffInfo]


class BuffParser(BaseParser[BuffConfig]):
	"""解析 buff.bytes 配置文件"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'buff.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'buff.json'

	def parse(self, data: bytes) -> BuffConfig:
		reader = BytesReader(data)
		result = BuffConfig(data=[])

		# 检查是否有数据
		if not reader.ReadBoolean():
			return result

		# 读取数组长度
		count = reader.ReadSignedInt()

		# 循环读取每个 BuffInfo
		for _ in range(count):
			# 按照 IBuffInfo.Parse 方法的读取顺序
			desc = reader.ReadUTFBytesWithLength()
			tag = reader.ReadUTFBytesWithLength()
			desc_tag = reader.ReadUTFBytesWithLength()

			# icon 是可选数组
			icon: list[int] = []
			if reader.ReadBoolean():
				icon_count = reader.ReadSignedInt()
				icon = [reader.ReadSignedInt() for _ in range(icon_count)]

			icontype = reader.ReadSignedInt()
			id_val = reader.ReadSignedInt()

			result['data'].append(
				BuffInfo(
					desc=desc,
					tag=tag,
					desc_tag=desc_tag,
					icon=icon,
					icontype=icontype,
					id=id_val,
				)
			)

		return result
