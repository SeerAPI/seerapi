from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 好友情项结构定义
class _FriendshipItem(TypedDict):
	effect_args: list[int]
	effect_id: list[int]
	friend_id: int
	pet_id: int


class _PetFriends(TypedDict):
	friendship: list[_FriendshipItem]


class PetFriendsConfig(TypedDict):
	pet_friends: _PetFriends


class PetFriendsParser(BaseParser[PetFriendsConfig]):
	"""解析精灵好友情配置数据"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'pet_friends.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'petFriends.json'

	def parse(self, data: bytes) -> PetFriendsConfig:
		reader = BytesReader(data)
		result: PetFriendsConfig = {'pet_friends': {'friendship': []}}

		# 根标志
		if not reader.read_bool():
			return result

		# PetFriends 容器标志
		if not reader.read_bool():
			return result

		count = reader.read_i32()
		for _ in range(count):
			effect_args: list[int] = []
			effect_id: list[int] = []

			# 可选 EffectArgs
			if reader.read_bool():
				n = reader.read_i32()
				effect_args = [reader.read_i32() for _ in range(n)]

			# 可选 EffectID
			if reader.read_bool():
				n = reader.read_i32()
				effect_id = [reader.read_i32() for _ in range(n)]

			friend_id = reader.read_i32()
			pet_id = reader.read_i32()

			item: _FriendshipItem = {
				'effect_args': effect_args,
				'effect_id': effect_id,
				'friend_id': friend_id,
				'pet_id': pet_id,
			}
			result['pet_friends']['friendship'].append(item)

		return result
