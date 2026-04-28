from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PeakBattleWeeklyIDItem(TypedDict):
	"""巅峰战斗周ID项"""

	new_se_icon: str  # 对应 C# 的 NewSeIcon
	home_addition_mon: int  # 对应 C# 的 HomeAdditionMon


class PeakBattleGlobalRule(TypedDict):
	"""巅峰战斗全局规则"""

	weekly_id: list[PeakBattleWeeklyIDItem]  # 对应 C# 的 WeeklyID


class PeakBattleVirtualBattle(TypedDict):
	"""巅峰战斗虚拟战斗"""

	peak_bt_global_rule: PeakBattleGlobalRule | None  # 对应 C# 的 PeakBtGlobalRule


class PeakBattleMonsConfig(TypedDict):
	"""巅峰战斗精灵顶层数据"""

	virtual_battle: PeakBattleVirtualBattle  # 对应 C# 的 VirtualBattle


class PeakBattleMonsParser(BaseParser[PeakBattleMonsConfig]):
	"""巅峰战斗精灵配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'peak_battle_mons.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'peakBattleMons.json'

	def parse(self, data: bytes) -> PeakBattleMonsConfig:
		reader = BytesReader(data)
		result: PeakBattleMonsConfig = {'virtual_battle': {'peak_bt_global_rule': None}}

		# 检查header - 根据IRootInterface.Parse逻辑
		if not reader.ReadBoolean():
			return result

		# 读取VirtualBattle数据
		if reader.ReadBoolean():
			# 读取PeakBtGlobalRule数据
			peak_bt_global_rule: PeakBattleGlobalRule | None = None
			if reader.ReadBoolean():
				# 读取WeeklyID数组
				weekly_id_items: list[PeakBattleWeeklyIDItem] = []
				if reader.ReadBoolean():
					weekly_count = reader.ReadSignedInt()

					for _ in range(weekly_count):
						# 按照IWeeklyIDItem.Parse的顺序读取字段
						home_addition_mon = reader.ReadSignedInt()
						new_se_icon = reader.ReadUTFBytesWithLength()

						weekly_item = PeakBattleWeeklyIDItem(
							new_se_icon=new_se_icon, home_addition_mon=home_addition_mon
						)
						weekly_id_items.append(weekly_item)

				peak_bt_global_rule = PeakBattleGlobalRule(weekly_id=weekly_id_items)

			result['virtual_battle']['peak_bt_global_rule'] = peak_bt_global_rule

		return result
