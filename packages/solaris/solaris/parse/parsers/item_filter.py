"""物品过滤器相关配置解析器

解析赛尔号客户端的物品过滤器数据文件，包含血药、捕获道具等分类信息。
"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 物品项数据结构（在多个地方使用）
class ItemItem(TypedDict):
	"""物品项"""

	name: str
	bonus: float
	b_show_pet_bag: int
	hp: int
	id: int
	is_midle: int
	item_type: int
	max: int
	pp: int
	price: int
	remove_mon_stat: int
	sort: int
	sort2: int  # 对应 C# 中的小写 sort 字段
	tradability: int
	vip_only: int
	vip_tradability: int


# 顶级数据结构
class TopLevel(TypedDict):
	"""顶级数据"""

	item: list[ItemItem]


# 巅峰圣战数据结构
class PeakJihad(TypedDict):
	"""巅峰圣战"""

	des: str
	item: list[ItemItem]


# 血药分类数据结构
class Blood(TypedDict):
	"""血药分类"""

	goblin_king: PeakJihad | None
	item: list[ItemItem]
	peak_jihad: PeakJihad | None
	status: PeakJihad | None
	top_level: TopLevel | None


# 捕获道具数据结构
class Catch(TypedDict):
	"""捕获道具"""

	text: str
	des: str
	item: list[ItemItem]
	sp: TopLevel | None
	super_id: PeakJihad | None


# 根容器结构
class _Root(TypedDict):
	"""根容器"""

	blood: Blood | None
	catch: Catch | None


# 顶层数据结构
class ItemFilterConfig(TypedDict):
	"""物品过滤器配置数据"""

	root: _Root


class ItemFilterParser(BaseParser[ItemFilterConfig]):
	"""物品过滤器配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'itemFilter.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'itemFilter.json'

	def _parse_item_item(self, reader: BytesReader) -> ItemItem:
		"""解析物品项"""
		# 严格按照 C# Parse 方法的顺序读取
		return {
			'bonus': reader.ReadFloat(),
			'hp': reader.ReadSignedInt(),
			'id': reader.ReadSignedInt(),
			'is_midle': reader.ReadSignedInt(),
			'item_type': reader.ReadSignedInt(),
			'max': reader.ReadSignedInt(),
			'name': reader.ReadUTFBytesWithLength(),
			'pp': reader.ReadSignedInt(),
			'price': reader.ReadSignedInt(),
			'remove_mon_stat': reader.ReadSignedInt(),
			'sort': reader.ReadSignedInt(),
			'tradability': reader.ReadSignedInt(),
			'vip_only': reader.ReadSignedInt(),
			'vip_tradability': reader.ReadSignedInt(),
			'b_show_pet_bag': reader.ReadSignedInt(),
			'sort2': reader.ReadSignedInt(),
		}

	def _parse_item_list(self, reader: BytesReader) -> list[ItemItem]:
		"""解析物品项列表"""
		items: list[ItemItem] = []
		if reader.ReadBoolean():
			count = reader.ReadSignedInt()
			for _ in range(count):
				item = self._parse_item_item(reader)
				items.append(item)
		return items

	def _parse_top_level(self, reader: BytesReader) -> TopLevel:
		"""解析顶级数据"""
		return {'item': self._parse_item_list(reader)}

	def _parse_peak_jihad(self, reader: BytesReader) -> PeakJihad:
		"""解析巅峰圣战数据"""
		item = self._parse_item_list(reader)
		des = reader.ReadUTFBytesWithLength()
		return {'des': des, 'item': item}

	def _parse_blood(self, reader: BytesReader) -> Blood:
		"""解析血药数据"""
		# 可选的 GoblinKing
		goblin_king = None
		if reader.ReadBoolean():
			goblin_king = self._parse_peak_jihad(reader)

		# 可选的 Item 数组
		item = self._parse_item_list(reader)

		# 可选的 PeakJihad
		peak_jihad = None
		if reader.ReadBoolean():
			peak_jihad = self._parse_peak_jihad(reader)

		# 可选的 Status
		status = None
		if reader.ReadBoolean():
			status = self._parse_peak_jihad(reader)

		# 可选的 TopLevel
		top_level = None
		if reader.ReadBoolean():
			top_level = self._parse_top_level(reader)

		return {
			'goblin_king': goblin_king,
			'item': item,
			'peak_jihad': peak_jihad,
			'status': status,
			'top_level': top_level,
		}

	def _parse_catch(self, reader: BytesReader) -> Catch:
		"""解析捕获数据"""
		# 可选的 Item 数组
		item = self._parse_item_list(reader)

		# 可选的 SP
		sp = None
		if reader.ReadBoolean():
			sp = self._parse_top_level(reader)

		# 可选的 SUPER_ID
		super_id = None
		if reader.ReadBoolean():
			super_id = self._parse_peak_jihad(reader)

		# 字符串字段
		text = reader.ReadUTFBytesWithLength()
		des = reader.ReadUTFBytesWithLength()

		return {'text': text, 'des': des, 'item': item, 'sp': sp, 'super_id': super_id}

	def parse(self, data: bytes) -> ItemFilterConfig:
		reader = BytesReader(data)
		result: ItemFilterConfig = {'root': {'blood': None, 'catch': None}}

		# 检查是否有数据
		if not reader.ReadBoolean():
			return result

		# 可选的 Blood 数据
		if reader.ReadBoolean():
			result['root']['blood'] = self._parse_blood(reader)

		# 可选的 Catch 数据
		if reader.ReadBoolean():
			result['root']['catch'] = self._parse_catch(reader)

		return result
