"""Auto Card Recom 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AutoCardRecomInfo(TypedDict):
    """Auto Card Recom 信息条目"""

    ma_card_id: str
    pet_card_id: str
    title: str
    class_id: int
    id: int
    pet_bg: int


class AutoCardRecomConfig(TypedDict):
    """Auto Card Recom 配置数据"""

    data: list[AutoCardRecomInfo]


class AutoCardRecomParser(BaseParser[AutoCardRecomConfig]):
    """解析 autoCardRecom.bytes 配置文件"""

    @classmethod
    def source_config_filename(cls) -> str:
        return "autoCardRecom.bytes"

    @classmethod
    def parsed_config_filename(cls) -> str:
        return "autoCardRecom.json"

    def parse(self, data: bytes) -> AutoCardRecomConfig:
        reader = BytesReader(data)
        result = AutoCardRecomConfig(data=[])

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            ma_card_id = reader.ReadUTFBytesWithLength()
            class_id = reader.ReadSignedInt()
            id_val = reader.ReadSignedInt()
            pet_bg = reader.ReadSignedInt()
            pet_card_id = reader.ReadUTFBytesWithLength()
            title = reader.ReadUTFBytesWithLength()

            result["data"].append(
                AutoCardRecomInfo(
                    ma_card_id=ma_card_id,
                    pet_card_id=pet_card_id,
                    title=title,
                    class_id=class_id,
                    id=id_val,
                    pet_bg=pet_bg,
                )
            )

        return result
