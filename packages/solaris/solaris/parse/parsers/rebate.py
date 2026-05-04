from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class RebateItem(TypedDict):
    rewardinfo: list[int]
    id: int
    title: int
    type: int


class _RebateData(TypedDict):
    item: list[RebateItem]


class RebateParser(BaseParser[_RebateData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'rebate.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'rebate.json'

    def parse(self, data: bytes) -> _RebateData:
        reader = BytesReader(data)
        result: _RebateData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: RebateItem = {
                'id': reader.ReadSignedInt(),
                'rewardinfo': [],
                'title': 0,
                'type': 0,
            }
            if reader.ReadBoolean():
                ri_count = reader.ReadSignedInt()
                item['rewardinfo'] = [reader.ReadSignedInt() for _ in range(ri_count)]
            item['title'] = reader.ReadSignedInt()
            item['type'] = reader.ReadSignedInt()
            result['item'].append(item)

        return result
