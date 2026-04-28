"""Autocard Nature 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AutocardNatureInfo(TypedDict):
    """Autocard Nature 信息条目"""

    name: str
    pic_id: str
    id: int


class AutocardNatureConfig(TypedDict):
    """Autocard Nature 配置数据"""

    data: list[AutocardNatureInfo]


class AutocardNatureParser(BaseParser[AutocardNatureConfig]):
    """解析 autocardNature.bytes 配置文件"""

    @classmethod
    def source_config_filename(cls) -> str:
        return "autocardNature.bytes"

    @classmethod
    def parsed_config_filename(cls) -> str:
        return "autocardNature.json"

    def parse(self, data: bytes) -> AutocardNatureConfig:
        reader = BytesReader(data)
        result = AutocardNatureConfig(data=[])

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            id_val = reader.ReadSignedInt()
            name = reader.ReadUTFBytesWithLength()
            pic_id = reader.ReadUTFBytesWithLength()

            result["data"].append(
                AutocardNatureInfo(id=id_val, name=name, pic_id=pic_id)
            )

        return result
