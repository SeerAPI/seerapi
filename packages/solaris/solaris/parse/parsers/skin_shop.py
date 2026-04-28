from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class SkinShopItem(TypedDict):
	"""皮肤商店项"""

	name: str  # 对应 C# 的 Name
	show: list[int]  # 对应 C# 的 Show[]
	batch: int  # 对应 C# 的 Batch
	card_price: int  # 对应 C# 的 CardPrice
	diamond_price: int  # 对应 C# 的 DiamondPrice
	id: int  # 对应 C# 的 ID
	mon_id: int  # 对应 C# 的 MonID
	original_price: int  # 对应 C# 的 OriginalPrice
	product_id: int  # 对应 C# 的 ProductId
	rec: int  # 对应 C# 的 Rec
	skin_id: int  # 对应 C# 的 SkinID


class SkinShopSkins(TypedDict):
	"""皮肤商店皮肤集合"""

	skin: list[SkinShopItem]  # 对应 C# 的 Skin 数组


class SkinShopConfig(TypedDict):
	"""皮肤商店顶层数据"""

	skins: SkinShopSkins | None  # 对应 C# 的 Skins


class SkinShopParser(BaseParser[SkinShopConfig]):
	"""皮肤商店配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'skin_shop.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'skinShop.json'

	def parse(self, data: bytes) -> SkinShopConfig:
		reader = BytesReader(data)
		result: SkinShopConfig = {'skins': None}

		# 检查header - 根据IRootInterface.Parse逻辑
		if not reader.ReadBoolean():
			return result

		# 读取Skins数据
		skins: SkinShopSkins | None = None
		if reader.ReadBoolean():
			# 读取Skin数组 - 根据ISkins.Parse逻辑
			skin_items: list[SkinShopItem] = []
			if reader.ReadBoolean():
				skin_count = reader.ReadSignedInt()

				for _ in range(skin_count):
					# 按照ISkinItem.Parse的顺序读取字段
					batch = reader.ReadSignedInt()
					card_price = reader.ReadSignedInt()
					diamond_price = reader.ReadSignedInt()
					id = reader.ReadSignedInt()
					mon_id = reader.ReadSignedInt()
					name = reader.read_utf(reader.read_u16())
					original_price = reader.ReadSignedInt()
					product_id = reader.ReadSignedInt()
					rec = reader.ReadSignedInt()

					# 读取可选的Show数组
					show: list[int] = []
					if reader.ReadBoolean():
						show_count = reader.ReadSignedInt()
						show = [reader.ReadSignedInt() for _ in range(show_count)]

					skin_id = reader.ReadSignedInt()

					skin_item = SkinShopItem(
						name=name,
						show=show,
						batch=batch,
						card_price=card_price,
						diamond_price=diamond_price,
						id=id,
						mon_id=mon_id,
						original_price=original_price,
						product_id=product_id,
						rec=rec,
						skin_id=skin_id,
					)
					skin_items.append(skin_item)

			skins = SkinShopSkins(skin=skin_items)

		result['skins'] = skins

		return result
