from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ShopElfItem(TypedDict):
    name: str
    reward: str
    discountprice: list[int]
    gift: list[int]
    price: list[int]
    discount: int
    id: int
    miditem: int
    prop: int
    quota: int
    recommend: int
    show: int
    sort: int
    type: int


class _ShopElfData(TypedDict):
    item: list[ShopElfItem]


class ShopElfParser(BaseParser[_ShopElfData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'shop_elf.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'shopElf.json'

    def parse(self, data: bytes) -> _ShopElfData:
        reader = BytesReader(data)
        result: _ShopElfData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ShopElfItem = {
                'discount': reader.ReadSignedInt(),
                'discountprice': [],
                'gift': [],
                'id': 0,
                'miditem': 0,
                'name': '',
                'price': [],
                'prop': 0,
                'quota': 0,
                'recommend': 0,
                'reward': '',
                'show': 0,
                'sort': 0,
                'type': 0,
            }
            if reader.ReadBoolean():
                dp_count = reader.ReadSignedInt()
                item['discountprice'] = [
                    reader.ReadSignedInt() for _ in range(dp_count)
                ]
            if reader.ReadBoolean():
                gift_count = reader.ReadSignedInt()
                item['gift'] = [reader.ReadSignedInt() for _ in range(gift_count)]
            item['id'] = reader.ReadSignedInt()
            item['miditem'] = reader.ReadSignedInt()
            item['name'] = reader.ReadUTFBytesWithLength()
            if reader.ReadBoolean():
                price_count = reader.ReadSignedInt()
                item['price'] = [reader.ReadSignedInt() for _ in range(price_count)]
            item['prop'] = reader.ReadSignedInt()
            item['quota'] = reader.ReadSignedInt()
            item['recommend'] = reader.ReadSignedInt()
            item['reward'] = reader.ReadUTFBytesWithLength()
            item['show'] = reader.ReadSignedInt()
            item['sort'] = reader.ReadSignedInt()
            item['type'] = reader.ReadSignedInt()
            result['item'].append(item)

        return result
