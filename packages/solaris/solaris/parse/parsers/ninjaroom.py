from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class NinbouItem(TypedDict):
    """忍法帖项"""

    new_stat_log: str
    boss: int
    exp: int
    grade: int
    id: int
    lv: int
    output: int
    rewardcnt: str
    rewardid: str
    rewardtype: str
    sebossid: int
    times: int
    type: int


class _Ninbous(TypedDict):
    """忍法帖容器"""

    ninbou: list[NinbouItem]


class NinjaItem(TypedDict):
    """忍者项"""

    new_stat_log: int
    creat: int
    id: int
    lv: str
    rank: int
    rewardcnt: str
    rewardid: str
    rewardtype: str
    show: str


class _Ninjas(TypedDict):
    """忍者容器"""

    ninja: list[NinjaItem]


class _Root(TypedDict):
    """根数据结构"""

    ninbous: _Ninbous | None
    ninjas: _Ninjas | None


class NinjaroomConfig(TypedDict):
    """忍者房间配置"""

    root: _Root


class NinjaroomParser(BaseParser[NinjaroomConfig]):
    """忍者房间解析器"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'ninjaroom.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'ninjaroom.json'

    def parse(self, data: bytes) -> NinjaroomConfig:
        reader = BytesReader(data)
        result: NinjaroomConfig = {'root': {'ninbous': None, 'ninjas': None}}

        if not reader.ReadBoolean():
            return result

        ninbous: _Ninbous | None = None
        if reader.ReadBoolean():
            ninbou_list: list[NinbouItem] = []
            if reader.ReadBoolean():
                count = reader.ReadSignedInt()
                for _ in range(count):
                    new_stat_log = reader.ReadUTFBytesWithLength()
                    boss = reader.ReadSignedInt()
                    exp = reader.ReadSignedInt()
                    grade = reader.ReadSignedInt()
                    ninbou_id = reader.ReadSignedInt()
                    lv = reader.ReadSignedInt()
                    output = reader.ReadSignedInt()
                    rewardcnt = reader.ReadUTFBytesWithLength()
                    rewardid = reader.ReadUTFBytesWithLength()
                    rewardtype = reader.ReadUTFBytesWithLength()
                    sebossid = reader.ReadSignedInt()
                    times = reader.ReadSignedInt()
                    type_val = reader.ReadSignedInt()

                    ninbou_item: NinbouItem = {
                        'new_stat_log': new_stat_log,
                        'boss': boss,
                        'exp': exp,
                        'grade': grade,
                        'id': ninbou_id,
                        'lv': lv,
                        'output': output,
                        'rewardcnt': rewardcnt,
                        'rewardid': rewardid,
                        'rewardtype': rewardtype,
                        'sebossid': sebossid,
                        'times': times,
                        'type': type_val,
                    }
                    ninbou_list.append(ninbou_item)

            ninbous = {'ninbou': ninbou_list}
        result['root']['ninbous'] = ninbous

        ninjas: _Ninjas | None = None
        if reader.ReadBoolean():
            ninja_list: list[NinjaItem] = []
            if reader.ReadBoolean():
                count = reader.ReadSignedInt()
                for _ in range(count):
                    new_stat_log = reader.ReadSignedInt()
                    creat = reader.ReadSignedInt()
                    ninja_id = reader.ReadSignedInt()
                    lv = reader.ReadUTFBytesWithLength()
                    rank = reader.ReadSignedInt()
                    rewardcnt = reader.ReadUTFBytesWithLength()
                    rewardid = reader.ReadUTFBytesWithLength()
                    rewardtype = reader.ReadUTFBytesWithLength()
                    show = reader.ReadUTFBytesWithLength()

                    ninja_item: NinjaItem = {
                        'new_stat_log': new_stat_log,
                        'creat': creat,
                        'id': ninja_id,
                        'lv': lv,
                        'rank': rank,
                        'rewardcnt': rewardcnt,
                        'rewardid': rewardid,
                        'rewardtype': rewardtype,
                        'show': show,
                    }
                    ninja_list.append(ninja_item)

            ninjas = {'ninja': ninja_list}
        result['root']['ninjas'] = ninjas

        return result
