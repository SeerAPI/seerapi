from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 效果图标项结构定义
class EffectIconItem(TypedDict):
	"""效果图标项数据结构"""

	analyze: str
	args: str
	come: str
	des: list[str]  # 可选字符串数组
	tag: list[str]  # 可选字符串数组
	tips: str
	kind: list[int]  # 可选整数数组
	pet_id: list[int]  # 可选整数数组
	specific_id: list[int]  # 可选整数数组
	effect_id: int
	icon_id: int
	id: int
	intensify: int
	is_adv: int
	label: int
	limited_type: int
	target: int
	to: int
	type: int


# 内部根结构
class _Root(TypedDict):
	effect: list[EffectIconItem]


# 顶层数据结构
class EffectIconConfig(TypedDict):
	root: _Root


# 效果图标Parser实现
class EffectIconParser(BaseParser[EffectIconConfig]):
	"""解析效果图标配置数据"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'effectIcon.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'effectIcon.json'

	def parse(self, data: bytes) -> EffectIconConfig:
		reader = BytesReader(data)
		result: EffectIconConfig = {'root': {'effect': []}}

		# 检查根布尔标志
		if not reader.read_bool():
			return result

		# 检查effect数组存在标志
		if not reader.read_bool():
			return result

		# 读取数组数量
		count = reader.read_i32()

		# 循环读取效果图标项（严格按照C#解析顺序）
		for _ in range(count):
			# 按照C# Parse方法的顺序读取所有字段
			item_id = reader.read_i32()  # Id
			analyze = reader.ReadUTFBytesWithLength()
			args = reader.ReadUTFBytesWithLength()
			come = reader.ReadUTFBytesWithLength()

			# 处理可选的des字符串数组
			des: list[str] = []
			if reader.read_bool():
				des_count = reader.read_i32()
				des = [reader.ReadUTFBytesWithLength() for _ in range(des_count)]

			effect_id = reader.read_i32()  # effectId
			icon_id = reader.read_i32()  # iconId
			intensify = reader.read_i32()  # intensify
			is_adv = reader.read_i32()  # isAdv

			# 处理可选的kind整数数组
			kind: list[int] = []
			if reader.read_bool():
				kind_count = reader.read_i32()
				kind = [reader.read_i32() for _ in range(kind_count)]

			label = reader.read_i32()  # label
			limited_type = reader.read_i32()  # limitedType

			# 处理可选的petId整数数组
			pet_id: list[int] = []
			if reader.read_bool():
				pet_id_count = reader.read_i32()
				pet_id = [reader.read_i32() for _ in range(pet_id_count)]

			# 处理可选的specificId整数数组
			specific_id: list[int] = []
			if reader.read_bool():
				specific_id_count = reader.read_i32()
				specific_id = [reader.read_i32() for _ in range(specific_id_count)]

			# 处理可选的tag字符串数组
			tag: list[str] = []
			if reader.read_bool():
				tag_count = reader.read_i32()
				tag = [reader.ReadUTFBytesWithLength() for _ in range(tag_count)]

			target = reader.read_i32()
			tips = reader.ReadUTFBytesWithLength()
			to = reader.read_i32()
			type_ = reader.read_i32()

			effect_item: EffectIconItem = {
				'analyze': analyze,
				'args': args,
				'come': come,
				'des': des,
				'tag': tag,
				'tips': tips,
				'kind': kind,
				'pet_id': pet_id,
				'specific_id': specific_id,
				'effect_id': effect_id,
				'icon_id': icon_id,
				'id': item_id,
				'intensify': intensify,
				'is_adv': is_adv,
				'label': label,
				'limited_type': limited_type,
				'target': target,
				'to': to,
				'type': type_,
			}
			result['root']['effect'].append(effect_item)

		return result
