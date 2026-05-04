from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class MintMarkItem(TypedDict):
    """刻印项"""

    arg: list[int]
    base_attri_value: list[int]
    connect: int
    des: str
    effect_des: str
    extra_attri_value: list[int]
    grade: int
    hide: int
    id: int
    level: int
    max: int
    max_attri_value: list[int]
    mintmark_class: int
    monster_id: list[int]
    move_id: list[int]
    quality: int
    rare: int
    rarity: int
    total_consume: int
    type: int


class MintmarkClassItem(TypedDict):
    """刻印分类项"""

    class_name: str
    id: int


class _MintMarks(TypedDict):
    """刻印容器"""

    mint_mark: list[MintMarkItem]
    mintmark_class: list[MintmarkClassItem]


class MintmarkTempConfig(TypedDict):
    """刻印模板配置"""

    mint_marks: _MintMarks


class MintmarkTempParser(BaseParser[MintmarkTempConfig]):
    """刻印模板解析器"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'mintmark_temp.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'mintmarkTemp.json'

    def parse(self, data: bytes) -> MintmarkTempConfig:
        reader = BytesReader(data)
        result: MintmarkTempConfig = {
            'mint_marks': {'mint_mark': [], 'mintmark_class': []}
        }

        if not reader.ReadBoolean():
            return result

        if reader.ReadBoolean():
            mark_count = reader.ReadSignedInt()
            for _ in range(mark_count):
                arg_list: list[int] = []
                if reader.ReadBoolean():
                    arg_count = reader.ReadSignedInt()
                    arg_list = [reader.ReadSignedInt() for _ in range(arg_count)]

                base_attri_list: list[int] = []
                if reader.ReadBoolean():
                    base_count = reader.ReadSignedInt()
                    base_attri_list = [
                        reader.ReadSignedInt() for _ in range(base_count)
                    ]

                connect = reader.ReadSignedInt()
                des = reader.ReadUTFBytesWithLength()
                effect_des = reader.ReadUTFBytesWithLength()

                extra_attri_list: list[int] = []
                if reader.ReadBoolean():
                    extra_count = reader.ReadSignedInt()
                    extra_attri_list = [
                        reader.ReadSignedInt() for _ in range(extra_count)
                    ]

                grade = reader.ReadSignedInt()
                hide = reader.ReadSignedInt()
                mark_id = reader.ReadSignedInt()
                level = reader.ReadSignedInt()
                max_val = reader.ReadSignedInt()

                max_attri_list: list[int] = []
                if reader.ReadBoolean():
                    max_attri_count = reader.ReadSignedInt()
                    max_attri_list = [
                        reader.ReadSignedInt() for _ in range(max_attri_count)
                    ]

                mintmark_class = reader.ReadSignedInt()

                monster_id_list: list[int] = []
                if reader.ReadBoolean():
                    monster_count = reader.ReadSignedInt()
                    monster_id_list = [
                        reader.ReadSignedInt() for _ in range(monster_count)
                    ]

                move_id_list: list[int] = []
                if reader.ReadBoolean():
                    move_count = reader.ReadSignedInt()
                    move_id_list = [reader.ReadSignedInt() for _ in range(move_count)]

                quality = reader.ReadSignedInt()
                rare = reader.ReadSignedInt()
                rarity = reader.ReadSignedInt()
                total_consume = reader.ReadSignedInt()
                type_val = reader.ReadSignedInt()

                mark_item: MintMarkItem = {
                    'arg': arg_list,
                    'base_attri_value': base_attri_list,
                    'connect': connect,
                    'des': des,
                    'effect_des': effect_des,
                    'extra_attri_value': extra_attri_list,
                    'grade': grade,
                    'hide': hide,
                    'id': mark_id,
                    'level': level,
                    'max': max_val,
                    'max_attri_value': max_attri_list,
                    'mintmark_class': mintmark_class,
                    'monster_id': monster_id_list,
                    'move_id': move_id_list,
                    'quality': quality,
                    'rare': rare,
                    'rarity': rarity,
                    'total_consume': total_consume,
                    'type': type_val,
                }
                result['mint_marks']['mint_mark'].append(mark_item)

        if reader.ReadBoolean():
            class_count = reader.ReadSignedInt()
            for _ in range(class_count):
                class_name = reader.ReadUTFBytesWithLength()
                class_id = reader.ReadSignedInt()

                class_item: MintmarkClassItem = {
                    'class_name': class_name,
                    'id': class_id,
                }
                result['mint_marks']['mintmark_class'].append(class_item)

        return result
