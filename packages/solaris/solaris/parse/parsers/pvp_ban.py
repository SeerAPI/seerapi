"""PVP 禁用配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PvpBanInfo(TypedDict):
	"""PVP 禁用信息"""

	id: int
	name: list[int]
	quantity: int
	subkey: int
	type: int


class PvpBanConfig(TypedDict):
	"""PVP 禁用配置"""

	data: list[PvpBanInfo]


class PvpBanParser(BaseParser[PvpBanConfig]):
	"""解析 pvp_ban.bytes（PVP 禁用配置）"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'pvp_ban.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'pvpBan.json'

	def parse(self, data: bytes) -> PvpBanConfig:
		reader = BytesReader(data)
		result = PvpBanConfig(data=[])

		# 读取头部布尔值
		if not reader.read_bool():
			return result

		# 读取数据项数量
		count = reader.read_i32()

		for _ in range(count):
			# 读取 id
			item_id = reader.read_i32()

			# 读取 name 数组（可选）
			name: list[int] = []
			if reader.read_bool():
				name_count = reader.read_i32()
				name = [reader.read_i32() for _ in range(name_count)]

			# 读取其他字段
			quantity = reader.read_i32()
			subkey = reader.read_i32()
			item_type = reader.read_i32()

			result['data'].append(
				PvpBanInfo(
					id=item_id,
					name=name,
					quantity=quantity,
					subkey=subkey,
					type=item_type,
				)
			)

		return result
