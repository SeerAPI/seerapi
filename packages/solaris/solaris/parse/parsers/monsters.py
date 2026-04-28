"""精灵相关配置解析器

解析赛尔号客户端的精灵数据文件，包含精灵属性、技能等信息。
"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 技能项数据结构
class MoveItem(TypedDict):
	"""技能项"""

	id: int
	learning_lv: int
	rec: int
	tag: int


# 特殊技能项数据结构
class SpMoveItem(TypedDict):
	"""特殊技能项"""

	id: int
	rec: int
	tag: int
	tag2: int  # C# 中有两个 Tag 字段，一个大写一个小写


# 可学技能数据结构
class LearnableMoves(TypedDict):
	"""可学技能"""

	adv_move: list[SpMoveItem]
	move: list[MoveItem]
	sp_move: list[SpMoveItem]


MonsterItem = TypedDict(
	'MonsterItem',
	{
		'def_name': str,
		'extra_moves': LearnableMoves | None,
		'learnable_moves': LearnableMoves | None,
		'move': MoveItem | None,
		'show_extra_moves': LearnableMoves | None,
		'sp_extra_moves': LearnableMoves | None,
		'atk': int,
		'character_attr_param': int,
		'combo': int,
		'def': int,
		'evolv_flag': int,
		'evolves_to': int,
		'evolving_lv': int,
		'free_forbidden': int,
		'gender': int,
		'hp': int,
		'id': int,
		'is_fly_pet': int,
		'is_ride_pet': int,
		'pet_class': int,
		'real_id': int,
		'sp_atk': int,
		'sp_def': int,
		'spd': int,
		'support': int,
		'transform': int,
		'type': int,
		'vip': int,
	},
)


# 精灵容器结构
class _Monsters(TypedDict):
	"""精灵容器"""

	monster: list[MonsterItem]


# 顶层数据结构
class MonstersConfig(TypedDict):
	"""精灵配置数据"""

	monsters: _Monsters


class MonstersParser(BaseParser[MonstersConfig]):
	"""精灵配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'monsters.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'monsters.json'

	def _parse_learnable_moves(self, reader: BytesReader) -> LearnableMoves:
		"""解析可学技能结构"""
		adv_move: list[SpMoveItem] = []
		move: list[MoveItem] = []
		sp_move: list[SpMoveItem] = []

		# 解析 AdvMove 数组
		if reader.ReadBoolean():
			adv_count = reader.ReadSignedInt()
			for _ in range(adv_count):
				adv_item: SpMoveItem = {
					'id': reader.ReadSignedInt(),
					'rec': reader.ReadSignedInt(),
					'tag': reader.ReadSignedInt(),
					'tag2': reader.ReadSignedInt(),
				}
				adv_move.append(adv_item)

		# 解析 Move 数组
		if reader.ReadBoolean():
			move_count = reader.ReadSignedInt()
			for _ in range(move_count):
				move_item: MoveItem = {
					'id': reader.ReadSignedInt(),
					'learning_lv': reader.ReadSignedInt(),
					'rec': reader.ReadSignedInt(),
					'tag': reader.ReadSignedInt(),
				}
				move.append(move_item)

		# 解析 SpMove 数组
		if reader.ReadBoolean():
			sp_count = reader.ReadSignedInt()
			for _ in range(sp_count):
				sp_item: SpMoveItem = {
					'id': reader.ReadSignedInt(),
					'rec': reader.ReadSignedInt(),
					'tag': reader.ReadSignedInt(),
					'tag2': reader.ReadSignedInt(),
				}
				sp_move.append(sp_item)

		return {'adv_move': adv_move, 'move': move, 'sp_move': sp_move}

	def _parse_move_item(self, reader: BytesReader) -> MoveItem:
		"""解析技能项"""
		return {
			'id': reader.ReadSignedInt(),
			'learning_lv': reader.ReadSignedInt(),
			'rec': reader.ReadSignedInt(),
			'tag': reader.ReadSignedInt(),
		}

	def parse(self, data: bytes) -> MonstersConfig:
		reader = BytesReader(data)
		result: MonstersConfig = {'monsters': {'monster': []}}

		# 检查是否有精灵数据
		if not reader.ReadBoolean():
			return result

		# 解析精灵容器
		if reader.ReadBoolean():
			monster_count = reader.ReadSignedInt()
			for _ in range(monster_count):
				# 解析精灵项 - 严格按照 C# 代码顺序读取
				atk = reader.ReadSignedInt()
				character_attr_param = reader.ReadSignedInt()
				combo = reader.ReadSignedInt()
				def_ = reader.ReadSignedInt()
				def_name = reader.ReadUTFBytesWithLength()
				evolv_flag = reader.ReadSignedInt()
				evolves_to = reader.ReadSignedInt()
				evolving_lv = reader.ReadSignedInt()

				# 可选的 ExtraMoves
				extra_moves = None
				if reader.ReadBoolean():
					extra_moves = self._parse_learnable_moves(reader)

				free_forbidden = reader.ReadSignedInt()
				gender = reader.ReadSignedInt()
				hp = reader.ReadSignedInt()
				monster_id = reader.ReadSignedInt()

				# 可选的 LearnableMoves
				learnable_moves = None
				if reader.ReadBoolean():
					learnable_moves = self._parse_learnable_moves(reader)

				# 可选的 Move
				move = None
				if reader.ReadBoolean():
					move = self._parse_move_item(reader)

				pet_class = reader.ReadSignedInt()
				real_id = reader.ReadSignedInt()

				# 可选的 ShowExtraMoves
				show_extra_moves = None
				if reader.ReadBoolean():
					show_extra_moves = self._parse_learnable_moves(reader)

				sp_atk = reader.ReadSignedInt()
				sp_def = reader.ReadSignedInt()

				# 可选的 SpExtraMoves
				sp_extra_moves = None
				if reader.ReadBoolean():
					sp_extra_moves = self._parse_learnable_moves(reader)

				spd = reader.ReadSignedInt()
				support = reader.ReadSignedInt()
				transform = reader.ReadSignedInt()
				type_value = reader.ReadSignedInt()
				vip = reader.ReadSignedInt()
				is_fly_pet = reader.ReadSignedInt()
				is_ride_pet = reader.ReadSignedInt()

				monster_item: MonsterItem = {
					'def_name': def_name,
					'extra_moves': extra_moves,
					'learnable_moves': learnable_moves,
					'move': move,
					'show_extra_moves': show_extra_moves,
					'sp_extra_moves': sp_extra_moves,
					'atk': atk,
					'character_attr_param': character_attr_param,
					'combo': combo,
					'def': def_,
					'evolv_flag': evolv_flag,
					'evolves_to': evolves_to,
					'evolving_lv': evolving_lv,
					'free_forbidden': free_forbidden,
					'gender': gender,
					'hp': hp,
					'id': monster_id,
					'is_fly_pet': is_fly_pet,
					'is_ride_pet': is_ride_pet,
					'pet_class': pet_class,
					'real_id': real_id,
					'sp_atk': sp_atk,
					'sp_def': sp_def,
					'spd': spd,
					'support': support,
					'transform': transform,
					'type': type_value,
					'vip': vip,
				}
				result['monsters']['monster'].append(monster_item)

		return result
