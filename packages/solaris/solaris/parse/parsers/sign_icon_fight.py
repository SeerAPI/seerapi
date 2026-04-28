"""解析赛尔号客户端的战斗印记图标配置数据文件。"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


# 配置项数据结构
class ItemItem(TypedDict):
	"""配置项"""

	class_name: str
	dec: str
	des: str
	frame: list[str]
	num_des: str
	sp_des: list[str]
	sp_icon: list[str]
	sp_tips: list[str]
	tips: str
	id: int
	is_show_num: int
	show_monster: int
	show_time: int
	sort: int


# 配置容器结构
class _Config(TypedDict):
	"""配置容器"""

	item: list[ItemItem]


# 顶层数据结构
class _SignIconFightConfig(TypedDict):
	"""战斗印记图标配置数据"""

	config: _Config


class SignIconFightParser(BaseParser[_SignIconFightConfig]):
	"""战斗印记图标配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'signIcon_fight.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'signIconFight.json'

	def parse(self, data: bytes) -> _SignIconFightConfig:
		reader = BytesReader(data)
		result: _SignIconFightConfig = {'config': {'item': []}}

		# 检查是否有配置数据
		if not reader.ReadBoolean():
			return result

		# 解析配置容器
		if reader.ReadBoolean():
			item_count = reader.ReadSignedInt()
			for _ in range(item_count):
				# 按照 C# 代码的顺序严格读取字段
				des = reader.ReadUTFBytesWithLength()
				num_des = reader.ReadUTFBytesWithLength()
				class_name = reader.ReadUTFBytesWithLength()
				dec = reader.ReadUTFBytesWithLength()

				# 可选的 frame 数组
				frame: list[str] = []
				if reader.ReadBoolean():
					frame_count = reader.ReadSignedInt()
					frame = [
						reader.ReadUTFBytesWithLength() for _ in range(frame_count)
					]

				# 读取整数字段
				item_id = reader.ReadSignedInt()
				is_show_num = reader.ReadSignedInt()
				show_monster = reader.ReadSignedInt()
				show_time = reader.ReadSignedInt()
				sort = reader.ReadSignedInt()

				# 可选的 spDes 数组
				sp_des: list[str] = []
				if reader.ReadBoolean():
					sp_des_count = reader.ReadSignedInt()
					sp_des = [
						reader.ReadUTFBytesWithLength() for _ in range(sp_des_count)
					]

				# 可选的 spicon 数组
				sp_icon: list[str] = []
				if reader.ReadBoolean():
					sp_icon_count = reader.ReadSignedInt()
					sp_icon = [
						reader.ReadUTFBytesWithLength() for _ in range(sp_icon_count)
					]

				# 可选的 sptips 数组
				sp_tips: list[str] = []
				if reader.ReadBoolean():
					sp_tips_count = reader.ReadSignedInt()
					sp_tips = [
						reader.ReadUTFBytesWithLength() for _ in range(sp_tips_count)
					]

				# 读取最后的 tips 字段
				tips = reader.ReadUTFBytesWithLength()

				# 构建配置项
				item: ItemItem = {
					'class_name': class_name,
					'dec': dec,
					'des': des,
					'frame': frame,
					'num_des': num_des,
					'sp_des': sp_des,
					'sp_icon': sp_icon,
					'sp_tips': sp_tips,
					'tips': tips,
					'id': item_id,
					'is_show_num': is_show_num,
					'show_monster': show_monster,
					'show_time': show_time,
					'sort': sort,
				}
				result['config']['item'].append(item)

		return result
