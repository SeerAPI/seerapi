from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class NewSeItem(TypedDict):
	AdditionNum: int
	AdditionType: int
	Args: str
	Des: str
	Desc: str
	Eid: int
	Idx: int
	Intro: str
	ItemId: int
	StarLevel: int
	Stat: int


class _NewSe(TypedDict):
	NewSeIdx: list[NewSeItem]


class NewSeConfig(TypedDict):
	NewSe: _NewSe


class NewSeParser(BaseParser[NewSeConfig]):
	@classmethod
	def source_config_filename(cls) -> str:
		return 'new_se.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'new_se.json'

	def parse(self, data: bytes) -> NewSeConfig:
		result: NewSeConfig = {'NewSe': {'NewSeIdx': []}}
		reader = BytesReader(data)
		if not (reader.ReadBoolean() and reader.ReadBoolean()):
			return result

		num = reader.ReadSignedInt()
		for _ in range(num):
			item: NewSeItem = {
				'AdditionNum': reader.ReadSignedInt(),
				'AdditionType': reader.ReadSignedInt(),
				'Args': reader.ReadUTFBytesWithLength(),
				'Des': reader.ReadUTFBytesWithLength(),
				'Desc': reader.ReadUTFBytesWithLength(),
				'Eid': reader.ReadSignedInt(),
				'Idx': reader.ReadSignedInt(),
				'Intro': reader.ReadUTFBytesWithLength(),
				'ItemId': reader.ReadSignedInt(),
				'StarLevel': reader.ReadSignedInt(),
				'Stat': reader.ReadSignedInt(),
			}
			result['NewSe']['NewSeIdx'].append(item)

		return result
