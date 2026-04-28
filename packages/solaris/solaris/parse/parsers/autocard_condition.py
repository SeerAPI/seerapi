"""Autocard Condition 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AutocardConditionInfo(TypedDict):
    """Autocard Condition 信息条目"""

    param: str
    param_des: str
    id: int


class AutocardConditionConfig(TypedDict):
    """Autocard Condition 配置数据"""

    data: list[AutocardConditionInfo]


class AutocardConditionParser(BaseParser[AutocardConditionConfig]):
    """解析 autocardCondition.bytes 配置文件"""

    @classmethod
    def source_config_filename(cls) -> str:
        return "autocardCondition.bytes"

    @classmethod
    def parsed_config_filename(cls) -> str:
        return "autocardCondition.json"

    def parse(self, data: bytes) -> AutocardConditionConfig:
        reader = BytesReader(data)
        result = AutocardConditionConfig(data=[])

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            id_val = reader.ReadSignedInt()
            param = reader.ReadUTFBytesWithLength()
            param_des = reader.ReadUTFBytesWithLength()

            result["data"].append(
                AutocardConditionInfo(id=id_val, param=param, param_des=param_des)
            )

        return result
