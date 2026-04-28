"""VIP商店相关的解析器

包含 VIP道具商店和VIP宠物商店两个解析器。
"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader

# ============ VIP道具商店相关结构 ============


class VipItemShopItem(TypedDict):
	"""VIP道具商店项"""

	ex: int  # 对应 C# 的 ex
	id: int  # 对应 C# 的 Id
	limit_lv: int  # 对应 C# 的 LimitLv
	limit_num: int  # 对应 C# 的 LimitNum
	miditem_id: int  # 对应 C# 的 MiditemId
	month_key: int  # 对应 C# 的 MonthKey
	month_pos: int  # 对应 C# 的 MonthPos
	price: int  # 对应 C# 的 Price
	product_id: int  # 对应 C# 的 productID
	show_num: int  # 对应 C# 的 ShowNum
	show_reward: int  # 对应 C# 的 ShowReward
	type: int  # 对应 C# 的 Type


class _VipItemShopRoot(TypedDict):
	"""VIP道具商店根节点"""

	item: list[VipItemShopItem]  # 对应 C# 的 Item 数组


class VipItemShopConfig(TypedDict):
	"""VIP道具商店顶层数据"""

	root: _VipItemShopRoot


# ============ VIP宠物商店相关结构 ============


class VipPetShopItem(TypedDict):
	"""VIP宠物商店项"""

	forever_half_pos: int  # 对应 C# 的 ForeverHalfPos
	forever_key: int  # 对应 C# 的 ForeverKey
	is_extra: int  # 对应 C# 的 IsExtra
	judge_type: int  # 对应 C# 的 JudgeType
	limit_lv: int  # 对应 C# 的 LimitLv
	miditem_id: int  # 对应 C# 的 MiditemId
	mintmark_id: int  # 对应 C# 的 MintmarkId
	new_se: int  # 对应 C# 的 NewSe
	pet_id: int  # 对应 C# 的 PetId
	price: int  # 对应 C# 的 Price
	product_id: int  # 对应 C# 的 productID
	time_id: int  # 对应 C# 的 TimeId
	time_sub_id: int  # 对应 C# 的 TimeSubId
	turn: int  # 对应 C# 的 Turn


class _VipPetShopRoot(TypedDict):
	"""VIP宠物商店根节点"""

	pet: list[VipPetShopItem]  # 对应 C# 的 Pet 数组


class VipPetShopConfig(TypedDict):
	"""VIP宠物商店顶层数据"""

	root: _VipPetShopRoot


# ============ Parser 实现 ============


class VipItemShopParser(BaseParser[VipItemShopConfig]):
	"""VIP道具商店配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'vip_item_shop.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'vipItemShop.json'

	def parse(self, data: bytes) -> VipItemShopConfig:
		reader = BytesReader(data)
		result: VipItemShopConfig = {'root': {'item': []}}

		# 检查header - 根据IRootInterface.Parse逻辑
		if not reader.ReadBoolean():
			return result

		# 检查是否有Item数据 - 根据IRoot.Parse逻辑
		if reader.ReadBoolean():
			item_count = reader.ReadSignedInt()

			for _ in range(item_count):
				# 按照IItemItem.Parse的顺序读取字段
				id = reader.ReadSignedInt()
				limit_lv = reader.ReadSignedInt()
				limit_num = reader.ReadSignedInt()
				miditem_id = reader.ReadSignedInt()
				month_key = reader.ReadSignedInt()
				month_pos = reader.ReadSignedInt()
				price = reader.ReadSignedInt()
				show_num = reader.ReadSignedInt()
				show_reward = reader.ReadSignedInt()
				type = reader.ReadSignedInt()
				ex = reader.ReadSignedInt()
				product_id = reader.ReadSignedInt()

				item = VipItemShopItem(
					ex=ex,
					id=id,
					limit_lv=limit_lv,
					limit_num=limit_num,
					miditem_id=miditem_id,
					month_key=month_key,
					month_pos=month_pos,
					price=price,
					product_id=product_id,
					show_num=show_num,
					show_reward=show_reward,
					type=type,
				)
				result['root']['item'].append(item)

		return result


class VipPetShopParser(BaseParser[VipPetShopConfig]):
	"""VIP宠物商店配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'vip_pet_shop.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'vipPetShop.json'

	def parse(self, data: bytes) -> VipPetShopConfig:
		reader = BytesReader(data)
		result: VipPetShopConfig = {'root': {'pet': []}}

		# 检查header - 根据IRootInterface.Parse逻辑
		if not reader.ReadBoolean():
			return result

		# 检查是否有Pet数据 - 根据IRoot.Parse逻辑
		if reader.ReadBoolean():
			pet_count = reader.ReadSignedInt()

			for _ in range(pet_count):
				# 按照IPetItem.Parse的顺序读取字段
				forever_half_pos = reader.ReadSignedInt()
				forever_key = reader.ReadSignedInt()
				is_extra = reader.ReadSignedInt()
				judge_type = reader.ReadSignedInt()
				limit_lv = reader.ReadSignedInt()
				miditem_id = reader.ReadSignedInt()
				mintmark_id = reader.ReadSignedInt()
				new_se = reader.ReadSignedInt()
				pet_id = reader.ReadSignedInt()
				price = reader.ReadSignedInt()
				time_id = reader.ReadSignedInt()
				time_sub_id = reader.ReadSignedInt()
				turn = reader.ReadSignedInt()
				product_id = reader.ReadSignedInt()

				pet_item = VipPetShopItem(
					forever_half_pos=forever_half_pos,
					forever_key=forever_key,
					is_extra=is_extra,
					judge_type=judge_type,
					limit_lv=limit_lv,
					miditem_id=miditem_id,
					mintmark_id=mintmark_id,
					new_se=new_se,
					pet_id=pet_id,
					price=price,
					product_id=product_id,
					time_id=time_id,
					time_sub_id=time_sub_id,
					turn=turn,
				)
				result['root']['pet'].append(pet_item)

		return result
