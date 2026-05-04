from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ShopGiftItem(TypedDict):
    atlas: str
    background: str
    icon: str
    name: str
    discountprice: list[int]
    price: list[int]
    reward: list[int]
    discount: int
    id: int
    miditem: int
    number: int
    prop: int
    quota: int
    show: int
    sort: int
    type: int


class _ShopGiftData(TypedDict):
    item: list[ShopGiftItem]


class ShopGiftParser(BaseParser[_ShopGiftData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'shop_gift.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'shopGift.json'

    def parse(self, data: bytes) -> _ShopGiftData:
        reader = BytesReader(data)
        result: _ShopGiftData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ShopGiftItem = {
                'atlas': reader.ReadUTFBytesWithLength(),
                'background': reader.ReadUTFBytesWithLength(),
                'discount': reader.ReadSignedInt(),
                'discountprice': [],
                'icon': '',
                'id': 0,
                'miditem': 0,
                'name': '',
                'number': 0,
                'price': [],
                'prop': 0,
                'quota': 0,
                'reward': [],
                'show': 0,
                'sort': 0,
                'type': 0,
            }
            if reader.ReadBoolean():
                dp_count = reader.ReadSignedInt()
                item['discountprice'] = [
                    reader.ReadSignedInt() for _ in range(dp_count)
                ]
            item['icon'] = reader.ReadUTFBytesWithLength()
            item['id'] = reader.ReadSignedInt()
            item['miditem'] = reader.ReadSignedInt()
            item['name'] = reader.ReadUTFBytesWithLength()
            item['number'] = reader.ReadSignedInt()
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
