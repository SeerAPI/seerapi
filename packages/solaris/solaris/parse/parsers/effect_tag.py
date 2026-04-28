from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class EffectTagItem(TypedDict):
	id: int
	tag: str


class EffectTagConfig(TypedDict):
	data: list[EffectTagItem]


class EffectTagParser(BaseParser[EffectTagConfig]):
	@classmethod
	def source_config_filename(cls) -> str:
		return 'effectag.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'effectag.json'

	def parse(self, data: bytes) -> EffectTagConfig:
		result = EffectTagConfig(data=[])
		reader = BytesReader(data)
		if not reader.read_bool():
			return result
		for _ in range(reader.read_i32()):
			item = EffectTagItem(
				id=reader.read_i32(),
				tag=reader.ReadUTFBytesWithLength(),
			)
			result['data'].append(item)

		return result
