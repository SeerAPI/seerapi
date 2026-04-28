from solaris.parse.bytes_reader import BytesReader

from .base_item import BaseItemData, BaseItemParser, ExtendedItemData

# =============================================================================
# 道具类别 20 解析器 (itemsOptimizeCatItems20)
# =============================================================================


class Item20(BaseItemData):
	"""道具类别20项"""


class ItemsOptimizeCatItems20Parser(BaseItemParser[Item20]):
	"""道具优化类别20配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems20.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems20.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item20(
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			cat_id=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 21 解析器 (itemsOptimizeCatItems21)
# =============================================================================


class Item21(BaseItemData):
	"""道具类别21项"""


class ItemsOptimizeCatItems21Parser(BaseItemParser[Item21]):
	"""道具优化类别21配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems21.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems21.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item21(
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			cat_id=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 22 解析器 (itemsOptimizeCatItems22)
# =============================================================================


class Item22(BaseItemData):
	"""道具类别22项"""


class ItemsOptimizeCatItems22Parser(BaseItemParser[Item22]):
	"""道具优化类别22配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems22.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems22.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item22(
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			cat_id=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 23 解析器 (itemsOptimizeCatItems23)
# =============================================================================


class Item23(ExtendedItemData):
	"""道具类别23项"""

	exchange_out_cnt: str
	exchange_out_id: str
	hide: int
	life_time: int
	rarity: int
	icon: int


class ItemsOptimizeCatItems23Parser(BaseItemParser[Item23]):
	"""道具优化类别23配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems23.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems23.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item23(
			bean=reader.ReadSignedInt(),
			exchange_out_cnt=reader.ReadUTFBytesWithLength(),
			exchange_out_id=reader.ReadUTFBytesWithLength(),
			hide=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			life_time=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			rarity=reader.ReadSignedInt(),
			sort=reader.ReadSignedInt(),
			use_max=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			icon=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 24 解析器 (itemsOptimizeCatItems24)
# =============================================================================


class Item24(BaseItemData):
	"""道具类别24项"""

	hide: int
	sort: int
	purpose: int
	wd: int


class ItemsOptimizeCatItems24Parser(BaseItemParser[Item24]):
	"""道具优化类别24配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems24.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems24.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item24(
			hide=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			sort=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 25 解析器 (itemsOptimizeCatItems25)
# =============================================================================


class Item25(BaseItemData):
	"""道具类别25项"""

	hide: int
	life_time: int
	rarity: int
	sort: int
	use_max: int
	wd: int


class ItemsOptimizeCatItems25Parser(BaseItemParser[Item25]):
	"""道具优化类别25配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems25.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems25.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item25(
			hide=reader.ReadSignedInt(),
			id=reader.ReadSignedInt(),
			life_time=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			rarity=reader.ReadSignedInt(),
			sort=reader.ReadSignedInt(),
			use_max=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)


# =============================================================================
# 道具类别 26 解析器 (itemsOptimizeCatItems26)
# =============================================================================


class Item26(BaseItemData):
	"""道具类别26项"""

	sort: int
	rarity: int
	use_max: int
	purpose: int
	wd: int


class ItemsOptimizeCatItems26Parser(BaseItemParser[Item26]):
	"""道具优化类别26配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems26.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemsOptimizeCatItems26.json'

	def parse_item_fields(self, reader: BytesReader):
		return Item26(
			id=reader.ReadSignedInt(),
			max=reader.ReadSignedInt(),
			name=reader.ReadUTFBytesWithLength(),
			rarity=reader.ReadSignedInt(),
			sort=reader.ReadSignedInt(),
			use_max=reader.ReadSignedInt(),
			cat_id=reader.ReadSignedInt(),
			purpose=reader.ReadSignedInt(),
			wd=reader.ReadSignedInt(),
		)
