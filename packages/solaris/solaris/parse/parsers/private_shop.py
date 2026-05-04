from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PrivateShopItem(TypedDict):
    content: str
    title: str
    bytepos: int
    cost_num: int
    cost_type: int
    id: int
    limit_num: int
    limit_type: int
    origin_price: int
    product_id: int
    type: int
    userinfo: int


class _PrivateShopData(TypedDict):
    item: list[PrivateShopItem]


class PrivateShopParser(BaseParser[_PrivateShopData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'privateShop.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'privateShop.json'

    def parse(self, data: bytes) -> _PrivateShopData:
        reader = BytesReader(data)
        result: _PrivateShopData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: PrivateShopItem = {
                'bytepos': reader.ReadSignedInt(),
                'content': reader.ReadUTFBytesWithLength(),
                'cost_num': reader.ReadSignedInt(),
                'cost_type': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'limit_num': reader.ReadSignedInt(),
                'limit_type': reader.ReadSignedInt(),
                'origin_price': reader.ReadSignedInt(),
                'product_id': reader.ReadSignedInt(),
                'title': reader.ReadUTFBytesWithLength(),
                'type': reader.ReadSignedInt(),
                'userinfo': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result


class PrivateSignItem(TypedDict):
    intro: str
    name: str
    reward: list[int]
    reward_pet: list[int]
    day: int
    id: int
    pet_id: int


class _PrivateSignData(TypedDict):
    item: list[PrivateSignItem]


class PrivateSignParser(BaseParser[_PrivateSignData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'privateSign.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'privateSign.json'

    def parse(self, data: bytes) -> _PrivateSignData:
        reader = BytesReader(data)
        result: _PrivateSignData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: PrivateSignItem = {
                'day': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'intro': reader.ReadUTFBytesWithLength(),
                'name': reader.ReadUTFBytesWithLength(),
                'pet_id': reader.ReadSignedInt(),
                'reward': [],
                'reward_pet': [],
            }
            if reader.ReadBoolean():
                r_count = reader.ReadSignedInt()
                item['reward'] = [reader.ReadSignedInt() for _ in range(r_count)]
            if reader.ReadBoolean():
                rp_count = reader.ReadSignedInt()
                item['reward_pet'] = [reader.ReadSignedInt() for _ in range(rp_count)]
            result['item'].append(item)

        return result


class PrivateCostDiamondRewardItem(TypedDict):
    reward: str
    id: int
    step: int


class _PrivateCostDiamondRewardData(TypedDict):
    item: list[PrivateCostDiamondRewardItem]


class PrivateCostDiamondRewardParser(BaseParser[_PrivateCostDiamondRewardData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'privateCostDiamondReward.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'privateCostDiamondReward.json'

    def parse(self, data: bytes) -> _PrivateCostDiamondRewardData:
        reader = BytesReader(data)
        result: _PrivateCostDiamondRewardData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: PrivateCostDiamondRewardItem = {
                'id': reader.ReadSignedInt(),
                'reward': reader.ReadUTFBytesWithLength(),
                'step': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
