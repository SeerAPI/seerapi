from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ProductDiamondItem(TypedDict):
	"""钻石产品项"""

	icon: str
	name: str
	item_id: list[int]  # 对应 C# 的 itemID[]
	price: int
	product_id: int  # 对应 C# 的 productID
	vip: float


class _ProductDiamondRoot(TypedDict):
	"""钻石产品根节点"""

	item: list[ProductDiamondItem]


class ProductDiamondConfig(TypedDict):
	"""钻石产品顶层数据"""

	root: _ProductDiamondRoot


class ProductDiamondParser(BaseParser[ProductDiamondConfig]):
	"""钻石产品配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'product_diamond.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'productDiamond.json'

	def parse(self, data: bytes) -> ProductDiamondConfig:
		reader = BytesReader(data)
		result: ProductDiamondConfig = {'root': {'item': []}}

		# 检查header - 根据IRootInterface.Parse逻辑
		if not reader.ReadBoolean():
			return result

		# 检查是否有item数据 - 根据IRoot.Parse逻辑
		if reader.ReadBoolean():
			count = reader.ReadSignedInt()

			for _ in range(count):
				# 按照IItemItem.Parse的顺序读取字段
				icon = reader.ReadUTFBytesWithLength()

				# 读取可选的itemID数组
				item_id: list[int] = []
				if reader.ReadBoolean():
					item_id_count = reader.ReadSignedInt()
					item_id = [reader.ReadSignedInt() for _ in range(item_id_count)]

				name = reader.ReadUTFBytesWithLength()
				price = reader.ReadSignedInt()
				product_id = reader.ReadSignedInt()
				vip = reader.ReadFloat()

				item = ProductDiamondItem(
					icon=icon,
					name=name,
					item_id=item_id,
					price=price,
					product_id=product_id,
					vip=vip,
				)
				result['root']['item'].append(item)

		return result
