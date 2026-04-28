"""刻印相关配置解析器

解析赛尔号客户端的刻印数据文件，包含刻印项和刻印分类信息。
"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 刻印分类项数据结构
class MintmarkClassItem(TypedDict):
	"""刻印分类项"""

	class_name: str
	id: int


# 刻印项数据结构
class MintMarkItem(TypedDict):
	"""刻印项"""

	des: str
	effect_des: str
	arg: list[int]
	base_attri_value: list[int]
	extra_attri_value: list[int]
	max_attri_value: list[int]
	monster_id: list[int]
	move_id: list[int]
	grade: int
	id: int
	level: int
	max: int
	mintmark_class: int
	quality: int
	rare: int
	rarity: int
	total_consume: int
	type: int
	connect: int
	hide: int


# 刻印容器结构
class _MintMarks(TypedDict):
	"""刻印容器"""

	mint_mark: list[MintMarkItem]
	mintmark_class: list[MintmarkClassItem]


# 顶层数据结构
class MintmarkConfig(TypedDict):
	"""刻印配置数据"""

	mint_marks: _MintMarks


class MintmarkParser(BaseParser[MintmarkConfig]):
	"""刻印配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'mintmark.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'mintmark.json'

	def parse(self, data: bytes) -> MintmarkConfig:
		reader = BytesReader(data)
		result: MintmarkConfig = {'mint_marks': {'mint_mark': [], 'mintmark_class': []}}

		# 检查是否有刻印数据
		if not reader.ReadBoolean():
			return result

		# 解析刻印容器
		# 解析刻印项列表
		if reader.ReadBoolean():
			mintmark_count = reader.ReadSignedInt()
			for _ in range(mintmark_count):
				# 解析刻印项 - 严格按照C#代码顺序读取

				# 1. 可选的 Arg 数组
				arg_list: list[int] = []
				if reader.ReadBoolean():
					arg_count = reader.ReadSignedInt()
					arg_list = [reader.ReadSignedInt() for _ in range(arg_count)]

				# 2. 可选的 BaseAttriValue 数组
				base_attri_value_list: list[int] = []
				if reader.ReadBoolean():
					base_count = reader.ReadSignedInt()
					base_attri_value_list = [
						reader.ReadSignedInt() for _ in range(base_count)
					]

				connect = reader.ReadSignedInt()
				# 3. Des 和 EffectDes 字符串
				des = reader.ReadUTFBytesWithLength()
				effect_des = reader.ReadUTFBytesWithLength()

				# 4. 可选的 ExtraAttriValue 数组
				extra_attri_value_list: list[int] = []
				if reader.ReadBoolean():
					extra_count = reader.ReadSignedInt()
					extra_attri_value_list = [
						reader.ReadSignedInt() for _ in range(extra_count)
					]

				# 5. 基本整型字段
				grade = reader.ReadSignedInt()
				hide = reader.ReadSignedInt()
				id_value = reader.ReadSignedInt()
				level = reader.ReadSignedInt()
				max_value = reader.ReadSignedInt()

				# 6. 可选的 MaxAttriValue 数组
				max_attri_value_list: list[int] = []
				if reader.ReadBoolean():
					max_attri_count = reader.ReadSignedInt()
					max_attri_value_list = [
						reader.ReadSignedInt() for _ in range(max_attri_count)
					]

				# 7. MintmarkClass
				mintmark_class = reader.ReadSignedInt()

				# 8. 可选的 MonsterID 数组
				monster_id_list: list[int] = []
				if reader.ReadBoolean():
					monster_count = reader.ReadSignedInt()
					monster_id_list = [
						reader.ReadSignedInt() for _ in range(monster_count)
					]

				# 9. 可选的 MoveID 数组
				move_id_list: list[int] = []
				if reader.ReadBoolean():
					move_count = reader.ReadSignedInt()
					move_id_list = [reader.ReadSignedInt() for _ in range(move_count)]

				# 10. 剩余的整型字段
				quality = reader.ReadSignedInt()
				rare = reader.ReadSignedInt()
				rarity = reader.ReadSignedInt()
				total_consume = reader.ReadSignedInt()
				type_value = reader.ReadSignedInt()

				mintmark_item: MintMarkItem = {
					'des': des,
					'effect_des': effect_des,
					'arg': arg_list,
					'base_attri_value': base_attri_value_list,
					'extra_attri_value': extra_attri_value_list,
					'max_attri_value': max_attri_value_list,
					'monster_id': monster_id_list,
					'move_id': move_id_list,
					'grade': grade,
					'id': id_value,
					'level': level,
					'max': max_value,
					'mintmark_class': mintmark_class,
					'quality': quality,
					'rare': rare,
					'rarity': rarity,
					'total_consume': total_consume,
					'type': type_value,
					'connect': connect,
					'hide': hide,
				}
				result['mint_marks']['mint_mark'].append(mintmark_item)

		# 解析刻印分类列表
		if reader.ReadBoolean():
			class_count = reader.ReadSignedInt()
			for _ in range(class_count):
				# 解析刻印分类项
				class_name = reader.ReadUTFBytesWithLength()
				class_id = reader.ReadSignedInt()

				class_item: MintmarkClassItem = {
					'class_name': class_name,
					'id': class_id,
				}
				result['mint_marks']['mintmark_class'].append(class_item)

		return result
