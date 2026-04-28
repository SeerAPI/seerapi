"""Autocard Content 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AutocardContentInfo(TypedDict):
    """Autocard Content 信息条目"""

    buff_id: str
    buff_param: str
    card_txt: str
    des: str
    name: str
    attack: int
    compose: int
    compose_to: int
    cost: int
    count_num: int
    display: int
    health: int
    id: int
    is_use: int
    level: int
    nature: int
    pic_id: int
    subtype: int
    type: int


class AutocardContentConfig(TypedDict):
    """Autocard Content 配置数据"""

    data: list[AutocardContentInfo]


class AutocardContentParser(BaseParser[AutocardContentConfig]):
    """解析 autocardContent.bytes 配置文件"""

    @classmethod
    def source_config_filename(cls) -> str:
        return "autocardContent.bytes"

    @classmethod
    def parsed_config_filename(cls) -> str:
        return "autocardContent.json"

    def parse(self, data: bytes) -> AutocardContentConfig:
        reader = BytesReader(data)
        result = AutocardContentConfig(data=[])

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            buff_id = reader.ReadUTFBytesWithLength()
            buff_param = reader.ReadUTFBytesWithLength()
            count_num = reader.ReadSignedInt()
            display = reader.ReadSignedInt()
            attack = reader.ReadSignedInt()
            card_txt = reader.ReadUTFBytesWithLength()
            compose = reader.ReadSignedInt()
            compose_to = reader.ReadSignedInt()
            cost = reader.ReadSignedInt()
            des = reader.ReadUTFBytesWithLength()
            health = reader.ReadSignedInt()
            id_val = reader.ReadSignedInt()
            is_use = reader.ReadSignedInt()
            level = reader.ReadSignedInt()
            name = reader.ReadUTFBytesWithLength()
            nature = reader.ReadSignedInt()
            pic_id = reader.ReadSignedInt()
            subtype = reader.ReadSignedInt()
            type_val = reader.ReadSignedInt()

            result["data"].append(
                AutocardContentInfo(
                    buff_id=buff_id,
                    buff_param=buff_param,
                    card_txt=card_txt,
                    des=des,
                    name=name,
                    attack=attack,
                    compose=compose,
                    compose_to=compose_to,
                    cost=cost,
                    count_num=count_num,
                    display=display,
                    health=health,
                    id=id_val,
                    is_use=is_use,
                    level=level,
                    nature=nature,
                    pic_id=pic_id,
                    subtype=subtype,
                    type=type_val,
                )
            )

        return result
