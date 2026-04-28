from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ProfilephotoInfo(TypedDict):
	checkown: int
	desc: str
	finishTime: int
	goto: str
	hide: int
	icon: int
	id: int
	name: str
	rarity: int
	spine: str
	tab: int
	text: str
	type: int
	unavailable: int
	unlocktype: int


class _Root(TypedDict):
	item: list[ProfilephotoInfo]


class ProfilephotoConfig(TypedDict):
	root: _Root


class ProfilephotoParser(BaseParser[ProfilephotoConfig]):
	@classmethod
	def source_config_filename(cls) -> str:
		return 'profilephoto.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'profilephoto.json'

	def parse(self, data: bytes) -> ProfilephotoConfig:
		reader = BytesReader(data)
		result: ProfilephotoConfig = {'root': {'item': []}}

		if not reader.ReadBoolean():
			return result

		num = reader.ReadSignedInt()
		for _ in range(num):
			item: ProfilephotoInfo = {
				'checkown': reader.ReadSignedInt(),
				'desc': reader.ReadUTFBytesWithLength(),
				'finishTime': reader.ReadSignedInt(),
				'goto': reader.ReadUTFBytesWithLength(),
				'hide': reader.ReadSignedInt(),
				'icon': reader.ReadSignedInt(),
				'id': reader.ReadSignedInt(),
				'name': reader.ReadUTFBytesWithLength(),
				'rarity': reader.ReadSignedInt(),
				'spine': reader.ReadUTFBytesWithLength(),
				'tab': reader.ReadSignedInt(),
				'text': reader.ReadUTFBytesWithLength(),
				'type': reader.ReadSignedInt(),
				'unavailable': reader.ReadSignedInt(),
				'unlocktype': reader.ReadSignedInt(),
			}
			result['root']['item'].append(item)

		return result
