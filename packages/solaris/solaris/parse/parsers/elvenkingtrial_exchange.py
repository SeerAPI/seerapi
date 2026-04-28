from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class RewardItem(TypedDict):
	"""奖励项目"""

	id: int
	realcnt: int
	realid: int


class SwapItem(TypedDict):
	"""兑换项目"""

	id: int
	rewards: int


class ItemItem(TypedDict):
	"""物品项目"""

	new_stat_log: str
	bosslist: int
	bosstitle: str
	bsreward: int
	difficulty: int
	exreward: list[int]
	exrewardpro: str
	id: int
	mon: int
	sebossid: int
	unlimite: int


class _Items(TypedDict):
	"""物品集合"""

	item: list[ItemItem]


class _Rewards(TypedDict):
	"""奖励集合"""

	reward: list[RewardItem]


class _Swaps(TypedDict):
	"""兑换集合"""

	swap: list[SwapItem]


class _Root(TypedDict):
	"""根数据结构"""

	items: _Items | None
	rewards: _Rewards | None
	swaps: _Swaps | None


class ElvenKingTrialExchangeConfig(TypedDict):
	"""顶层数据结构"""

	root: _Root | None


class ElvenKingTrialExchangeParser(BaseParser[ElvenKingTrialExchangeConfig]):
	"""精灵王试炼兑换解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'elvenkingtrial_exchange.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'elvenKingTrialExchange.json'

	def parse(self, data: bytes) -> ElvenKingTrialExchangeConfig:
		reader = BytesReader(data)
		result: ElvenKingTrialExchangeConfig = {'root': None}

		# 检查根数据是否存在
		has_root = reader.ReadBoolean()
		if not has_root:
			return result

		# 解析Items
		items: _Items | None = None
		has_items = reader.ReadBoolean()
		if has_items:
			items_data: list[ItemItem] = []
			has_item_array = reader.ReadBoolean()
			if has_item_array:
				count = reader.ReadSignedInt()
				for _ in range(count):
					# 按照C#代码中的字段顺序读取
					new_stat_log = reader.ReadUTFBytesWithLength()
					bosslist = reader.ReadSignedInt()
					bosstitle = reader.ReadUTFBytesWithLength()
					bsreward = reader.ReadSignedInt()
					difficulty = reader.ReadSignedInt()

					# 处理可选的exreward数组
					exreward: list[int] = []
					has_exreward = reader.ReadBoolean()
					if has_exreward:
						exreward_count = reader.ReadSignedInt()
						exreward = [
							reader.ReadSignedInt() for _ in range(exreward_count)
						]

					exrewardpro = reader.ReadUTFBytesWithLength()
					item_id = reader.ReadSignedInt()
					mon = reader.ReadSignedInt()
					sebossid = reader.ReadSignedInt()
					unlimite = reader.ReadSignedInt()

					item: ItemItem = {
						'new_stat_log': new_stat_log,
						'bosslist': bosslist,
						'bosstitle': bosstitle,
						'bsreward': bsreward,
						'difficulty': difficulty,
						'exreward': exreward,
						'exrewardpro': exrewardpro,
						'id': item_id,
						'mon': mon,
						'sebossid': sebossid,
						'unlimite': unlimite,
					}
					items_data.append(item)
			items = {'item': items_data}

		# 解析Rewards
		rewards: _Rewards | None = None
		has_rewards = reader.ReadBoolean()
		if has_rewards:
			rewards_data: list[RewardItem] = []
			has_reward_array = reader.ReadBoolean()
			if has_reward_array:
				count = reader.ReadSignedInt()
				for _ in range(count):
					reward: RewardItem = {
						'id': reader.ReadSignedInt(),
						'realcnt': reader.ReadSignedInt(),
						'realid': reader.ReadSignedInt(),
					}
					rewards_data.append(reward)
			rewards = {'reward': rewards_data}

		# 解析Swaps
		swaps: _Swaps | None = None
		has_swaps = reader.ReadBoolean()
		if has_swaps:
			swaps_data: list[SwapItem] = []
			has_swap_array = reader.ReadBoolean()
			if has_swap_array:
				count = reader.ReadSignedInt()
				for _ in range(count):
					swap: SwapItem = {
						'id': reader.ReadSignedInt(),
						'rewards': reader.ReadSignedInt(),
					}
					swaps_data.append(swap)
			swaps = {'swap': swaps_data}

		result['root'] = {
			'items': items,
			'rewards': rewards,
			'swaps': swaps,
		}

		return result
