"""Autocard Effect Icon Des 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AutocardEffectIconDesInfo(TypedDict):
    """Autocard Effect Icon Des 信息条目"""

    des: str
    name: str
    resource_name: str
    id: int


class AutocardEffectIconDesConfig(TypedDict):
    """Autocard Effect Icon Des 配置数据"""

    data: list[AutocardEffectIconDesInfo]


class AutocardEffectIconDesParser(BaseParser[AutocardEffectIconDesConfig]):
    """解析 autocardEffectIconDes.bytes 配置文件"""

    @classmethod
    def source_config_filename(cls) -> str:
        return "autocardEffectIconDes.bytes"

    @classmethod
    def parsed_config_filename(cls) -> str:
        return "autocardEffectIconDes.json"

    def parse(self, data: bytes) -> AutocardEffectIconDesConfig:
        reader = BytesReader(data)
        result = AutocardEffectIconDesConfig(data=[])

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            des = reader.ReadUTFBytesWithLength()
            id_val = reader.ReadSignedInt()
            name = reader.ReadUTFBytesWithLength()
            resource_name = reader.ReadUTFBytesWithLength()

            result["data"].append(
                AutocardEffectIconDesInfo(
                    des=des,
                    name=name,
                    resource_name=resource_name,
                    id=id_val,
                )
            )

        return result
