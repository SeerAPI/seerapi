from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class RuleItem(TypedDict):
    """规则项"""

    ability_title: int
    achievement_point: int
    desc: str
    id: int
    spe_name_bonus: int
    threshold: str
    abtext: str
    ach_name: str
    hide: int
    proicon: int
    title: str
    title_color: str


class BranchItem(TypedDict):
    """分支项"""

    desc: str
    id: int
    is_single: int
    rule: list[RuleItem]
    _text: str
    is_show_pro: int


class BranchesItem(TypedDict):
    """分支容器"""

    branch: list[BranchItem]


class TypeItem(TypedDict):
    """类型项"""

    branches: list[BranchesItem]
    desc: str
    id: int


class _AchievementRules(TypedDict):
    """成就规则容器"""

    type: list[TypeItem]


class AchievementsTempConfig(TypedDict):
    """成就模板配置"""

    achievement_rules: _AchievementRules


class AchievementsTempParser(BaseParser[AchievementsTempConfig]):
    """成就模板解析器"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'achievements_temp.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'achievementsTemp.json'

    def parse(self, data: bytes) -> AchievementsTempConfig:
        reader = BytesReader(data)
        result: AchievementsTempConfig = {'achievement_rules': {'type': []}}

        if not reader.ReadBoolean():
            return result

        if not reader.ReadBoolean():
            return result

        type_count = reader.ReadSignedInt()
        for _ in range(type_count):
            branches_list: list[BranchesItem] = []
            if reader.ReadBoolean():
                branches_count = reader.ReadSignedInt()
                for _ in range(branches_count):
                    branch_list: list[BranchItem] = []
                    if reader.ReadBoolean():
                        branch_count = reader.ReadSignedInt()
                        for _ in range(branch_count):
                            desc = reader.ReadUTFBytesWithLength()
                            branch_id = reader.ReadSignedInt()
                            is_single = reader.ReadSignedInt()
                            rule_list: list[RuleItem] = []
                            if reader.ReadBoolean():
                                rule_count = reader.ReadSignedInt()
                                for _ in range(rule_count):
                                    ability_title = reader.ReadSignedInt()
                                    achievement_point = reader.ReadSignedInt()
                                    rule_desc = reader.ReadUTFBytesWithLength()
                                    rule_id = reader.ReadSignedInt()
                                    spe_name_bonus = reader.ReadSignedInt()
                                    threshold = reader.ReadUTFBytesWithLength()
                                    abtext = reader.ReadUTFBytesWithLength()
                                    ach_name = reader.ReadUTFBytesWithLength()
                                    hide = reader.ReadSignedInt()
                                    proicon = reader.ReadSignedInt()
                                    title = reader.ReadUTFBytesWithLength()
                                    title_color = reader.ReadUTFBytesWithLength()

                                    rule_item: RuleItem = {
                                        'ability_title': ability_title,
                                        'achievement_point': achievement_point,
                                        'desc': rule_desc,
                                        'id': rule_id,
                                        'spe_name_bonus': spe_name_bonus,
                                        'threshold': threshold,
                                        'abtext': abtext,
                                        'ach_name': ach_name,
                                        'hide': hide,
                                        'proicon': proicon,
                                        'title': title,
                                        'title_color': title_color,
                                    }
                                    rule_list.append(rule_item)

                            _text = reader.ReadUTFBytesWithLength()
                            is_show_pro = reader.ReadSignedInt()

                            branch_item: BranchItem = {
                                'desc': desc,
                                'id': branch_id,
                                'is_single': is_single,
                                'rule': rule_list,
                                '_text': _text,
                                'is_show_pro': is_show_pro,
                            }
                            branch_list.append(branch_item)

                    branches_item: BranchesItem = {
                        'branch': branch_list,
                    }
                    branches_list.append(branches_item)

            type_desc = reader.ReadUTFBytesWithLength()
            type_id = reader.ReadSignedInt()

            type_item: TypeItem = {
                'branches': branches_list,
                'desc': type_desc,
                'id': type_id,
            }
            result['achievement_rules']['type'].append(type_item)

        return result
