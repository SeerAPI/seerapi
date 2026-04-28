from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AttireconversionItem(TypedDict):
	"""套装转换项目"""

	exchange_num: int
	id: int
	platform: int
	reward_id: int
	reward_num: int
	sub_num: int
	user_info: int


class _Attireconversions(TypedDict):
	"""套装转换集合"""

	attireconversion: list[AttireconversionItem]


class AttireconversionConfig(TypedDict):
	"""顶层数据结构"""

	attireconversions: _Attireconversions


class AttireconversionParser(BaseParser[AttireconversionConfig]):
	"""套装转换解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'Attireconversion.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'Attireconversion.json'

	def parse(self, data: bytes) -> AttireconversionConfig:
		reader = BytesReader(data)
		result: AttireconversionConfig = {'attireconversions': {'attireconversion': []}}

		# 检查套装转换集合是否存在
		if not reader.ReadBoolean():
			return result

		# 检查项目数组是否存在
		if not reader.ReadBoolean():
			return result

		# 读取项目数量
		count = reader.ReadSignedInt()

		# 读取每个项目
		for _ in range(count):
			# 按照C#代码中的字段顺序读取
			item: AttireconversionItem = {
				'exchange_num': reader.ReadSignedInt(),
				'id': reader.ReadSignedInt(),
				'platform': reader.ReadSignedInt(),
				'reward_id': reader.ReadSignedInt(),
				'reward_num': reader.ReadSignedInt(),
				'sub_num': reader.ReadSignedInt(),
				'user_info': reader.ReadSignedInt(),
			}
			result['attireconversions']['attireconversion'].append(item)

		return result
