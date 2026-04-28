"""Helper 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class HelperInfo(TypedDict):
	"""Helper 帮助信息条目"""

	group: int
	id: int
	jump: str
	node: str
	picture: str
	searchword: str
	text: str
	title: str
	type: int


class HelperConfig(TypedDict):
	"""Helper 配置数据"""

	data: list[HelperInfo]


class HelperParser(BaseParser[HelperConfig]):
	"""解析 helper.bytes 配置文件"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'helper.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'helper.json'

	def parse(self, data: bytes) -> HelperConfig:
		reader = BytesReader(data)
		result = HelperConfig(data=[])

		# 检查是否有数据
		if not reader.ReadBoolean():
			return result

		# 读取数组长度
		count = reader.ReadSignedInt()

		# 循环读取每个 HelperInfo
		for _ in range(count):
			# 按照 IHelperInfo.Parse 方法的读取顺序
			group = reader.ReadSignedInt()
			id_val = reader.ReadSignedInt()
			jump = reader.ReadUTFBytesWithLength()
			node = reader.ReadUTFBytesWithLength()
			picture = reader.ReadUTFBytesWithLength()
			searchword = reader.ReadUTFBytesWithLength()
			text = reader.ReadUTFBytesWithLength()
			title = reader.ReadUTFBytesWithLength()
			type_val = reader.ReadSignedInt()

			result['data'].append(
				HelperInfo(
					group=group,
					id=id_val,
					jump=jump,
					node=node,
					picture=picture,
					searchword=searchword,
					text=text,
					title=title,
					type=type_val,
				)
			)

		return result
