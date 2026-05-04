from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ExpTowerItem(TypedDict):
    bosslist: str
    raidunlocktext: str
    rewardid: str
    rewardnum: str
    rewardtype: str
    sebossid: str
    id: int
    raidunlockarg: int


class _ExpTowerData(TypedDict):
    item: list[ExpTowerItem]


class ExpTowerParser(BaseParser[_ExpTowerData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'exp_tower.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'expTower.json'

    def parse(self, data: bytes) -> _ExpTowerData:
        reader = BytesReader(data)
        result: _ExpTowerData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ExpTowerItem = {
                'bosslist': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'raidunlockarg': reader.ReadSignedInt(),
                'raidunlocktext': reader.ReadUTFBytesWithLength(),
                'rewardid': reader.ReadUTFBytesWithLength(),
                'rewardnum': reader.ReadUTFBytesWithLength(),
                'rewardtype': reader.ReadUTFBytesWithLength(),
                'sebossid': reader.ReadUTFBytesWithLength(),
            }
            result['item'].append(item)

        return result
