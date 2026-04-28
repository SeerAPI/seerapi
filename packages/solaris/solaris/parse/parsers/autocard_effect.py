"""Autocard Effect 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AutocardEffectInfo(TypedDict):
    """Autocard Effect 信息条目"""

    param: str
    param_des: str
    id: int


class AutocardEffectConfig(TypedDict):
    """Autocard Effect 配置数据"""

    data: list[AutocardEffectInfo]


class AutocardEffectParser(BaseParser[AutocardEffectConfig]):
    """解析 autocardEffect.bytes 配置文件"""

    @classmethod
    def source_config_filename(cls) -> str:
        return "autocardEffect.bytes"

    @classmethod
    def parsed_config_filename(cls) -> str:
        return "autocardEffect.json"

    def parse(self, data: bytes) -> AutocardEffectConfig:
        reader = BytesReader(data)
        result = AutocardEffectConfig(data=[])

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            id_val = reader.ReadSignedInt()
            param = reader.ReadUTFBytesWithLength()
            param_des = reader.ReadUTFBytesWithLength()

            result["data"].append(
                AutocardEffectInfo(id=id_val, param=param, param_des=param_des)
            )

        return result
