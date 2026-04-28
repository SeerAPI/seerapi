from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 技能石效果项结构
class MoveEffectItem(TypedDict):
	id: int
	side_effect: list[int] | None  # 可选数组字段
	side_effect_arg: list[int] | None  # 可选数组字段


# 技能石项结构
class MoveStoneItem(TypedDict):
	accuracy: int
	id: int
	max_pp: int
	move_effect: list[MoveEffectItem]  # 可选数组字段
	name: str
	power: int
	type: int


# 技能石集合内部结构
class _MoveStones(TypedDict):
	move_stone: list[MoveStoneItem]


# 技能石数据根结构
class MoveStonesConfig(TypedDict):
	root: _MoveStones | None


class MoveStonesParser(BaseParser[MoveStonesConfig]):
	"""技能石解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'move_stones.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'moveStones.json'

	def parse(self, data: bytes) -> MoveStonesConfig:
		reader = BytesReader(data)
		result: MoveStonesConfig = {'root': None}

		# 检查是否有MoveStones数据
		if reader.ReadBoolean():
			move_stones: _MoveStones = {'move_stone': []}

			# 检查是否有MoveStone数组数据
			if reader.ReadBoolean():
				stone_count = reader.ReadSignedInt()

				# 循环读取每个MoveStoneItem
				for _ in range(stone_count):
					stone_item: MoveStoneItem = {
						'accuracy': reader.ReadSignedInt(),
						'id': reader.ReadSignedInt(),
						'max_pp': reader.ReadSignedInt(),
						'move_effect': [],
						'name': '',
						'power': 0,
						'type': 0,
					}

					# 读取可选的MoveEffect数组
					if reader.ReadBoolean():
						effect_count = reader.ReadSignedInt()
						stone_item['move_effect'] = []

						for _ in range(effect_count):
							effect_item: MoveEffectItem = {
								'id': reader.ReadSignedInt(),
								'side_effect': None,
								'side_effect_arg': None,
							}

							# 读取可选的SideEffect数组
							if reader.ReadBoolean():
								se_count = reader.ReadSignedInt()
								effect_item['side_effect'] = [
									reader.ReadSignedInt() for _ in range(se_count)
								]

							# 读取可选的SideEffectArg数组
							if reader.ReadBoolean():
								se_arg_count = reader.ReadSignedInt()
								effect_item['side_effect_arg'] = [
									reader.ReadSignedInt() for _ in range(se_arg_count)
								]

							stone_item['move_effect'].append(effect_item)

					# 继续读取基础字段
					stone_item['name'] = reader.ReadUTFBytesWithLength()
					stone_item['power'] = reader.ReadSignedInt()
					stone_item['type'] = reader.ReadSignedInt()

					move_stones['move_stone'].append(stone_item)

			result['root'] = move_stones

		return result
