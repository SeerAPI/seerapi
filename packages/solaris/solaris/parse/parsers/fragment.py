"""解析 Fragment.bytes 精灵碎片配置数据文件。"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class FragmentItem(TypedDict):
    """精灵因子配置条目"""

    id: int
    monster_id: int
    move_id: int
    moves_consume: int
    needmon_id: int
    new_se_idx: int
    new_se_consume: int
    pet_consume: int
    pet_limit: int
    rarity: int
    effect_id: int
    show: int


class _FragmentRoot(TypedDict):
    """精灵因子配置容器"""

    fragment: list[FragmentItem]


class FragmentConfig(TypedDict):
    """精灵因子配置数据"""

    root: _FragmentRoot | None


class FragmentParser(BaseParser[FragmentConfig]):
    """Fragment.bytes 配置解析器"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'Fragment.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'fragment.json'

    def parse(self, data: bytes) -> FragmentConfig:
        reader = BytesReader(data)
        result: FragmentConfig = {'root': None}

        if not reader.ReadBoolean():
            return result

        root: _FragmentRoot = {'fragment': []}
        result['root'] = root

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: FragmentItem = {
                'id': reader.ReadSignedInt(),
                'monster_id': reader.ReadSignedInt(),
                'move_id': reader.ReadSignedInt(),
                'moves_consume': reader.ReadSignedInt(),
                'needmon_id': reader.ReadSignedInt(),
                'new_se_idx': reader.ReadSignedInt(),
                'new_se_consume': reader.ReadSignedInt(),
                'pet_consume': reader.ReadSignedInt(),
                'pet_limit': reader.ReadSignedInt(),
                'rarity': reader.ReadSignedInt(),
                'effect_id': reader.ReadSignedInt(),
                'show': reader.ReadSignedInt(),
            }
            root['fragment'].append(item)

        return result
