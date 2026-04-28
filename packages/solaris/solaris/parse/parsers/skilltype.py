from typing import TypedDict

from solaris.parse.bytes_reader import BytesReader

from ..base import BaseParser


class SkillType(TypedDict):
	id: int
	is_dou: int
	cn: str
	en: list[str]
	att: str


class _Root(TypedDict):
	item: list[SkillType]


class SkillTypeConfig(TypedDict):
	root: _Root


class SkillTypeParser(BaseParser[SkillTypeConfig]):
	@classmethod
	def source_config_filename(cls) -> str:
		return 'skillTypes.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'skillType.json'

	def parse(self, data: bytes) -> SkillTypeConfig:
		reader = BytesReader(data)
		result: SkillTypeConfig = {'root': {'item': []}}
		if not (reader.ReadBoolean() and reader.ReadBoolean()):
			return result

		num = reader.ReadSignedInt()
		for _ in range(num):
			item: SkillType = {
				'att': reader.ReadUTFBytesWithLength(),
				'cn': reader.ReadUTFBytesWithLength(),
				'en': [
					reader.ReadUTFBytesWithLength()
					for _ in range(reader.ReadSignedInt())
				]
				if reader.ReadBoolean()
				else [],
				'id': reader.ReadSignedInt(),
				'is_dou': reader.ReadSignedInt(),
			}
			result['root']['item'].append(item)

		return result
