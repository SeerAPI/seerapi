from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class VipMonthMonsterItem(TypedDict):
	"""VIP月度精灵项"""

	bonus_ids: list[int]  # 对应 C# 的 BonusIds[]
	got_flag_info: list[int]  # 对应 C# 的 GotFlagInfo[]
	monsters_id: list[int]  # 对应 C# 的 MonstersID[]
	cur_month: int  # 对应 C# 的 CurMonth
	cur_year: int  # 对应 C# 的 CurYear
	id: int  # 对应 C# 的 ID
	monster_id: int  # 对应 C# 的 MonsterID


class _VipMonthMonsterRoot(TypedDict):
	"""VIP月度精灵根节点"""

	item: list[VipMonthMonsterItem]  # 对应 C# 的 Item 数组


class VipMonthMonsterConfig(TypedDict):
	"""VIP月度精灵顶层数据"""

	root: _VipMonthMonsterRoot


class VipMonthMonsterParser(BaseParser[VipMonthMonsterConfig]):
	"""VIP月度精灵配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'vip_month_monster.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'vipMonthMonster.json'

	def parse(self, data: bytes) -> VipMonthMonsterConfig:
		reader = BytesReader(data)
		result: VipMonthMonsterConfig = {'root': {'item': []}}

		# 检查header - 根据IRootInterface.Parse逻辑
		if not reader.ReadBoolean():
			return result

		# 检查是否有Item数据 - 根据IRoot.Parse逻辑
		if reader.ReadBoolean():
			item_count = reader.ReadSignedInt()

			for _ in range(item_count):
				# 按照IItemItem.Parse的顺序读取字段

				# 读取可选的BonusIds数组
				bonus_ids: list[int] = []
				if reader.ReadBoolean():
					bonus_count = reader.ReadSignedInt()
					bonus_ids = [reader.ReadSignedInt() for _ in range(bonus_count)]

				cur_month = reader.ReadSignedInt()
				cur_year = reader.ReadSignedInt()

				# 读取可选的GotFlagInfo数组
				got_flag_info: list[int] = []
				if reader.ReadBoolean():
					flag_count = reader.ReadSignedInt()
					got_flag_info = [reader.ReadSignedInt() for _ in range(flag_count)]

				id = reader.ReadSignedInt()
				monster_id = reader.ReadSignedInt()

				# 读取可选的MonstersID数组
				monsters_id: list[int] = []
				if reader.ReadBoolean():
					monsters_count = reader.ReadSignedInt()
					monsters_id = [
						reader.ReadSignedInt() for _ in range(monsters_count)
					]

				item = VipMonthMonsterItem(
					bonus_ids=bonus_ids,
					got_flag_info=got_flag_info,
					monsters_id=monsters_id,
					cur_month=cur_month,
					cur_year=cur_year,
					id=id,
					monster_id=monster_id,
				)
				result['root']['item'].append(item)

		return result
