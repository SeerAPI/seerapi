"""Autocard Player 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AutocardPlayerInfo(TypedDict):
    """Autocard Player 信息条目"""

    action_1: str
    action_2: str
    action_3: str
    des: str
    name: str
    resource: str
    id: int
    jumpinfo: int
    move_speed: int
    rarity: int


class AutocardPlayerConfig(TypedDict):
    """Autocard Player 配置数据"""

    data: list[AutocardPlayerInfo]


class AutocardPlayerParser(BaseParser[AutocardPlayerConfig]):
    """解析 autocardPlayer.bytes 配置文件"""

    @classmethod
    def source_config_filename(cls) -> str:
        return "autocardPlayer.bytes"

    @classmethod
    def parsed_config_filename(cls) -> str:
        return "autocardPlayer.json"

    def parse(self, data: bytes) -> AutocardPlayerConfig:
        reader = BytesReader(data)
        result = AutocardPlayerConfig(data=[])

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            action_1 = reader.ReadUTFBytesWithLength()
            action_2 = reader.ReadUTFBytesWithLength()
            action_3 = reader.ReadUTFBytesWithLength()
            des = reader.ReadUTFBytesWithLength()
            id_val = reader.ReadSignedInt()
            jumpinfo = reader.ReadSignedInt()
            move_speed = reader.ReadSignedInt()
            name = reader.ReadUTFBytesWithLength()
            rarity = reader.ReadSignedInt()
            resource = reader.ReadUTFBytesWithLength()

            result["data"].append(
                AutocardPlayerInfo(
                    action_1=action_1,
                    action_2=action_2,
                    action_3=action_3,
                    des=des,
                    name=name,
                    resource=resource,
                    id=id_val,
                    jumpinfo=jumpinfo,
                    move_speed=move_speed,
                    rarity=rarity,
                )
            )

        return result
