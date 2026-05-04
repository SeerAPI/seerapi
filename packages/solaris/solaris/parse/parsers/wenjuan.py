from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ItemItem(TypedDict):
    """问卷选项项"""

    a: str
    dir: int
    wb: int


class WjItem(TypedDict):
    """问卷题目项"""

    id: int
    item: list[ItemItem]
    q: str
    skip: int
    statlog: str
    type: int


class _Wjmain(TypedDict):
    """问卷主体容器"""

    wj: list[WjItem]


class Detail(TypedDict):
    """问卷详情"""

    desc: str
    reward: str


class _Root(TypedDict):
    """根数据结构"""

    detail: Detail | None
    wjmain: _Wjmain | None


class WenjuanConfig(TypedDict):
    """问卷配置"""

    root: _Root


class WenjuanParser(BaseParser[WenjuanConfig]):
    """问卷解析器"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'wenjuan.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'wenjuan.json'

    def parse(self, data: bytes) -> WenjuanConfig:
        reader = BytesReader(data)
        result: WenjuanConfig = {'root': {'detail': None, 'wjmain': None}}

        if not reader.ReadBoolean():
            return result

        detail: Detail | None = None
        if reader.ReadBoolean():
            desc = reader.ReadUTFBytesWithLength()
            reward = reader.ReadUTFBytesWithLength()
            detail = {'desc': desc, 'reward': reward}
        result['root']['detail'] = detail

        wjmain: _Wjmain | None = None
        if reader.ReadBoolean():
            wj_list: list[WjItem] = []
            if reader.ReadBoolean():
                count = reader.ReadSignedInt()
                for _ in range(count):
                    wj_id = reader.ReadSignedInt()
                    item_list: list[ItemItem] = []
                    if reader.ReadBoolean():
                        item_count = reader.ReadSignedInt()
                        for _ in range(item_count):
                            a = reader.ReadUTFBytesWithLength()
                            dir_val = reader.ReadSignedInt()
                            wb = reader.ReadSignedInt()

                            item: ItemItem = {
                                'a': a,
                                'dir': dir_val,
                                'wb': wb,
                            }
                            item_list.append(item)

                    q = reader.ReadUTFBytesWithLength()
                    skip = reader.ReadSignedInt()
                    statlog = reader.ReadUTFBytesWithLength()
                    type_val = reader.ReadSignedInt()

                    wj_item: WjItem = {
                        'id': wj_id,
                        'item': item_list,
                        'q': q,
                        'skip': skip,
                        'statlog': statlog,
                        'type': type_val,
                    }
                    wj_list.append(wj_item)

            wjmain = {'wj': wj_list}
        result['root']['wjmain'] = wjmain

        return result
