"""特殊隐藏技能相关配置解析器

解析赛尔号客户端的特殊隐藏技能数据文件。
"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 特殊技能项数据结构
class SpMovesItem(TypedDict):
	"""特殊隐藏技能项"""

	itemname: str
	movesname: str
	id: int
	item: int
	itemnumber: int
	monster: int
	moves: int
	movetype: int


# 特殊隐藏技能配置结构
class _Config(TypedDict):
	"""特殊隐藏技能配置"""

	show_moves: list[SpMovesItem]
	sp_moves: list[SpMovesItem]


# 顶层数据结构
class SpHideMovesConfig(TypedDict):
	"""特殊隐藏技能配置数据"""

	config: _Config


class SpHideMovesParser(BaseParser[SpHideMovesConfig]):
	"""特殊隐藏技能配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'sp_hide_moves.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'spHideMoves.json'

	def parse(self, data: bytes) -> SpHideMovesConfig:
		reader = BytesReader(data)
		result: SpHideMovesConfig = {'config': {'show_moves': [], 'sp_moves': []}}

		# 检查是否有数据
		if not reader.ReadBoolean():
			return result

		# 解析 ShowMoves 数组
		if reader.ReadBoolean():
			show_moves_count = reader.ReadSignedInt()
			for _ in range(show_moves_count):
				# 按照 C# 代码顺序读取
				item_id = reader.ReadSignedInt()
				item = reader.ReadSignedInt()
				itemname = reader.ReadUTFBytesWithLength()
				itemnumber = reader.ReadSignedInt()
				monster = reader.ReadSignedInt()
				moves = reader.ReadSignedInt()
				movesname = reader.ReadUTFBytesWithLength()
				movetype = reader.ReadSignedInt()

				show_moves_item: SpMovesItem = {
					'itemname': itemname,
					'movesname': movesname,
					'id': item_id,
					'item': item,
					'itemnumber': itemnumber,
					'monster': monster,
					'moves': moves,
					'movetype': movetype,
				}
				result['config']['show_moves'].append(show_moves_item)

		# 解析 SpMoves 数组
		if reader.ReadBoolean():
			sp_moves_count = reader.ReadSignedInt()
			for _ in range(sp_moves_count):
				# 按照 C# 代码顺序读取
				item_id = reader.ReadSignedInt()
				item = reader.ReadSignedInt()
				itemname = reader.ReadUTFBytesWithLength()
				itemnumber = reader.ReadSignedInt()
				monster = reader.ReadSignedInt()
				moves = reader.ReadSignedInt()
				movesname = reader.ReadUTFBytesWithLength()
				movetype = reader.ReadSignedInt()

				sp_moves_item: SpMovesItem = {
					'itemname': itemname,
					'movesname': movesname,
					'id': item_id,
					'item': item,
					'itemnumber': itemnumber,
					'monster': monster,
					'moves': moves,
					'movetype': movetype,
				}
				result['config']['sp_moves'].append(sp_moves_item)

		return result
