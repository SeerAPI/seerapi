from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AchievementRuleItem(TypedDict):
	"""成就规则项"""

	abtext: str
	ach_name: str  # 对应 C# 的 achName
	desc: str  # 对应 C# 的 Desc
	threshold: str  # 对应 C# 的 Threshold
	title: str
	title_color: str  # 对应 C# 的 titleColor
	ability_title: int  # 对应 C# 的 AbilityTitle
	achievement_point: int  # 对应 C# 的 AchievementPoint
	hide: int
	id: int  # 对应 C# 的 ID
	proicon: int
	spe_name_bonus: int  # 对应 C# 的 SpeNameBonus


class AchievementBranchItem(TypedDict):
	"""成就分支项"""

	text: str  # 对应 C# 的 _text
	desc: str  # 对应 C# 的 Desc
	rule: list[AchievementRuleItem]  # 对应 C# 的 Rule[]
	id: int  # 对应 C# 的 ID
	is_show_pro: int  # 对应 C# 的 isShowPro
	is_single: int  # 对应 C# 的 IsSingle


class AchievementBranchesItem(TypedDict):
	"""成就分支集合项"""

	branch: list[AchievementBranchItem]  # 对应 C# 的 Branch[]


class AchievementTypeItem(TypedDict):
	"""成就类型项"""

	branches: list[AchievementBranchesItem]  # 对应 C# 的 Branches[]
	desc: str  # 对应 C# 的 Desc
	id: int  # 对应 C# 的 ID


class AchievementRulesRoot(TypedDict):
	"""成就规则根节点"""

	type: list[AchievementTypeItem]  # 对应 C# 的 type[]


class AchievementsConfig(TypedDict):
	"""成就系统顶层数据"""

	achievement_rules: AchievementRulesRoot  # 对应 C# 的 AchievementRules


class AchievementsParser(BaseParser[AchievementsConfig]):
	"""成就系统配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'achievements.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'achievements.json'

	def _parse_rule_item(self, reader: BytesReader) -> AchievementRuleItem:
		"""解析成就规则项"""
		# 按照IRuleItem.Parse的顺序读取字段
		ability_title = reader.ReadSignedInt()
		achievement_point = reader.ReadSignedInt()
		desc = reader.ReadUTFBytesWithLength()
		id = reader.ReadSignedInt()
		spe_name_bonus = reader.ReadSignedInt()
		threshold = reader.ReadUTFBytesWithLength()
		abtext = reader.ReadUTFBytesWithLength()
		ach_name = reader.ReadUTFBytesWithLength()
		hide = reader.ReadSignedInt()
		proicon = reader.ReadSignedInt()
		title = reader.ReadUTFBytesWithLength()
		title_color = reader.ReadUTFBytesWithLength()

		return AchievementRuleItem(
			abtext=abtext,
			ach_name=ach_name,
			desc=desc,
			threshold=threshold,
			title=title,
			title_color=title_color,
			ability_title=ability_title,
			achievement_point=achievement_point,
			hide=hide,
			id=id,
			proicon=proicon,
			spe_name_bonus=spe_name_bonus,
		)

	def _parse_branch_item(self, reader: BytesReader) -> AchievementBranchItem:
		"""解析成就分支项"""
		# 按照IBranchItem.Parse的顺序读取字段
		desc = reader.ReadUTFBytesWithLength()
		id = reader.ReadSignedInt()
		is_single = reader.ReadSignedInt()

		# 读取可选的Rule数组
		rule_items: list[AchievementRuleItem] = []
		if reader.ReadBoolean():
			rule_count = reader.ReadSignedInt()
			for _ in range(rule_count):
				rule_items.append(self._parse_rule_item(reader))

		text = reader.ReadUTFBytesWithLength()
		is_show_pro = reader.ReadSignedInt()

		return AchievementBranchItem(
			text=text,
			desc=desc,
			rule=rule_items,
			id=id,
			is_show_pro=is_show_pro,
			is_single=is_single,
		)

	def _parse_branches_item(self, reader: BytesReader) -> AchievementBranchesItem:
		"""解析成就分支集合项"""
		branch_items: list[AchievementBranchItem] = []

		# 读取可选的Branch数组
		if reader.ReadBoolean():
			branch_count = reader.ReadSignedInt()
			for _ in range(branch_count):
				branch_items.append(self._parse_branch_item(reader))

		return AchievementBranchesItem(branch=branch_items)

	def _parse_type_item(self, reader: BytesReader) -> AchievementTypeItem:
		"""解析成就类型项"""
		branches_items: list[AchievementBranchesItem] = []

		# 读取可选的Branches数组
		if reader.ReadBoolean():
			branches_count = reader.ReadSignedInt()
			for _ in range(branches_count):
				branches_items.append(self._parse_branches_item(reader))

		desc = reader.ReadUTFBytesWithLength()
		id = reader.ReadSignedInt()

		return AchievementTypeItem(branches=branches_items, desc=desc, id=id)

	def parse(self, data: bytes) -> AchievementsConfig:
		reader = BytesReader(data)
		result: AchievementsConfig = {'achievement_rules': {'type': []}}

		# 检查header - 根据IRootInterface.Parse逻辑
		if not reader.ReadBoolean():
			return result

		# 检查是否有AchievementRules数据
		if reader.ReadBoolean():
			# 读取type数组
			type_items: list[AchievementTypeItem] = []
			type_count = reader.ReadSignedInt()
			for _ in range(type_count):
				type_items.append(self._parse_type_item(reader))

			result['achievement_rules']['type'] = type_items

		return result
