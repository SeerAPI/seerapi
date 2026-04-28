from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ShopItem(TypedDict):
	"""商店物品项"""

	check_buy: str  # 对应 C# 的 checkBuy
	name: str
	tip: str
	checkown: list[int]  # 对应 C# 的 checkown[]
	item_id: list[int]  # 对应 C# 的 itemID[]
	coins: int
	exchange_id: int  # 对应 C# 的 exchangeId
	exclude_search: int  # 对应 C# 的 excludeSearch
	gold: int
	hide: int
	malldiscount: int
	mint_mark: int  # 对应 C# 的 mintMark
	monster_id: int  # 对应 C# 的 MonsterID
	move_id: int  # 对应 C# 的 moveID
	pop_id: int  # 对应 C# 的 POPID
	price: float
	product_id: int  # 对应 C# 的 productID
	product_type: int  # 对应 C# 的 productType
	skin_id: int  # 对应 C# 的 skinId
	tip2: int
	tip3: int
	type: int
	usenew: int
	vip: float


class ShopMenuItem(TypedDict):
	"""商店菜单项"""

	ad: str
	cls: str
	count_id: str  # 对应 C# 的 countID
	name: str
	view_class: str  # 对应 C# 的 viewClass
	id: int
	page_size: int  # 对应 C# 的 pageSize
	item: list[ShopItem]  # 商品列表
	menu: list['ShopMenuItem']  # 递归的子菜单列表


class _ShopConfigRoot(TypedDict):
	"""商店配置根节点"""

	menu: list[ShopMenuItem]


class ShopConfig(TypedDict):
	"""商店配置顶层数据"""

	root: _ShopConfigRoot


class ShopConfigParser(BaseParser[ShopConfig]):
	"""商店配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'shop_config.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'shopConfig.json'

	def _parse_shop_item(self, reader: BytesReader) -> ShopItem:
		"""解析商店物品项"""
		# 按照 IItemItem.Parse 的顺序读取字段
		monster_id = reader.ReadSignedInt()
		pop_id = reader.ReadSignedInt()
		check_buy = reader.ReadUTFBytesWithLength()

		# 读取可选的 checkown 数组
		checkown: list[int] = []
		if reader.ReadBoolean():
			checkown_count = reader.ReadSignedInt()
			checkown = [reader.ReadSignedInt() for _ in range(checkown_count)]

		coins = reader.ReadSignedInt()
		exchange_id = reader.ReadSignedInt()
		exclude_search = reader.ReadSignedInt()
		gold = reader.ReadSignedInt()
		hide = reader.ReadSignedInt()

		# 读取可选的 itemID 数组
		item_id: list[int] = []
		if reader.ReadBoolean():
			item_id_count = reader.ReadSignedInt()
			item_id = [reader.ReadSignedInt() for _ in range(item_id_count)]

		malldiscount = reader.ReadSignedInt()
		mint_mark = reader.ReadSignedInt()
		move_id = reader.ReadSignedInt()
		name = reader.ReadUTFBytesWithLength()
		price = reader.ReadFloat()
		product_id = reader.ReadSignedInt()
		product_type = reader.ReadSignedInt()
		skin_id = reader.ReadSignedInt()
		tip = reader.ReadUTFBytesWithLength()
		tip2 = reader.ReadSignedInt()
		tip3 = reader.ReadSignedInt()
		type = reader.ReadSignedInt()
		usenew = reader.ReadSignedInt()
		vip = reader.ReadFloat()

		return ShopItem(
			check_buy=check_buy,
			name=name,
			tip=tip,
			checkown=checkown,
			item_id=item_id,
			coins=coins,
			exchange_id=exchange_id,
			exclude_search=exclude_search,
			gold=gold,
			hide=hide,
			malldiscount=malldiscount,
			mint_mark=mint_mark,
			monster_id=monster_id,
			move_id=move_id,
			pop_id=pop_id,
			price=price,
			product_id=product_id,
			product_type=product_type,
			skin_id=skin_id,
			tip2=tip2,
			tip3=tip3,
			type=type,
			usenew=usenew,
			vip=vip,
		)

	def _parse_menu_item(self, reader: BytesReader) -> ShopMenuItem:
		"""解析菜单项（递归）"""
		# 按照 IMenuItem.Parse 的顺序读取字段
		ad = reader.ReadUTFBytesWithLength()
		cls = reader.ReadUTFBytesWithLength()
		count_id = reader.ReadUTFBytesWithLength()
		id = reader.ReadSignedInt()

		# 读取可选的 item 数组
		item_list: list[ShopItem] = []
		if reader.ReadBoolean():
			item_count = reader.ReadSignedInt()
			for _ in range(item_count):
				item_list.append(self._parse_shop_item(reader))

		# 读取可选的递归 menu 数组
		menu_list: list[ShopMenuItem] = []
		if reader.ReadBoolean():
			menu_count = reader.ReadSignedInt()
			for _ in range(menu_count):
				menu_list.append(self._parse_menu_item(reader))

		name = reader.ReadUTFBytesWithLength()
		page_size = reader.ReadSignedInt()
		view_class = reader.ReadUTFBytesWithLength()

		return ShopMenuItem(
			ad=ad,
			cls=cls,
			count_id=count_id,
			name=name,
			view_class=view_class,
			id=id,
			page_size=page_size,
			item=item_list,
			menu=menu_list,
		)

	def parse(self, data: bytes) -> ShopConfig:
		reader = BytesReader(data)
		result: ShopConfig = {'root': {'menu': []}}

		# 检查header - 根据IRootInterface.Parse逻辑
		if not reader.ReadBoolean():
			return result

		# 检查是否有menu数据 - 根据IRoot.Parse逻辑
		if reader.ReadBoolean():
			menu_count = reader.ReadSignedInt()

			for _ in range(menu_count):
				menu_item = self._parse_menu_item(reader)
				result['root']['menu'].append(menu_item)

		return result
