from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ItemItem(TypedDict):
    """称号背景项"""

    finish_time: str
    go: str
    id: int
    image_id: int
    introduction: str
    is_obtain: int
    name: str


class _Root(TypedDict):
    """根数据结构"""

    item: list[ItemItem]


class TitleBgConfig(TypedDict):
    """称号背景配置"""

    root: _Root


class TitleBgParser(BaseParser[TitleBgConfig]):
    """称号背景解析器"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'TitleBg.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'titleBg.json'

    def parse(self, data: bytes) -> TitleBgConfig:
        reader = BytesReader(data)
        result: TitleBgConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            finish_time = reader.ReadUTFBytesWithLength()
            go = reader.ReadUTFBytesWithLength()
            item_id = reader.ReadSignedInt()
            image_id = reader.ReadSignedInt()
            introduction = reader.ReadUTFBytesWithLength()
            is_obtain = reader.ReadSignedInt()
            name = reader.ReadUTFBytesWithLength()

            item: ItemItem = {
                'finish_time': finish_time,
                'go': go,
                'id': item_id,
                'image_id': image_id,
                'introduction': introduction,
                'is_obtain': is_obtain,
                'name': name,
            }
            result['root']['item'].append(item)

        return result
