"""Autocard Skin 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AutocardSkinInfo(TypedDict):
    """Autocard Skin 信息条目"""

    name: str
    skin_name: str
    content_id: int
    id: int
    series: int
    type: int


class AutocardSkinConfig(TypedDict):
    """Autocard Skin 配置数据"""

    data: list[AutocardSkinInfo]


class AutocardSkinParser(BaseParser[AutocardSkinConfig]):
    """解析 autocardSkin.bytes 配置文件"""

    @classmethod
    def source_config_filename(cls) -> str:
        return "autocardSkin.bytes"

    @classmethod
    def parsed_config_filename(cls) -> str:
        return "autocardSkin.json"

    def parse(self, data: bytes) -> AutocardSkinConfig:
        reader = BytesReader(data)
        result = AutocardSkinConfig(data=[])

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            content_id = reader.ReadSignedInt()
            id_val = reader.ReadSignedInt()
            name = reader.ReadUTFBytesWithLength()
            series = reader.ReadSignedInt()
            skin_name = reader.ReadUTFBytesWithLength()
            type_val = reader.ReadSignedInt()

            result["data"].append(
                AutocardSkinInfo(
                    name=name,
                    skin_name=skin_name,
                    content_id=content_id,
                    id=id_val,
                    series=series,
                    type=type_val,
                )
            )

        return result
