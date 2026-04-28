"""
道具优化解析器 0-10

实现道具优化类别0到10的解析器
"""

from ...bytes_reader import BytesReader
from .base_item import BaseItemData, BaseItemParser, ExtendedItemData

# =============================================================================
# 道具类别 0 解析器 (itemsOptimizeCatItems0)
# =============================================================================


class Item0(ExtendedItemData):
	"""道具类别0项"""

	life_time: int
	price: int
	rarity: int


class ItemsOptimizeCatItems0Parser(BaseItemParser[Item0]):
	"""道具优化类别0配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems0.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems0.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item0(
			bean=reader.ReadSignedInt(),
			hide=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			life_time=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			price=reader.ReadSignedInt(),
			rarity=reader.ReadSignedInt(),
			sort=reader.ReadSignedInt(),
			use_max=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 1 解析器 (itemsOptimizeCatItems1)
# =============================================================================


class Item1(ExtendedItemData):
	"""道具类别1项"""

	life_time: int
	price: int
	repair_price: int
	vip_only: int
	action_dir: int
	is_special: int
	speed: float
	type: str


class ItemsOptimizeCatItems1Parser(BaseItemParser[Item1]):
	"""道具优化类别1配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems1.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems1.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item1(
			bean=reader.ReadSignedInt(),
			hide=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			life_time=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			price=reader.ReadSignedInt(),
			repair_price=reader.ReadSignedInt(),
			sort=reader.ReadSignedInt(),
			use_max=reader.ReadSignedInt(),
			vip_only=reader.ReadSignedInt(),
			action_dir=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			is_special=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			speed=reader.ReadFloat(),
			type=reader.ReadUTFBytesWithLength(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 2 解析器 (itemsOptimizeCatItems2)
# =============================================================================


class Item2(BaseItemData):
	"""道具类别2项"""

	color: str
	price: int
	texture: int


class ItemsOptimizeCatItems2Parser(BaseItemParser[Item2]):
	"""道具优化类别2配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems2.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems2.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item2(
			color=reader.ReadUTFBytesWithLength(),
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			price=reader.ReadSignedInt(),
			texture=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 3 解析器 (itemsOptimizeCatItems3)
# =============================================================================


class Item3(ExtendedItemData):
	"""道具类别3项"""

	ev_remove: int
	incre_mon_lv_to: int
	item_type: int
	limit_pet_class: str
	pp: int
	price: int
	rarity: int
	vip_only: int


class ItemsOptimizeCatItems3Parser(BaseItemParser[Item3]):
	"""道具优化类别3配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems3.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems3.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item3(
			bean=reader.ReadSignedInt(),
			ev_remove=reader.ReadSignedInt(),
			hide=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			incre_mon_lv_to=reader.ReadSignedInt(),
			item_type=reader.ReadSignedInt(),
			limit_pet_class=reader.ReadUTFBytesWithLength(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			pp=reader.ReadSignedInt(),
			price=reader.ReadSignedInt(),
			rarity=reader.ReadSignedInt(),
			sort=reader.ReadSignedInt(),
			use_max=reader.ReadSignedInt(),
			vip_only=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 4 解析器 (itemsOptimizeCatItems4)
# =============================================================================


class Item4(ExtendedItemData):
	"""道具类别4项"""

	price: int
	rarity: int
	vip_only: int


class ItemsOptimizeCatItems4Parser(BaseItemParser[Item4]):
	"""道具优化类别4配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems4.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems4.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item4(
			bean=reader.ReadSignedInt(),
			hide=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			price=reader.ReadSignedInt(),
			rarity=reader.ReadSignedInt(),
			sort=reader.ReadSignedInt(),
			use_max=reader.ReadSignedInt(),
			vip_only=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 5 解析器 (itemsOptimizeCatItems5)
# =============================================================================


class Item5(BaseItemData):
	"""道具类别5项"""

	bean: int
	hide: int
	price: int
	sort: int
	vip_only: int
	purpose: int
	wd: int


class ItemsOptimizeCatItems5Parser(BaseItemParser[Item5]):
	"""道具优化类别5配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems5.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems5.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item5(
			bean=reader.ReadSignedInt(),
			hide=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			price=reader.ReadSignedInt(),
			sort=reader.ReadSignedInt(),
			vip_only=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 6 解析器 (itemsOptimizeCatItems6)
# =============================================================================


class Item6(BaseItemData):
	"""道具类别6项"""

	wd: int


class ItemsOptimizeCatItems6Parser(BaseItemParser[Item6]):
	"""道具优化类别6配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems6.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems6.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item6(
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			cat_id=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 7 解析器 (itemsOptimizeCatItems7)
# =============================================================================


class Item7(BaseItemData):
	"""道具类别7项"""

	bean: int
	hide: int
	sort: int
	hide_num: int
	purpose: int
	wd: int


class ItemsOptimizeCatItems7Parser(BaseItemParser[Item7]):
	"""道具优化类别7配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems7.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems7.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item7(
			bean=reader.ReadSignedInt(),
			hide=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			sort=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			hide_num=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 8 解析器 (itemsOptimizeCatItems8)
# =============================================================================


class Item8(BaseItemData):
	"""道具类别8项"""


class ItemsOptimizeCatItems8Parser(BaseItemParser[Item8]):
	"""道具优化类别8配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems8.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems8.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item8(
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			cat_id=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 9 解析器 (itemsOptimizeCatItems9)
# =============================================================================


class Item9(BaseItemData):
	"""道具类别9项"""


class ItemsOptimizeCatItems9Parser(BaseItemParser[Item9]):
	"""道具优化类别9配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems9.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems9.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item9(
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			cat_id=reader.ReadSignedInt(),
		)
