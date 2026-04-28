from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AchievementRuleBranchItem(TypedDict):
	"""成就规则分支项"""

	id: int  # 对应 C# 的 ID
	is_single: int  # 对应 C# 的 IsSingle


class AchievementRulesRoot(TypedDict):
	"""成就规则根节点"""

	branch: list[AchievementRuleBranchItem]  # 对应 C# 的 Branch 数组


class AchievementRuleConfig(TypedDict):
	"""成就规则顶层数据"""

	achievement_rules: AchievementRulesRoot  # 对应 C# 的 AchievementRules


class AchievementRuleParser(BaseParser[AchievementRuleConfig]):
	"""成就规则配置解析器"""

	@classmethod
	def source_config_filename(cls) -> str:
		return 'achievement_rule.bytes'

	@classmethod
	def parsed_config_filename(cls) -> str:
		return 'achievementRule.json'

	def parse(self, data: bytes) -> AchievementRuleConfig:
		reader = BytesReader(data)
		result: AchievementRuleConfig = {'achievement_rules': {'branch': []}}

		# 检查header - 根据IRootInterface.Parse逻辑
		if not reader.ReadBoolean():
			return result

		# 检查是否有AchievementRules数据 - 根据IAchievementRules.Parse逻辑
		if reader.ReadBoolean():
			branch_count = reader.ReadSignedInt()

			for _ in range(branch_count):
				# 按照IBranchItem.Parse的顺序读取字段
				id = reader.ReadSignedInt()
				is_single = reader.ReadSignedInt()

				branch_item = AchievementRuleBranchItem(id=id, is_single=is_single)
				result['achievement_rules']['branch'].append(branch_item)

		return result
