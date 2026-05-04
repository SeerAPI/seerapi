from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PurchaseBonusShopItem(TypedDict):
    commodity: list[int]
    consumeitemid: int
    id: int
    limit: int
    price: int
    quantity: int
    shoptype: int
    stat: int
    userinfo: int


class _PurchaseBonusShopData(TypedDict):
    item: list[PurchaseBonusShopItem]


class PurchaseBonusShopParser(BaseParser[_PurchaseBonusShopData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'purchaseBonus_shop.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'purchaseBonusShop.json'

    def parse(self, data: bytes) -> _PurchaseBonusShopData:
        reader = BytesReader(data)
        result: _PurchaseBonusShopData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: PurchaseBonusShopItem = {
                'commodity': [],
                'consumeitemid': 0,
                'id': 0,
                'limit': 0,
                'price': 0,
                'quantity': 0,
                'shoptype': 0,
                'stat': 0,
                'userinfo': 0,
            }
            if reader.ReadBoolean():
                c_count = reader.ReadSignedInt()
                item['commodity'] = [reader.ReadSignedInt() for _ in range(c_count)]
            item['consumeitemid'] = reader.ReadSignedInt()
            item['id'] = reader.ReadSignedInt()
            item['limit'] = reader.ReadSignedInt()
            item['price'] = reader.ReadSignedInt()
            item['quantity'] = reader.ReadSignedInt()
            item['shoptype'] = reader.ReadSignedInt()
            item['stat'] = reader.ReadSignedInt()
            item['userinfo'] = reader.ReadSignedInt()
            result['item'].append(item)

        return result
