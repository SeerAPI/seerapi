"""petEffectIcon.bytes 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PetEffectIconInfo(TypedDict):
	"""精灵效果图标信息条目"""

	Desc: str
	affectedBoss: int
	effecticonid: int
	id: int
	isAdv: int
	petid: int


class PetEffectIconConfig(TypedDict):
	"""精灵效果图标配置数据"""

	data: list[PetEffectIconInfo]


class PetEffectIconParser(BaseParser[PetEffectIconConfig]):
	"""解析 petEffectIcon.bytes 配置文件"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'petEffectIcon.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'petEffectIcon.json'

	def parse(self, data: bytes) -> PetEffectIconConfig:
		reader = BytesReader(data)
		result = PetEffectIconConfig(data=[])

		# 检查是否有数据
		if not reader.ReadBoolean():
			return result

		# 读取数组长度
		count = reader.ReadSignedInt()

		# 循环读取每个 PetEffectIconInfo
		for _ in range(count):
			# 按照 IPetEffectIconInfo.Parse 方法的读取顺序
			desc = reader.ReadUTFBytesWithLength()
			affected_boss = reader.ReadSignedInt()
			effecticonid = reader.ReadSignedInt()
			id_val = reader.ReadSignedInt()
			is_adv = reader.ReadSignedInt()
			petid = reader.ReadSignedInt()

			result['data'].append(
				PetEffectIconInfo(
					Desc=desc,
					affectedBoss=affected_boss,
					effecticonid=effecticonid,
					id=id_val,
					isAdv=is_adv,
					petid=petid,
				)
			)

		return result
