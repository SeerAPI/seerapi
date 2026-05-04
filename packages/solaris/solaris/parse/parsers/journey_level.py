from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ItemItem(TypedDict):
    """旅途等级项"""

    id: int
    level: int
    rewardcnt: str
    rewardid: str
    rewardtype: str
    taskid: str


class _Root(TypedDict):
    """根数据结构"""

    item: list[ItemItem]


class JourneyLevelConfig(TypedDict):
    """旅途等级配置"""

    root: _Root


class JourneyLevelParser(BaseParser[JourneyLevelConfig]):
    """旅途等级解析器"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'journey_level.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'journeyLevel.json'

    def parse(self, data: bytes) -> JourneyLevelConfig:
        reader = BytesReader(data)
        result: JourneyLevelConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item_id = reader.ReadSignedInt()
            level = reader.ReadSignedInt()
            rewardcnt = reader.ReadUTFBytesWithLength()
            rewardid = reader.ReadUTFBytesWithLength()
            rewardtype = reader.ReadUTFBytesWithLength()
            taskid = reader.ReadUTFBytesWithLength()

            item: ItemItem = {
                'id': item_id,
                'level': level,
                'rewardcnt': rewardcnt,
                'rewardid': rewardid,
                'rewardtype': rewardtype,
                'taskid': taskid,
            }
            result['root']['item'].append(item)

        return result
