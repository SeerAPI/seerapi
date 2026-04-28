from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ProductMoneyItem(TypedDict):
	"""金币产品项"""

	name: str
	item_id: list[int]  # 对应 C# 的 itemID[]
	gold: int
	price: float
	product_id: int  # 对应 C# 的 productID
	vip: int


class _ProductMoneyRoot(TypedDict):
	"""金币产品根节点"""

	item: list[ProductMoneyItem]


class ProductMoneyConfig(TypedDict):
	"""金币产品顶层数据"""

	root: _ProductMoneyRoot


class ProductMoneyParser(BaseParser[ProductMoneyConfig]):
	"""金币产品配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'product_money.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'productMoney.json'

	def parse(self, data: bytes) -> ProductMoneyConfig:
		reader = BytesReader(data)
		result: ProductMoneyConfig = {'root': {'item': []}}

		# 检查header - 根据IRootInterface.Parse逻辑
		if not reader.ReadBoolean():
			return result

		# 检查是否有item数据 - 根据IRoot.Parse逻辑
		if reader.ReadBoolean():
			count = reader.ReadSignedInt()

			for _ in range(count):
				# 按照IItemItem.Parse的顺序读取字段
				gold = reader.ReadSignedInt()

				# 读取可选的itemID数组
				item_id: list[int] = []
				if reader.ReadBoolean():
					item_id_count = reader.ReadSignedInt()
					item_id = [reader.ReadSignedInt() for _ in range(item_id_count)]

				name = reader.ReadUTFBytesWithLength()
				price = reader.ReadFloat()
				product_id = reader.ReadSignedInt()
				vip = reader.ReadSignedInt()

				item = ProductMoneyItem(
					name=name,
					item_id=item_id,
					gold=gold,
					price=price,
					product_id=product_id,
					vip=vip,
				)
				result['root']['item'].append(item)

		return result
