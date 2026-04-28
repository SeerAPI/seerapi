from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ErrorpostItem(TypedDict):
	"""错误代码分析项目"""

	event: int
	id: int
	tx: str
	tx_type: int


class _Root(TypedDict):
	"""根数据结构"""

	errorpost: list[ErrorpostItem]


class ErrorCodeAnalysisConfig(TypedDict):
	"""顶层数据结构"""

	root: _Root


class ErrorCodeAnalysisParser(BaseParser[ErrorCodeAnalysisConfig]):
	"""错误代码分析解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'error_code_analysis.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'error_code_analysis.json'

	def parse(self, data: bytes) -> ErrorCodeAnalysisConfig:
		reader = BytesReader(data)
		result: ErrorCodeAnalysisConfig = {'root': {'errorpost': []}}

		# 注意：这个解析器的逻辑与其他不同，先读取布尔值再检查
		has_root = reader.ReadBoolean()
		if not has_root:
			return result

		# 检查错误日志数组是否存在
		has_errorpost = reader.ReadBoolean()
		if not has_errorpost:
			return result

		# 读取错误日志数量
		count = reader.ReadSignedInt()

		# 读取每个错误日志项目
		for _ in range(count):
			# 按照C#代码中的字段顺序读取: event -> id -> tx -> txType
			item: ErrorpostItem = {
				'event': reader.ReadSignedInt(),
				'id': reader.ReadSignedInt(),
				'tx': reader.ReadUTFBytesWithLength(),
				'tx_type': reader.ReadSignedInt(),
			}
			result['root']['errorpost'].append(item)

		return result
