from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 皮肤种类项结构定义
class _SkinKindItem(TypedDict):
	id: int
	life_time: int
	skin_type: int
	type: int
	year: int


# 皮肤项结构定义
class _SkinItem(TypedDict):
	go: str
	go_type: str
	name: str
	skin_kind: list[_SkinKindItem]
	id: int
	jump_target: int
	mon_id: int
	type: int


class _PetSkins(TypedDict):
	skin: list[_SkinItem]


class PetSkinConfig(TypedDict):
	pet_skins: _PetSkins


class PetSkinParser(BaseParser[PetSkinConfig]):
	"""解析精灵皮肤配置数据"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'pet_skin.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'petSkin.json'

	def parse(self, data: bytes) -> PetSkinConfig:
		reader = BytesReader(data)
		result: PetSkinConfig = {'pet_skins': {'skin': []}}

		# 根标志
		if not reader.read_bool():
			return result

		# PetSkins 容器标志
		if not reader.read_bool():
			return result

		count = reader.read_i32()
		for _ in range(count):
			# 读取 SkinItem（严格遵循 C# 顺序）
			go = reader.ReadUTFBytesWithLength()
			go_type = reader.ReadUTFBytesWithLength()
			id_ = reader.read_i32()
			jump_target = reader.read_i32()
			mon_id = reader.read_i32()
			name = reader.ReadUTFBytesWithLength()

			skin_kind: list[_SkinKindItem] = []
			if reader.read_bool():
				n = reader.read_i32()
				for _ in range(n):
					item: _SkinKindItem = {
						'id': reader.read_i32(),
						'life_time': reader.read_i32(),
						'skin_type': reader.read_i32(),
						'type': reader.read_i32(),
						'year': reader.read_i32(),
					}
					skin_kind.append(item)

			skin_type = reader.read_i32()

			skin_item: _SkinItem = {
				'go': go,
				'go_type': go_type,
				'name': name,
				'skin_kind': skin_kind,
				'id': id_,
				'jump_target': jump_target,
				'mon_id': mon_id,
				'type': skin_type,
			}
			result['pet_skins']['skin'].append(skin_item)

		return result
