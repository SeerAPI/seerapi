"""Autocard Skin 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AutocardSkinInfo(TypedDict):
    """Autocard Skin 信息条目"""

    content_id: int
    get_des: str
    id: int
    jump_id: int
    name: str
    series: int
    skin_name: str
    type: int


class AutocardSkinConfig(TypedDict):
    """Autocard Skin 配置数据"""

    data: list[AutocardSkinInfo]


class AutocardSkinParser(BaseParser[AutocardSkinConfig]):
    """解析 autocardSkin.bytes 配置文件"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'autocardSkin.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'autocardSkin.json'

    def parse(self, data: bytes) -> AutocardSkinConfig:
        reader = BytesReader(data)
        result = AutocardSkinConfig(data=[])

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            content_id = reader.ReadSignedInt()
            get_des = reader.ReadUTFBytesWithLength()
            id_val = reader.ReadSignedInt()
            jump_id = reader.ReadSignedInt()
            name = reader.ReadUTFBytesWithLength()
            series = reader.ReadSignedInt()
            skin_name = reader.ReadUTFBytesWithLength()
            type_val = reader.ReadSignedInt()

            result['data'].append(
                AutocardSkinInfo(
                    content_id=content_id,
                    get_des=get_des,
                    id=id_val,
                    jump_id=jump_id,
                    name=name,
                    series=series,
                    skin_name=skin_name,
                    type=type_val,
                )
            )

        return result
