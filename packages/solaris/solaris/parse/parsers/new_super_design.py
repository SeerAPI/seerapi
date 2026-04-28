"""解析赛尔号客户端的因子关卡数据文件。"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 成就数据结构
class Achievement(TypedDict):
	"""成就"""

	branch_id: int
	rule_id: int


# 配置数据结构
class Configure(TypedDict):
	"""配置"""

	exchange_id: list[int]
	exchange_product_id: list[int]
	exchange_mintmark: int
	fail_times: int
	needmon: int
	progress_value: int
	times: int
	time_value: int


# 任务项数据结构
class TaskItem(TypedDict):
	"""任务项"""

	desc: str
	battle_boss: int
	battlelevel: int
	battle_type: int
	id: int


# 简单战斗数据结构
class EasyBattle(TypedDict):
	"""简单战斗"""

	desc: str
	task: list[TaskItem]
	battle_cnt: int
	out: int
	task_style: int


# 普通战斗数据结构
class NormalBattle(TypedDict):
	"""普通战斗"""

	desc: str
	rule_id: str
	task: list[TaskItem]
	battle_cnt: int
	out: int
	task_style: int


# 奖励数据结构
class Reward(TypedDict):
	"""奖励"""

	gain_value: int
	item_id: int
	mint_mark_id: int
	monster_id: int


# 规则项数据结构
class RuleItem(TypedDict):
	"""规则项"""

	args: str
	check_tips: str
	fail_tips: str
	repeat_tips: str
	user_info: str
	id: int
	mould_id: int


# 规则容器数据结构
class Rules(TypedDict):
	"""规则容器"""

	rule: list[RuleItem]


# 扫荡数据结构
class Sweep(TypedDict):
	"""扫荡"""

	product_id: list[int]


# 设计项数据结构
class DesignItem(TypedDict):
	"""设计项"""

	achievement: Achievement | None
	configure: Configure | None
	easy_battle: EasyBattle | None
	hard_battle: NormalBattle | None  # 使用 INormalBattle 类型
	normal_battle: NormalBattle | None
	reward: Reward | None
	rules: Rules | None
	sweep: Sweep | None
	id: int


# 根容器结构
class _Root(TypedDict):
	"""根容器"""

	design: list[DesignItem]


# 顶层数据结构
class NewSuperDesignConfig(TypedDict):
	"""因子关卡配置数据"""

	root: _Root


class NewSuperDesignParser(BaseParser[NewSuperDesignConfig]):
	"""因子关卡配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'new_super_design.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'newSuperDesign.json'

	def _parse_achievement(self, reader: BytesReader) -> Achievement:
		"""解析成就"""
		return {'branch_id': reader.ReadSignedInt(), 'rule_id': reader.ReadSignedInt()}

	def _parse_configure(self, reader: BytesReader) -> Configure:
		"""解析配置"""
		# 解析 ExchangeID 数组
		exchange_id: list[int] = []
		if reader.ReadBoolean():
			count = reader.ReadSignedInt()
			exchange_id = [reader.ReadSignedInt() for _ in range(count)]

		# 解析 ExchangeProductID 数组
		exchange_product_id: list[int] = []
		if reader.ReadBoolean():
			count = reader.ReadSignedInt()
			exchange_product_id = [reader.ReadSignedInt() for _ in range(count)]

		return {
			'exchange_id': exchange_id,
			'exchange_product_id': exchange_product_id,
			'exchange_mintmark': reader.ReadSignedInt(),
			'fail_times': reader.ReadSignedInt(),
			'progress_value': reader.ReadSignedInt(),
			'time_value': reader.ReadSignedInt(),
			'times': reader.ReadSignedInt(),
			'needmon': reader.ReadSignedInt(),
		}

	def _parse_task_items(self, reader: BytesReader) -> list[TaskItem]:
		"""解析任务项列表"""
		tasks: list[TaskItem] = []
		if reader.ReadBoolean():
			count = reader.ReadSignedInt()
			for _ in range(count):
				task: TaskItem = {
					'battle_boss': reader.ReadSignedInt(),
					'battle_type': reader.ReadSignedInt(),
					'battlelevel': reader.ReadSignedInt(),
					'desc': reader.ReadUTFBytesWithLength(),
					'id': reader.ReadSignedInt(),
				}
				tasks.append(task)
		return tasks

	def _parse_easy_battle(self, reader: BytesReader) -> EasyBattle:
		"""解析简单战斗"""
		battle_cnt = reader.ReadSignedInt()
		desc = reader.ReadUTFBytesWithLength()
		out = reader.ReadSignedInt()
		task = self._parse_task_items(reader)
		task_style = reader.ReadSignedInt()

		return {
			'desc': desc,
			'task': task,
			'battle_cnt': battle_cnt,
			'out': out,
			'task_style': task_style,
		}

	def _parse_normal_battle(self, reader: BytesReader) -> NormalBattle:
		"""解析普通战斗"""
		battle_cnt = reader.ReadSignedInt()
		desc = reader.ReadUTFBytesWithLength()
		out = reader.ReadSignedInt()
		rule_id = reader.ReadUTFBytesWithLength()
		task = self._parse_task_items(reader)
		task_style = reader.ReadSignedInt()

		return {
			'desc': desc,
			'rule_id': rule_id,
			'task': task,
			'battle_cnt': battle_cnt,
			'out': out,
			'task_style': task_style,
		}

	def _parse_reward(self, reader: BytesReader) -> Reward:
		"""解析奖励"""
		return {
			'gain_value': reader.ReadSignedInt(),
			'item_id': reader.ReadSignedInt(),
			'mint_mark_id': reader.ReadSignedInt(),
			'monster_id': reader.ReadSignedInt(),
		}

	def _parse_rules(self, reader: BytesReader) -> Rules:
		"""解析规则容器"""
		rule_list: list[RuleItem] = []
		if reader.ReadBoolean():
			count = reader.ReadSignedInt()
			for _ in range(count):
				rule_item: RuleItem = {
					'args': reader.ReadUTFBytesWithLength(),
					'check_tips': reader.ReadUTFBytesWithLength(),
					'fail_tips': reader.ReadUTFBytesWithLength(),
					'id': reader.ReadSignedInt(),
					'mould_id': reader.ReadSignedInt(),
					'repeat_tips': reader.ReadUTFBytesWithLength(),
					'user_info': reader.ReadUTFBytesWithLength(),
				}
				rule_list.append(rule_item)

		return {'rule': rule_list}

	def _parse_sweep(self, reader: BytesReader) -> Sweep:
		"""解析扫荡"""
		product_id: list[int] = []
		if reader.ReadBoolean():
			count = reader.ReadSignedInt()
			product_id = [reader.ReadSignedInt() for _ in range(count)]

		return {'product_id': product_id}

	def parse(self, data: bytes) -> NewSuperDesignConfig:
		reader = BytesReader(data)
		result: NewSuperDesignConfig = {'root': {'design': []}}

		# 检查是否有数据
		if not reader.ReadBoolean():
			return result

		# 解析根容器
		if reader.ReadBoolean():
			design_count = reader.ReadSignedInt()
			for _ in range(design_count):
				# 解析设计项 - 严格按照 C# 代码顺序读取

				# 可选的 Achievement
				achievement = None
				if reader.ReadBoolean():
					achievement = self._parse_achievement(reader)

				# 可选的 Configure
				configure = None
				if reader.ReadBoolean():
					configure = self._parse_configure(reader)

				# 可选的 EasyBattle
				easy_battle = None
				if reader.ReadBoolean():
					easy_battle = self._parse_easy_battle(reader)

				# 可选的 HardBattle (使用 INormalBattle)
				hard_battle = None
				if reader.ReadBoolean():
					hard_battle = self._parse_normal_battle(reader)

				# ID 字段
				design_id = reader.ReadSignedInt()

				# 可选的 NormalBattle
				normal_battle = None
				if reader.ReadBoolean():
					normal_battle = self._parse_normal_battle(reader)

				# 可选的 Reward
				reward = None
				if reader.ReadBoolean():
					reward = self._parse_reward(reader)

				# 可选的 Rules
				rules = None
				if reader.ReadBoolean():
					rules = self._parse_rules(reader)

				# 可选的 Sweep
				sweep = None
				if reader.ReadBoolean():
					sweep = self._parse_sweep(reader)

				design_item: DesignItem = {
					'achievement': achievement,
					'configure': configure,
					'easy_battle': easy_battle,
					'hard_battle': hard_battle,
					'normal_battle': normal_battle,
					'reward': reward,
					'rules': rules,
					'sweep': sweep,
					'id': design_id,
				}
				result['root']['design'].append(design_item)

		return result
