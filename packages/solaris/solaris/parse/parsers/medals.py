from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class MedalItem(TypedDict):
    """勋章项"""

    achievepoint: int
    award: int
    hide: int
    id: int
    title: str


class _Medals(TypedDict):
    """勋章容器"""

    medal: list[MedalItem]


class MedalsConfig(TypedDict):
    """勋章配置"""

    medals: _Medals


class MedalsParser(BaseParser[MedalsConfig]):
    """勋章解析器"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'medals.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'medals.json'

    def parse(self, data: bytes) -> MedalsConfig:
        reader = BytesReader(data)
        result: MedalsConfig = {'medals': {'medal': []}}

        if not reader.ReadBoolean():
            return result

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            achievepoint = reader.ReadSignedInt()
            award = reader.ReadSignedInt()
            hide = reader.ReadSignedInt()
            medal_id = reader.ReadSignedInt()
            title = reader.ReadUTFBytesWithLength()

            medal_item: MedalItem = {
                'achievepoint': achievepoint,
                'award': award,
                'hide': hide,
                'id': medal_id,
                'title': title,
            }
            result['medals']['medal'].append(medal_item)

        return result
