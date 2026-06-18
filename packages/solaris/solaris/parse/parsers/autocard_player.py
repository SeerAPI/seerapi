"""Autocard Player 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AutocardPlayerInfo(TypedDict):
    """Autocard Player 信息条目"""

    action_1: str
    action_2: str
    action_3: str
    book_action_1: str
    book_action_2: str
    book_action_3: str
    des: str
    get_des: str
    name: str
    pos: str
    resource: str
    skin_name: str
    tag: str
    id: int
    jumpinfo: int
    max_level: int
    move_speed: int
    rarity: int
    stat: int


class AutocardPlayerConfig(TypedDict):
    """Autocard Player 配置数据"""

    data: list[AutocardPlayerInfo]


class AutocardPlayerParser(BaseParser[AutocardPlayerConfig]):
    """解析 autocardPlayer.bytes 配置文件"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'autocardPlayer.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'autocardPlayer.json'

    def parse(self, data: bytes) -> AutocardPlayerConfig:
        reader = BytesReader(data)
        result = AutocardPlayerConfig(data=[])

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            max_level = reader.ReadSignedInt()
            pos = reader.ReadUTFBytesWithLength()
            action_1 = reader.ReadUTFBytesWithLength()
            action_2 = reader.ReadUTFBytesWithLength()
            action_3 = reader.ReadUTFBytesWithLength()
            book_action_1 = reader.ReadUTFBytesWithLength()
            book_action_2 = reader.ReadUTFBytesWithLength()
            book_action_3 = reader.ReadUTFBytesWithLength()
            des = reader.ReadUTFBytesWithLength()
            get_des = reader.ReadUTFBytesWithLength()
            id_val = reader.ReadSignedInt()
            jumpinfo = reader.ReadSignedInt()
            move_speed = reader.ReadSignedInt()
            name = reader.ReadUTFBytesWithLength()
            rarity = reader.ReadSignedInt()
            resource = reader.ReadUTFBytesWithLength()
            skin_name = reader.ReadUTFBytesWithLength()
            stat = reader.ReadSignedInt()
            tag = reader.ReadUTFBytesWithLength()

            result['data'].append(
                AutocardPlayerInfo(
                    action_1=action_1,
                    action_2=action_2,
                    action_3=action_3,
                    book_action_1=book_action_1,
                    book_action_2=book_action_2,
                    book_action_3=book_action_3,
                    des=des,
                    get_des=get_des,
                    name=name,
                    pos=pos,
                    resource=resource,
                    skin_name=skin_name,
                    tag=tag,
                    id=id_val,
                    jumpinfo=jumpinfo,
                    max_level=max_level,
                    move_speed=move_speed,
                    rarity=rarity,
                    stat=stat,
                )
            )

        return result
