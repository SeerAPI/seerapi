"""
道具优化解析器 11-21

实现道具优化类别11到21的解析器
"""

from ...bytes_reader import BytesReader
from .base_item import BaseItemData, BaseItemParser, ExtendedItemData

# =============================================================================
# 道具类别 10 解析器 (itemsOptimizeCatItems10)
# =============================================================================


class Item10(ExtendedItemData):
	"""道具类别10项"""


class ItemsOptimizeCatItems10Parser(BaseItemParser[Item10]):
	"""道具优化类别10配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems10.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems10.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item10(
			bean=reader.ReadSignedInt(),
			hide=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			sort=reader.ReadSignedInt(),
			use_max=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 11 解析器 (itemsOptimizeCatItems11)
# =============================================================================


class Item11(BaseItemData):
	"""道具类别11项"""

	bean: int
	need_lv: int
	purpose: int
	rank: int
	rarity: int
	sort: int
	type: int
	wd: int


class ItemsOptimizeCatItems11Parser(BaseItemParser[Item11]):
	"""道具优化类别11配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems11.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems11.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item11(
			bean=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			need_lv=reader.ReadSignedInt(),
			rank=reader.ReadSignedInt(),
			rarity=reader.ReadSignedInt(),
			sort=reader.ReadSignedInt(),
			type=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 12 解析器 (itemsOptimizeCatItems12)
# =============================================================================


class Item12(BaseItemData):
	"""道具类别12项"""

	exchange_id: int
	hide: int
	purpose: int
	rarity: int
	sort: int
	target_id: int
	wd: int


class ItemsOptimizeCatItems12Parser(BaseItemParser[Item12]):
	"""道具优化类别12配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems12.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems12.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item12(
			exchange_id=reader.ReadSignedInt(),
			hide=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			rarity=reader.ReadSignedInt(),
			sort=reader.ReadSignedInt(),
			target_id=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 13 解析器 (itemsOptimizeCatItems13)
# =============================================================================


class Item13(ExtendedItemData):
	"""道具类别13项"""

	type: str
	is_special: int
	vip_only: int
	speed: float


class ItemsOptimizeCatItems13Parser(BaseItemParser[Item13]):
	"""道具优化类别13配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems13.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems13.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item13(
			bean=reader.ReadSignedInt(),
			hide=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			sort=reader.ReadSignedInt(),
			use_max=reader.ReadSignedInt(),
			vip_only=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			is_special=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			speed=reader.ReadFloat(),
			type=reader.ReadUTFBytesWithLength(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 14 解析器 (itemsOptimizeCatItems14)
# =============================================================================


class Item14(BaseItemData):
	"""道具类别14项"""

	bean: int
	hide: int
	sort: int
	purpose: int
	wd: int
	rarity: int


class ItemsOptimizeCatItems14Parser(BaseItemParser[Item14]):
	"""道具优化类别14配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems14.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems14.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item14(
			bean=reader.ReadSignedInt(),
			hide=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			rarity=reader.ReadSignedInt(),
			sort=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 15 解析器 (itemsOptimizeCatItems15)
# =============================================================================


class Item15(ExtendedItemData):
	"""道具类别15项"""


class ItemsOptimizeCatItems15Parser(BaseItemParser[Item15]):
	"""道具优化类别15配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems15.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems15.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item15(
			bean=reader.ReadSignedInt(),
			hide=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			sort=reader.ReadSignedInt(),
			use_max=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 16 解析器 (itemsOptimizeCatItems16)
# =============================================================================


class Item16(BaseItemData):
	"""道具类别16项"""


class ItemsOptimizeCatItems16Parser(BaseItemParser[Item16]):
	"""道具优化类别16配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems16.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems16.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item16(
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			cat_id=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 17 解析器 (itemsOptimizeCatItems17)
# =============================================================================


class Item17(BaseItemData):
	"""道具类别17项"""

	bean: int
	hide: int
	sort: int
	purpose: int
	wd: int
	exchange_out_cnt: str
	exchange_out_id: str
	use_end: str
	exchange_id: int
	exchange_type: int
	item_type: int
	life_time: int
	price: int
	rarity: int
	skin_id: int
	target_id: int
	hide_num: int


class ItemsOptimizeCatItems17Parser(BaseItemParser[Item17]):
	"""道具优化类别17配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems17.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems17.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item17(
			bean=reader.ReadSignedInt(),
			exchange_id=reader.ReadSignedInt(),
			exchange_out_cnt=reader.ReadUTFBytesWithLength(),
			exchange_out_id=reader.ReadUTFBytesWithLength(),
			exchange_type=reader.ReadSignedInt(),
			hide=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			item_type=reader.ReadSignedInt(),
			life_time=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			price=reader.ReadSignedInt(),
			rarity=reader.ReadSignedInt(),
			skin_id=reader.ReadSignedInt(),
			sort=reader.ReadSignedInt(),
			target_id=reader.ReadSignedInt(),
			use_end=reader.ReadUTFBytesWithLength(),
			cat_id=reader.ReadSignedInt(),
			hide_num=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 18 解析器 (itemsOptimizeCatItems18)
# =============================================================================


class Item18(BaseItemData):
	"""道具类别18项"""

	bean: int
	hide: int
	sort: int
	purpose: int
	wd: int
	rarity: int


class ItemsOptimizeCatItems18Parser(BaseItemParser[Item18]):
	"""道具优化类别18配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems18.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems18.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item18(
			bean=reader.ReadSignedInt(),
			hide=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			rarity=reader.ReadSignedInt(),
			sort=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 19 解析器 (itemsOptimizeCatItems19)
# =============================================================================


class Item19(BaseItemData):
	"""道具类别19项"""


class ItemsOptimizeCatItems19Parser(BaseItemParser[Item19]):
	"""道具优化类别19配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems19.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems19.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item19(
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			cat_id=reader.ReadSignedInt(),
		)
