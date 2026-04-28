"""Autocard Buff 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AutocardBuffInfo(TypedDict):
    """Autocard Buff 信息条目"""

    effect_icon: str
    object: str
    param: str
    param_des: str
    id: int
    is_death_effect: int
    is_place_effect: int


class AutocardBuffConfig(TypedDict):
    """Autocard Buff 配置数据"""

    data: list[AutocardBuffInfo]


class AutocardBuffParser(BaseParser[AutocardBuffConfig]):
    """解析 autocardBuff.bytes 配置文件"""

    @classmethod
    def source_config_filename(cls) -> str:
        return "autocardBuff.bytes"

    @classmethod
    def parsed_config_filename(cls) -> str:
        return "autocardBuff.json"

    def parse(self, data: bytes) -> AutocardBuffConfig:
        reader = BytesReader(data)
        result = AutocardBuffConfig(data=[])

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            is_death_effect = reader.ReadSignedInt()
            is_place_effect = reader.ReadSignedInt()
            effect_icon = reader.ReadUTFBytesWithLength()
            id_val = reader.ReadSignedInt()
            object_val = reader.ReadUTFBytesWithLength()
            param = reader.ReadUTFBytesWithLength()
            param_des = reader.ReadUTFBytesWithLength()

            result["data"].append(
                AutocardBuffInfo(
                    effect_icon=effect_icon,
                    object=object_val,
                    param=param,
                    param_des=param_des,
                    id=id_val,
                    is_death_effect=is_death_effect,
                    is_place_effect=is_place_effect,
                )
            )

        return result
