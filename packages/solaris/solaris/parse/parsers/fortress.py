from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class FortressBOSSItem(TypedDict):
    boss_info: str
    fortress_name: str
    damage_to_hp: list[int]
    boss: int
    fortress_hp: int
    id: int
    layer: int
    pet_id: int


class _FortressBOSSData(TypedDict):
    item: list[FortressBOSSItem]


class FortressBOSSParser(BaseParser[_FortressBOSSData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'fortressBOSS.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'fortressBOSS.json'

    def parse(self, data: bytes) -> _FortressBOSSData:
        reader = BytesReader(data)
        result: _FortressBOSSData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            boss = reader.ReadSignedInt()
            boss_info = reader.ReadUTFBytesWithLength()
            damage_to_hp: list[int] = []
            if reader.ReadBoolean():
                dc = reader.ReadSignedInt()
                damage_to_hp = [reader.ReadSignedInt() for _ in range(dc)]
            fortress_hp = reader.ReadSignedInt()
            fortress_name = reader.ReadUTFBytesWithLength()
            item_id = reader.ReadSignedInt()
            layer = reader.ReadSignedInt()
            pet_id = reader.ReadSignedInt()
            item: FortressBOSSItem = {
                'boss_info': boss_info,
                'fortress_name': fortress_name,
                'damage_to_hp': damage_to_hp,
                'boss': boss,
                'fortress_hp': fortress_hp,
                'id': item_id,
                'layer': layer,
                'pet_id': pet_id,
            }
            result['item'].append(item)

        return result


class FortressRewardItem(TypedDict):
    reward: list[int]
    end_rank: int
    id: int
    start_rank: int
    type: int


class _FortressRewardData(TypedDict):
    item: list[FortressRewardItem]


class FortressRewardParser(BaseParser[_FortressRewardData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'fortressReward.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'fortressReward.json'

    def parse(self, data: bytes) -> _FortressRewardData:
        reader = BytesReader(data)
        result: _FortressRewardData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            end_rank = reader.ReadSignedInt()
            item_id = reader.ReadSignedInt()
            reward: list[int] = []
            if reader.ReadBoolean():
                rc = reader.ReadSignedInt()
                reward = [reader.ReadSignedInt() for _ in range(rc)]
            start_rank = reader.ReadSignedInt()
            _type = reader.ReadSignedInt()
            item: FortressRewardItem = {
                'reward': reward,
                'end_rank': end_rank,
                'id': item_id,
                'start_rank': start_rank,
                'type': _type,
            }
            result['item'].append(item)

        return result
