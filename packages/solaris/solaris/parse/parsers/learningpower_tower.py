from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _Item(TypedDict):
    boss_list: str
    id: int
    raid_unlock_arg: int
    raid_unlock_text: str
    reward_id: str
    reward_num: str
    reward_type: str
    se_boss_id: str


class _Data(TypedDict):
    data: list[_Item]


class LearningpowerTowerParser(BaseParser[_Data]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'learningpower_tower.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'learningpowerTower.json'

    def parse(self, data: bytes) -> _Data:
        reader = BytesReader(data)
        result: _Data = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: _Item = {
                'boss_list': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'raid_unlock_arg': reader.ReadSignedInt(),
                'raid_unlock_text': reader.ReadUTFBytesWithLength(),
                'reward_id': reader.ReadUTFBytesWithLength(),
                'reward_num': reader.ReadUTFBytesWithLength(),
                'reward_type': reader.ReadUTFBytesWithLength(),
                'se_boss_id': reader.ReadUTFBytesWithLength(),
            }
            result['data'].append(item)

        return result
