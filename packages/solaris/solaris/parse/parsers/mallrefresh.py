from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class MallrefreshItem(TypedDict):
    price: list[int]
    rewardinfo: list[int]
    id: int


class _MallrefreshData(TypedDict):
    item: list[MallrefreshItem]


class MallrefreshParser(BaseParser[_MallrefreshData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'mallrefresh.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'mallrefresh.json'

    def parse(self, data: bytes) -> _MallrefreshData:
        reader = BytesReader(data)
        result: _MallrefreshData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: MallrefreshItem = {
                'id': reader.ReadSignedInt(),
                'price': [],
                'rewardinfo': [],
            }
            if reader.ReadBoolean():
                p_count = reader.ReadSignedInt()
                item['price'] = [reader.ReadSignedInt() for _ in range(p_count)]
            if reader.ReadBoolean():
                ri_count = reader.ReadSignedInt()
                item['rewardinfo'] = [reader.ReadSignedInt() for _ in range(ri_count)]
            result['item'].append(item)

        return result
