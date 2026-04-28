from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AdvEffect(TypedDict):
	"""觉醒效果"""

	des: str
	id: int


class ExMove(TypedDict):
	"""额外招式"""

	extra_moves: int


class Race(TypedDict):
	"""种族信息"""

	new_race: list[int]
	old_race: list[int]


class SpMove(TypedDict):
	"""特殊招式"""

	sp_moves: list[int]


class Advances(TypedDict):
	"""觉醒详情"""

	adv_effect: AdvEffect | None
	ex_move: ExMove | None
	race: Race | None
	sp_move: SpMove | None
	adv_type: int
	monster_id: int


class TaskItem(TypedDict):
	"""任务项目"""

	advances: Advances | None
	id: int
	new_eff_id: int
	old_eff_id: int


class _Root(TypedDict):
	"""根数据结构"""

	task: list[TaskItem]


class AwakenDetailConfig(TypedDict):
	"""顶层数据结构"""

	root: _Root


class AwakenDetailParser(BaseParser[AwakenDetailConfig]):
	"""觉醒详情解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'awakendetail.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'awakenDetail.json'

	def parse(self, data: bytes) -> AwakenDetailConfig:
		reader = BytesReader(data)
		result: AwakenDetailConfig = {'root': {'task': []}}

		# 检查根数据是否存在
		if not reader.ReadBoolean():
			return result

		# 检查任务数组是否存在
		if not reader.ReadBoolean():
			return result

		# 读取任务数量
		count = reader.ReadSignedInt()

		# 读取每个任务项
		for _ in range(count):
			# 解析可选的Advances
			advances: Advances | None = None
			if reader.ReadBoolean():
				# 解析AdvEffect
				adv_effect: AdvEffect | None = None
				if reader.ReadBoolean():
					adv_effect = {
						'des': reader.ReadUTFBytesWithLength(),
						'id': reader.ReadSignedInt(),
					}

				# 读取AdvType和MonsterId
				adv_type = reader.ReadSignedInt()
				monster_id = reader.ReadSignedInt()

				# 解析可选的Race
				race: Race | None = None
				if reader.ReadBoolean():
					new_race: list[int] = []
					if reader.ReadBoolean():
						new_race_count = reader.ReadSignedInt()
						new_race = [
							reader.ReadSignedInt() for _ in range(new_race_count)
						]

					old_race: list[int] = []
					if reader.ReadBoolean():
						old_race_count = reader.ReadSignedInt()
						old_race = [
							reader.ReadSignedInt() for _ in range(old_race_count)
						]

					race = {'new_race': new_race, 'old_race': old_race}

				# 解析可选的ExMove
				ex_move: ExMove | None = None
				if reader.ReadBoolean():
					ex_move = {'extra_moves': reader.ReadSignedInt()}

				# 解析可选的SpMove
				sp_move: SpMove | None = None
				if reader.ReadBoolean():
					sp_moves: list[int] = []
					if reader.ReadBoolean():
						sp_moves_count = reader.ReadSignedInt()
						sp_moves = [
							reader.ReadSignedInt() for _ in range(sp_moves_count)
						]
					sp_move = {'sp_moves': sp_moves}

				advances = {
					'adv_effect': adv_effect,
					'ex_move': ex_move,
					'race': race,
					'sp_move': sp_move,
					'adv_type': adv_type,
					'monster_id': monster_id,
				}

			# 读取任务项的其他字段
			task_id = reader.ReadSignedInt()
			new_eff_id = reader.ReadSignedInt()
			old_eff_id = reader.ReadSignedInt()

			task_item: TaskItem = {
				'advances': advances,
				'id': task_id,
				'new_eff_id': new_eff_id,
				'old_eff_id': old_eff_id,
			}
			result['root']['task'].append(task_item)

		return result
