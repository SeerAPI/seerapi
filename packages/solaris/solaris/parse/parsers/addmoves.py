from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _MoveItem(TypedDict):
	id: int
	anm: list[str]
	reportname: list[str]
	reportskill: list[str]
	reporttxt: list[str]
	skin: list[int]
	cover: int
	damage: int
	monster: int


class _Moves(TypedDict):
	move: list[_MoveItem]


class AddMovesConfig(TypedDict):
	moves: _Moves


class AddMovesParser(BaseParser[AddMovesConfig]):
	@classmethod
	def source_config_filename(cls) -> str:
		return 'addmoves.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'addMoves.json'

	def parse(self, data: bytes) -> AddMovesConfig:
		reader = BytesReader(data)
		result: AddMovesConfig = {'moves': {'move': []}}

		# root presence
		if not reader.read_bool():
			return result

		# Moves presence
		if not reader.read_bool():
			return result

		count = reader.read_i32()
		for _ in range(count):
			# Defaults for optional arrays
			anm: list[str] = []
			reportname: list[str] = []
			reportskill: list[str] = []
			reporttxt: list[str] = []
			skin: list[int] = []

			item_id = reader.read_i32()

			if reader.read_bool():
				n = reader.read_i32()
				anm = [reader.read_utf(reader.read_u16()) for _ in range(n)]

			cover = reader.read_i32()
			damage = reader.read_i32()
			monster = reader.read_i32()

			if reader.read_bool():
				n = reader.read_i32()
				reportname = [reader.read_utf(reader.read_u16()) for _ in range(n)]

			if reader.read_bool():
				n = reader.read_i32()
				reportskill = [reader.read_utf(reader.read_u16()) for _ in range(n)]

			if reader.read_bool():
				n = reader.read_i32()
				reporttxt = [reader.read_utf(reader.read_u16()) for _ in range(n)]

			if reader.read_bool():
				n = reader.read_i32()
				skin = [reader.read_i32() for _ in range(n)]

			move_item: _MoveItem = {
				'id': item_id,
				'anm': anm,
				'reportname': reportname,
				'reportskill': reportskill,
				'reporttxt': reporttxt,
				'skin': skin,
				'cover': cover,
				'damage': damage,
				'monster': monster,
			}
			result['moves']['move'].append(move_item)

		return result
