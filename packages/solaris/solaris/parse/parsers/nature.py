"""
性格修正配置解析器
"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader

NatureItem = TypedDict(
	'NatureItem',
	{
		'id': int,
		'name': str,
		'des': str,
		'des2': str,
		'atk': float,
		'def': float,
		'sp_atk': float,
		'sp_def': float,
		'spd': float,
	},
)


class _Root(TypedDict):
	nature: list[NatureItem]


class NatureConfig(TypedDict):
	root: _Root


class NatureParser(BaseParser[NatureConfig]):
	@classmethod
	def source_config_filename(cls) -> str:
		return 'nature.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'nature.json'

	def parse(self, data: bytes) -> NatureConfig:
		reader = BytesReader(data)
		result: NatureConfig = {'root': {'nature': []}}

		# 检查根布尔标志
		if not reader.read_bool():
			return result

		# 检查nature数组存在标志
		if not reader.read_bool():
			return result

		# 读取nature数组数量
		count = reader.read_i32()

		# 循环读取nature项
		for _ in range(count):
			nature_item: NatureItem = {
				'des': reader.ReadUTFBytesWithLength(),
				'des2': reader.ReadUTFBytesWithLength(),
				'id': reader.read_i32(),
				'sp_atk': round(reader.read_f32(), 2),
				'sp_def': round(reader.read_f32(), 2),
				'atk': round(reader.read_f32(), 2),
				'def': round(reader.read_f32(), 2),
				'spd': round(reader.read_f32(), 2),
				'name': reader.ReadUTFBytesWithLength(),
			}
			result['root']['nature'].append(nature_item)

		return result
