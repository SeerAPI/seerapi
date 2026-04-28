"""skill_effect.bytes 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class SkillEffectItem(TypedDict):
	"""技能效果信息条目"""

	Bosseffective: int
	argsNum: int
	formattingAdjustment: str
	id: int
	ifTextItalic: str
	info: str
	isif: int
	tagA: str
	tagAboss: int
	tagB: str
	tagBboss: int
	tagC: str
	tagCboss: int


class SkillEffectConfig(TypedDict):
	"""技能效果配置数据"""

	data: list[SkillEffectItem]


class SkillEffectParser(BaseParser[SkillEffectConfig]):
	"""解析 skill_effect.bytes 配置文件"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'skill_effect.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'skillEffect.json'

	def parse(self, data: bytes) -> SkillEffectConfig:
		reader = BytesReader(data)
		result = SkillEffectConfig(data=[])

		# 检查是否有数据
		if not reader.ReadBoolean():
			return result

		# 读取数组长度
		count = reader.ReadSignedInt()

		# 循环读取每个 SkillEffectInfo
		for _ in range(count):
			# 按照 ISkillEffectInfo.Parse 方法的读取顺序
			bosseffective = reader.ReadSignedInt()
			args_num = reader.ReadSignedInt()
			formatting_adjustment = reader.ReadUTFBytesWithLength()
			id_val = reader.ReadSignedInt()
			if_text_italic = reader.ReadUTFBytesWithLength()
			info = reader.ReadUTFBytesWithLength()
			isif = reader.ReadSignedInt()
			tag_a = reader.ReadUTFBytesWithLength()
			tag_aboss = reader.ReadSignedInt()
			tag_b = reader.ReadUTFBytesWithLength()
			tag_bboss = reader.ReadSignedInt()
			tag_c = reader.ReadUTFBytesWithLength()
			tag_cboss = reader.ReadSignedInt()

			result['data'].append(
				SkillEffectItem(
					Bosseffective=bosseffective,
					argsNum=args_num,
					formattingAdjustment=formatting_adjustment,
					id=id_val,
					ifTextItalic=if_text_italic,
					info=info,
					isif=isif,
					tagA=tag_a,
					tagAboss=tag_aboss,
					tagB=tag_b,
					tagBboss=tag_bboss,
					tagC=tag_c,
					tagCboss=tag_cboss,
				)
			)

		return result
