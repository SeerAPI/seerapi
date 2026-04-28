from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class FreeTime(TypedDict):
	"""免费时间配置"""

	id: int


class MainPanel(TypedDict):
	"""主面板配置"""

	free_time: FreeTime | None
	pay_time: FreeTime | None


class Compone(TypedDict):
	"""组件配置"""

	name: list[str]


class TaskItem(TypedDict):
	"""任务项配置"""

	compone: Compone | None
	jump: str
	jump_h5: str
	main_panel: MainPanel | None
	id: int


class _Root(TypedDict):
	"""根数据结构"""

	task: list[TaskItem]


class AdvancedPetPanelConfig(TypedDict):
	"""顶层数据结构"""

	root: _Root


class AdvancedPetPanelConfigParser(BaseParser[AdvancedPetPanelConfig]):
	"""高级宠物面板配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'advancedPetPanelConfig.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'advancedPetPanelConfig.json'

	def parse(self, data: bytes) -> AdvancedPetPanelConfig:
		reader = BytesReader(data)
		result: AdvancedPetPanelConfig = {'root': {'task': []}}

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
			# 读取可选的Compone组件
			compone: Compone | None = None
			if reader.ReadBoolean():
				compone_names: list[str] = []
				if reader.ReadBoolean():
					name_count = reader.ReadSignedInt()
					for _ in range(name_count):
						name = reader.ReadUTFBytesWithLength()
						compone_names.append(name)
				compone = {'name': compone_names}

			# 读取ID
			task_id = reader.ReadSignedInt()

			# 读取Jump字符串
			jump = reader.ReadUTFBytesWithLength()

			# 读取JumpH5字符串
			jump_h5 = reader.ReadUTFBytesWithLength()

			# 读取可选的MainPanel
			main_panel: MainPanel | None = None
			if reader.ReadBoolean():
				free_time: FreeTime | None = None
				if reader.ReadBoolean():
					free_time = {'id': reader.ReadSignedInt()}

				pay_time: FreeTime | None = None
				if reader.ReadBoolean():
					pay_time = {'id': reader.ReadSignedInt()}

				main_panel = {'free_time': free_time, 'pay_time': pay_time}

			# 创建任务项
			task_item: TaskItem = {
				'compone': compone,
				'jump': jump,
				'jump_h5': jump_h5,
				'main_panel': main_panel,
				'id': task_id,
			}
			result['root']['task'].append(task_item)

		return result
