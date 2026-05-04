from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AchievementbonusItem(TypedDict):
    rewardcnt: str
    rewardid: str
    branch: int
    id: int
    rewardtype: int
    rule: int


class _AchievementbonusData(TypedDict):
    item: list[AchievementbonusItem]


class AchievementbonusParser(BaseParser[_AchievementbonusData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'achievementbonus.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'achievementbonus.json'

    def parse(self, data: bytes) -> _AchievementbonusData:
        reader = BytesReader(data)
        result: _AchievementbonusData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: AchievementbonusItem = {
                'branch': reader.ReadSignedInt(),
                'rule': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'rewardcnt': reader.ReadUTFBytesWithLength(),
                'rewardid': reader.ReadUTFBytesWithLength(),
                'rewardtype': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
