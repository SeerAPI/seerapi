from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ItemItem(TypedDict):
    """任务内容项"""

    dbquery: int
    taskparam1: int
    taskparam2: int
    tasktype: int
    content: str
    gopanel: str
    helptips: str
    icon: str
    id: int
    rewardcnt: str
    rewardid: str
    rewardtype: str
    taskschedule: int
    timelimited: str
    tipstime: int


class _Root(TypedDict):
    """根数据结构"""

    item: list[ItemItem]


class JourneyContentConfig(TypedDict):
    """旅途内容配置"""

    root: _Root


class JourneyContentParser(BaseParser[JourneyContentConfig]):
    """旅途内容解析器"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'journey_content.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'journeyContent.json'

    def parse(self, data: bytes) -> JourneyContentConfig:
        reader = BytesReader(data)
        result: JourneyContentConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            dbquery = reader.ReadSignedInt()
            taskparam1 = reader.ReadSignedInt()
            taskparam2 = reader.ReadSignedInt()
            tasktype = reader.ReadSignedInt()
            content = reader.ReadUTFBytesWithLength()
            gopanel = reader.ReadUTFBytesWithLength()
            helptips = reader.ReadUTFBytesWithLength()
            icon = reader.ReadUTFBytesWithLength()
            item_id = reader.ReadSignedInt()
            rewardcnt = reader.ReadUTFBytesWithLength()
            rewardid = reader.ReadUTFBytesWithLength()
            rewardtype = reader.ReadUTFBytesWithLength()
            taskschedule = reader.ReadSignedInt()
            timelimited = reader.ReadUTFBytesWithLength()
            tipstime = reader.ReadSignedInt()

            item: ItemItem = {
                'dbquery': dbquery,
                'taskparam1': taskparam1,
                'taskparam2': taskparam2,
                'tasktype': tasktype,
                'content': content,
                'gopanel': gopanel,
                'helptips': helptips,
                'icon': icon,
                'id': item_id,
                'rewardcnt': rewardcnt,
                'rewardid': rewardid,
                'rewardtype': rewardtype,
                'taskschedule': taskschedule,
                'timelimited': timelimited,
                'tipstime': tipstime,
            }
            result['root']['item'].append(item)

        return result
