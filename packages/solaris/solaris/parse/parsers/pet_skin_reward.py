"""pet_skin_reward.bytes 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PetSkinRewardInfo(TypedDict):
	"""精灵皮肤奖励信息条目"""

	id: int
	changereward: str
	param: int
	redbadge: int
	reward: str
	skintype: int
	stainfo: int
	subtype: int
	userbit: int
	userinfo: int
	userinfo1: int


class PetSkinRewardConfig(TypedDict):
	"""精灵皮肤奖励配置数据"""

	data: list[PetSkinRewardInfo]


class PetSkinRewardParser(BaseParser[PetSkinRewardConfig]):
	"""解析 pet_skin_reward.bytes 配置文件"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'pet_skin_reward.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'petSkinReward.json'

	def parse(self, data: bytes) -> PetSkinRewardConfig:
		reader = BytesReader(data)
		result = PetSkinRewardConfig(data=[])

		# 检查是否有数据
		if not reader.ReadBoolean():
			return result

		# 读取数组长度
		count = reader.ReadSignedInt()

		# 循环读取每个 PetSkinRewardInfo
		for _ in range(count):
			# 按照 IPetSkinRewardInfo.Parse 方法的读取顺序
			changereward = reader.ReadUTFBytesWithLength()
			id_val = reader.ReadSignedInt()
			param = reader.ReadSignedInt()
			redbadge = reader.ReadSignedInt()
			reward = reader.ReadUTFBytesWithLength()
			skintype = reader.ReadSignedInt()
			stainfo = reader.ReadSignedInt()
			subtype = reader.ReadSignedInt()
			userbit = reader.ReadSignedInt()
			userinfo = reader.ReadSignedInt()
			userinfo1 = reader.ReadSignedInt()
			result['data'].append(
				PetSkinRewardInfo(
					id=id_val,
					changereward=changereward,
					param=param,
					redbadge=redbadge,
					reward=reward,
					skintype=skintype,
					stainfo=stainfo,
					subtype=subtype,
					userbit=userbit,
					userinfo=userinfo,
					userinfo1=userinfo1,
				)
			)

		return result
