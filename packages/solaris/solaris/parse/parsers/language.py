from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class LanguageInfo(TypedDict):
	content: str
	id: int
	key: str


class _Root(TypedDict):
	item: list[LanguageInfo]


class LanguageConfig(TypedDict):
	root: _Root


class LanguageParser(BaseParser[LanguageConfig]):
	@classmethod
	def source_config_filename(cls) -> str:
		return 'language.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'language.json'

	def parse(self, data: bytes) -> LanguageConfig:
		reader = BytesReader(data)
		result: LanguageConfig = {'root': {'item': []}}

		if not reader.ReadBoolean():
			return result

		num = reader.ReadSignedInt()
		for _ in range(num):
			item: LanguageInfo = {
				'content': reader.ReadUTFBytesWithLength(),
				'id': reader.ReadSignedInt(),
				'key': reader.ReadUTFBytesWithLength(),
			}
			result['root']['item'].append(item)

		return result
