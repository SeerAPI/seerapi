from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class DiamonBoxItem(TypedDict):
    rewardcnt: str
    rewardid: str
    rewardpr: str
    rewardtype: str
    activitynum: int
    exchangecut: int
    id: int


class _DiamonBoxData(TypedDict):
    item: list[DiamonBoxItem]


class DiamonBoxParser(BaseParser[_DiamonBoxData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'diamon_box.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'diamonBox.json'

    def parse(self, data: bytes) -> _DiamonBoxData:
        reader = BytesReader(data)
        result: _DiamonBoxData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: DiamonBoxItem = {
                'activitynum': reader.ReadSignedInt(),
                'exchangecut': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'rewardcnt': reader.ReadUTFBytesWithLength(),
                'rewardid': reader.ReadUTFBytesWithLength(),
                'rewardpr': reader.ReadUTFBytesWithLength(),
                'rewardtype': reader.ReadUTFBytesWithLength(),
            }
            result['item'].append(item)

        return result
