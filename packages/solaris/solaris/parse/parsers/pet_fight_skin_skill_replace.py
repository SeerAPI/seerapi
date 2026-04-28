from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PetFightSkillItem(TypedDict):
	"""精灵战斗技能项"""

	action: str
	id: int
	replace_id: int  # 对应 C# 的 replaceId


class PetFightSkinSkillItem(TypedDict):
	"""精灵战斗皮肤技能项"""

	petid: int
	skill: PetFightSkillItem | None  # 可选的技能信息
	skinid: int


class _PetFightSkinSkillRoot(TypedDict):
	"""精灵战斗皮肤技能根节点"""

	item: list[PetFightSkinSkillItem]


class PetFightSkinSkillReplaceConfig(TypedDict):
	"""精灵战斗皮肤技能顶层数据"""

	root: _PetFightSkinSkillRoot


class PetFightSkinSkillReplaceParser(BaseParser[PetFightSkinSkillReplaceConfig]):
	"""精灵战斗皮肤技能替换配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'PetFightSkinSkillReplace.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'petFightSkinSkillReplace.json'

	def parse(self, data: bytes) -> PetFightSkinSkillReplaceConfig:
		reader = BytesReader(data)
		result: PetFightSkinSkillReplaceConfig = {'root': {'item': []}}

		# 检查header - 根据IRootInterface.Parse逻辑
		if not reader.ReadBoolean():
			return result

		# 检查是否有item数据 - 根据IRoot.Parse逻辑
		if reader.ReadBoolean():
			item_count = reader.ReadSignedInt()

			for _ in range(item_count):
				# 按照IItemItem.Parse的顺序读取字段
				petid = reader.ReadSignedInt()

				# 读取可选的skill数据
				skill: PetFightSkillItem | None = None
				if reader.ReadBoolean():
					# 按照ISkill.Parse的顺序读取字段
					action = reader.ReadUTFBytesWithLength()
					id = reader.ReadSignedInt()
					replace_id = reader.ReadSignedInt()

					skill = PetFightSkillItem(
						action=action, id=id, replace_id=replace_id
					)

				skinid = reader.ReadSignedInt()

				item = PetFightSkinSkillItem(petid=petid, skill=skill, skinid=skinid)
				result['root']['item'].append(item)

		return result
