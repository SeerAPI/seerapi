"""许愿系统相关的解析器

包含 Wishsuit（套装许愿）、Wishskin（皮肤许愿）、Wishpet（精灵许愿）、
Wishpart（部件许愿）四个解析器。
"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader

# ============ Wishsuit 相关结构 ============


class WishsuitItem(TypedDict):
	"""套装许愿项目"""

	suit_id: int
	suit_name: str
	suit_part_1: int
	suit_part_2: int
	suit_part_3: int
	suit_part_4: int
	suit_part_5: int
	wishrank_id: int
	wishsuit_id: int


class _WishsuitsContainer(TypedDict):
	wishsuit: list[WishsuitItem]


class WishsuitConfig(TypedDict):
	wishsuits: _WishsuitsContainer | None


# ============ Wishskin 相关结构 ============


class WishskinItem(TypedDict):
	"""皮肤许愿项目"""

	mon_id: int
	pet_skin_id: int
	wishskin_id: int


class _WishskinsContainer(TypedDict):
	wishskin: list[WishskinItem]


class WishskinConfig(TypedDict):
	wishskins: _WishskinsContainer | None


# ============ Wishpet 相关结构 ============


class WishpetItem(TypedDict):
	"""精灵许愿项目"""

	monster_id: int
	monster_star: int
	wish_progress: int
	wishpet_id: int


class _WishpetsContainer(TypedDict):
	wishpet: list[WishpetItem]


class WishpetConfig(TypedDict):
	wishpets: _WishpetsContainer | None


# ============ Wishpart 相关结构 ============


class WishpartItem(TypedDict):
	"""部件许愿项目"""

	part_item_id: int
	part_item_name: str
	part_item_type: str
	wishpart_id: int
	wishrank_id: int


class _WishpartsContainer(TypedDict):
	wishpart: list[WishpartItem]


class WishpartConfig(TypedDict):
	wishparts: _WishpartsContainer | None


# ============ Parser 实现 ============


class WishsuitParser(BaseParser[WishsuitConfig]):
	"""套装许愿解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'Wishsuit.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'wishsuit.json'

	def parse(self, data: bytes) -> WishsuitConfig:
		reader = BytesReader(data)
		result: WishsuitConfig = {'wishsuits': None}

		# 检查是否有许愿套装数据
		if reader.ReadBoolean():
			# 创建容器
			container: _WishsuitsContainer = {'wishsuit': []}

			# 检查是否有具体数据
			if reader.ReadBoolean():
				count = reader.ReadSignedInt()

				for _ in range(count):
					item: WishsuitItem = {
						'suit_id': reader.ReadSignedInt(),
						'suit_name': reader.ReadUTFBytesWithLength(),
						'suit_part_1': reader.ReadSignedInt(),
						'suit_part_2': reader.ReadSignedInt(),
						'suit_part_3': reader.ReadSignedInt(),
						'suit_part_4': reader.ReadSignedInt(),
						'suit_part_5': reader.ReadSignedInt(),
						'wishrank_id': reader.ReadSignedInt(),
						'wishsuit_id': reader.ReadSignedInt(),
					}
					container['wishsuit'].append(item)

			result['wishsuits'] = container

		return result


class WishskinParser(BaseParser[WishskinConfig]):
	"""皮肤许愿解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'Wishskin.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'wishskin.json'

	def parse(self, data: bytes) -> WishskinConfig:
		reader = BytesReader(data)
		result: WishskinConfig = {'wishskins': None}

		# 检查是否有许愿皮肤数据
		if reader.ReadBoolean():
			# 创建容器
			container: _WishskinsContainer = {'wishskin': []}

			# 检查是否有具体数据
			if reader.ReadBoolean():
				count = reader.ReadSignedInt()

				for _ in range(count):
					item: WishskinItem = {
						'mon_id': reader.ReadSignedInt(),
						'pet_skin_id': reader.ReadSignedInt(),
						'wishskin_id': reader.ReadSignedInt(),
					}
					container['wishskin'].append(item)

			result['wishskins'] = container

		return result


class WishpetParser(BaseParser[WishpetConfig]):
	"""精灵许愿解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'Wishpet.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'wishpet.json'

	def parse(self, data: bytes) -> WishpetConfig:
		reader = BytesReader(data)
		result: WishpetConfig = {'wishpets': None}

		# 检查是否有许愿精灵数据
		if reader.ReadBoolean():
			# 创建容器
			container: _WishpetsContainer = {'wishpet': []}

			# 检查是否有具体数据
			if reader.ReadBoolean():
				count = reader.ReadSignedInt()

				for _ in range(count):
					item: WishpetItem = {
						'monster_id': reader.ReadSignedInt(),
						'monster_star': reader.ReadSignedInt(),
						'wish_progress': reader.ReadSignedInt(),
						'wishpet_id': reader.ReadSignedInt(),
					}
					container['wishpet'].append(item)

			result['wishpets'] = container

		return result


class WishpartParser(BaseParser[WishpartConfig]):
	"""部件许愿解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'Wishpart.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'wishpart.json'

	def parse(self, data: bytes) -> WishpartConfig:
		reader = BytesReader(data)
		result: WishpartConfig = {'wishparts': None}

		# 检查是否有许愿部件数据
		if reader.ReadBoolean():
			# 创建容器
			container: _WishpartsContainer = {'wishpart': []}

			# 检查是否有具体数据
			if reader.ReadBoolean():
				count = reader.ReadSignedInt()

				for _ in range(count):
					item: WishpartItem = {
						'part_item_id': reader.ReadSignedInt(),
						'part_item_name': reader.ReadUTFBytesWithLength(),
						'part_item_type': reader.ReadUTFBytesWithLength(),
						'wishpart_id': reader.ReadSignedInt(),
						'wishrank_id': reader.ReadSignedInt(),
					}
					container['wishpart'].append(item)

			result['wishparts'] = container

		return result
