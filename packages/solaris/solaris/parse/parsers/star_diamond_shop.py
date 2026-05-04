from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class StarDiamondShopItem(TypedDict):
    icon: str
    name: str
    reward: str
    commodity: int
    currency: int
    grade: int
    id: int
    limit: int
    mintmark_id: int
    new_se_id: int
    price: int
    type: int


class _StarDiamondShopData(TypedDict):
    item: list[StarDiamondShopItem]


class StarDiamondShopParser(BaseParser[_StarDiamondShopData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'StarDiamondShop.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'starDiamondShop.json'

    def parse(self, data: bytes) -> _StarDiamondShopData:
        reader = BytesReader(data)
        result: _StarDiamondShopData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: StarDiamondShopItem = {
                'mintmark_id': reader.ReadSignedInt(),
                'new_se_id': reader.ReadSignedInt(),
                'commodity': reader.ReadSignedInt(),
                'currency': reader.ReadSignedInt(),
                'grade': reader.ReadSignedInt(),
                'icon': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'limit': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
                'price': reader.ReadSignedInt(),
                'reward': reader.ReadUTFBytesWithLength(),
                'type': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
