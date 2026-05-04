from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ShopCultivateItem(TypedDict):
    name: str
    price: list[int]
    reward: list[int]
    id: int
    miditem: int
    number: int
    prop: int
    quota: int
    show: int
    sort: int
    type: int


class _ShopCultivateData(TypedDict):
    item: list[ShopCultivateItem]


class ShopCultivateParser(BaseParser[_ShopCultivateData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'shop_cultivate.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'shopCultivate.json'

    def parse(self, data: bytes) -> _ShopCultivateData:
        reader = BytesReader(data)
        result: _ShopCultivateData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ShopCultivateItem = {
                'id': reader.ReadSignedInt(),
                'miditem': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
                'number': reader.ReadSignedInt(),
                'price': [],
                'prop': 0,
                'quota': 0,
                'reward': [],
                'show': 0,
                'sort': 0,
                'type': 0,
            }
            if reader.ReadBoolean():
                price_count = reader.ReadSignedInt()
                item['price'] = [reader.ReadSignedInt() for _ in range(price_count)]
            item['prop'] = reader.ReadSignedInt()
            item['quota'] = reader.ReadSignedInt()
            if reader.ReadBoolean():
                reward_count = reader.ReadSignedInt()
                item['reward'] = [reader.ReadSignedInt() for _ in range(reward_count)]
            item['show'] = reader.ReadSignedInt()
            item['sort'] = reader.ReadSignedInt()
            item['type'] = reader.ReadSignedInt()
            result['item'].append(item)

        return result
