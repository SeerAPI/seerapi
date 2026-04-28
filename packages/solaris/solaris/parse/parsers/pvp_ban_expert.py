"""PVP 专家禁用配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PvpBanExpertInfo(TypedDict):
	"""PVP 专家禁用信息"""

	id: int
	name: str
	quantity: int
	reward: str
	seasonopen: int
	subkey_month: int
	subkey_total: int
	type: int


class PvpBanExpertConfig(TypedDict):
	"""PVP 专家禁用配置"""

	data: list[PvpBanExpertInfo]


class PvpBanExpertParser(BaseParser[PvpBanExpertConfig]):
	"""解析 pvp_ban_expert.bytes（PVP 专家禁用配置）"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'pvp_ban_expert.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'pvpBanExpert.json'

	def parse(self, data: bytes) -> PvpBanExpertConfig:
		reader = BytesReader(data)
		result = PvpBanExpertConfig(data=[])

		# 读取头部布尔值
		if not reader.read_bool():
			return result

		# 读取数据项数量
		count = reader.read_i32()

		for _ in range(count):
			info = PvpBanExpertInfo(
				id=reader.read_i32(),
				name=reader.ReadUTFBytesWithLength(),
				quantity=reader.read_i32(),
				reward=reader.ReadUTFBytesWithLength(),
				seasonopen=reader.read_i32(),
				subkey_month=reader.read_i32(),
				subkey_total=reader.read_i32(),
				type=reader.read_i32(),
			)
			result['data'].append(info)

		return result
