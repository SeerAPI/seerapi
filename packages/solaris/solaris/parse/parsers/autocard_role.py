"""Autocard Role 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AutocardRoleInfo(TypedDict):
    """Autocard Role 信息条目"""

    buff_id: str
    buff_param: str
    desc: str
    name: str
    skill_name: str
    skill_txt: str
    skill_upgrade: str
    count_num: int
    display: int
    health: int
    id: int
    pic_id: int
    skill_cost_num: int
    skill_game_limit: int
    skill_id: int
    skill_round_limit: int
    skill_type: int


class AutocardRoleConfig(TypedDict):
    """Autocard Role 配置数据"""

    data: list[AutocardRoleInfo]


class AutocardRoleParser(BaseParser[AutocardRoleConfig]):
    """解析 autocardRole.bytes 配置文件"""

    @classmethod
    def source_config_filename(cls) -> str:
        return "autocardRole.bytes"

    @classmethod
    def parsed_config_filename(cls) -> str:
        return "autocardRole.json"

    def parse(self, data: bytes) -> AutocardRoleConfig:
        reader = BytesReader(data)
        result = AutocardRoleConfig(data=[])

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            buff_id = reader.ReadUTFBytesWithLength()
            buff_param = reader.ReadUTFBytesWithLength()
            count_num = reader.ReadSignedInt()
            display = reader.ReadSignedInt()
            desc = reader.ReadUTFBytesWithLength()
            health = reader.ReadSignedInt()
            id_val = reader.ReadSignedInt()
            name = reader.ReadUTFBytesWithLength()
            pic_id = reader.ReadSignedInt()
            skill_cost_num = reader.ReadSignedInt()
            skill_game_limit = reader.ReadSignedInt()
            skill_id = reader.ReadSignedInt()
            skill_name = reader.ReadUTFBytesWithLength()
            skill_round_limit = reader.ReadSignedInt()
            skill_txt = reader.ReadUTFBytesWithLength()
            skill_type = reader.ReadSignedInt()
            skill_upgrade = reader.ReadUTFBytesWithLength()

            result["data"].append(
                AutocardRoleInfo(
                    buff_id=buff_id,
                    buff_param=buff_param,
                    desc=desc,
                    name=name,
                    skill_name=skill_name,
                    skill_txt=skill_txt,
                    skill_upgrade=skill_upgrade,
                    count_num=count_num,
                    display=display,
                    health=health,
                    id=id_val,
                    pic_id=pic_id,
                    skill_cost_num=skill_cost_num,
                    skill_game_limit=skill_game_limit,
                    skill_id=skill_id,
                    skill_round_limit=skill_round_limit,
                    skill_type=skill_type,
                )
            )

        return result
