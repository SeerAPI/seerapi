from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ShopAttireItem(TypedDict):
    name: str
    miditem: list[int]
    price: list[int]
    prop: list[int]
    reward: list[int]
    vipprice: list[int]
    id: int
    label: int
    recommend: int
    show: int
    sort: int
    suit: int
    type: int
    vip: int


class _ShopAttireData(TypedDict):
    item: list[ShopAttireItem]


class ShopAttireParser(BaseParser[_ShopAttireData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'shop_attire.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'shopAttire.json'

    def parse(self, data: bytes) -> _ShopAttireData:
        reader = BytesReader(data)
        result: _ShopAttireData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ShopAttireItem = {
                'id': reader.ReadSignedInt(),
                'label': reader.ReadSignedInt(),
                'miditem': [],
                'name': '',
                'price': [],
                'prop': [],
                'recommend': 0,
                'reward': [],
                'show': 0,
                'sort': 0,
                'suit': 0,
                'type': 0,
                'vip': 0,
                'vipprice': [],
            }
            if reader.ReadBoolean():
                miditem_count = reader.ReadSignedInt()
                item['miditem'] = [reader.ReadSignedInt() for _ in range(miditem_count)]
            item['name'] = reader.ReadUTFBytesWithLength()
            if reader.ReadBoolean():
                price_count = reader.ReadSignedInt()
                item['price'] = [reader.ReadSignedInt() for _ in range(price_count)]
            if reader.ReadBoolean():
                prop_count = reader.ReadSignedInt()
                item['prop'] = [reader.ReadSignedInt() for _ in range(prop_count)]
            item['recommend'] = reader.ReadSignedInt()
            if reader.ReadBoolean():
                reward_count = reader.ReadSignedInt()
                item['reward'] = [reader.ReadSignedInt() for _ in range(reward_count)]
            item['show'] = reader.ReadSignedInt()
            item['sort'] = reader.ReadSignedInt()
            item['suit'] = reader.ReadSignedInt()
            item['type'] = reader.ReadSignedInt()
            item['vip'] = reader.ReadSignedInt()
            if reader.ReadBoolean():
                vipprice_count = reader.ReadSignedInt()
                item['vipprice'] = [
                    reader.ReadSignedInt() for _ in range(vipprice_count)
                ]
            result['item'].append(item)

        return result
