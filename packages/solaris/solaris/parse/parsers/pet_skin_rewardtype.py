"""pet_skin_rewardtype.bytes 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PetSkinRewardtypeInfo(TypedDict):
	id: int
	name: str
	sort: int
	subtype: int
	subtypename: str
	type: int


class _Data(TypedDict):
	data: list[PetSkinRewardtypeInfo]


class PetSkinRewardtypeParser(BaseParser[_Data]):
	@classmethod
	def source_config_filename(cls) -> str:
		return 'pet_skin_rewardtype.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'petSkinRewardtype.json'

	def parse(self, data: bytes) -> _Data:
		reader = BytesReader(data)
		result: _Data = {'data': []}

		if not reader.ReadBoolean():
			return result

		count = reader.ReadSignedInt()
		for _ in range(count):
			item: PetSkinRewardtypeInfo = {
				'id': reader.ReadSignedInt(),
				'name': reader.ReadUTFBytesWithLength(),
				'sort': reader.ReadSignedInt(),
				'subtype': reader.ReadSignedInt(),
				'subtypename': reader.ReadUTFBytesWithLength(),
				'type': reader.ReadSignedInt(),
			}
			result['data'].append(item)

		return result
