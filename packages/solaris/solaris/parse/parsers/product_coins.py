from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ProductCoinsItem(TypedDict):
    item_id: str
    name: str
    coins: int
    limit: int
    price: int
    product_id: int
    product_type: int
    times: int
    type: int
    vip: int


class _ProductCoinsRoot(TypedDict):
    item: list[ProductCoinsItem]


class ProductCoinsConfig(TypedDict):
    root: _ProductCoinsRoot


class ProductCoinsParser(BaseParser[ProductCoinsConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'product_coins.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'productCoins.json'

    def parse(self, data: bytes) -> ProductCoinsConfig:
        reader = BytesReader(data)
        result: ProductCoinsConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        if reader.ReadBoolean():
            count = reader.ReadSignedInt()
            for _ in range(count):
                item: ProductCoinsItem = {
                    'coins': reader.ReadSignedInt(),
                    'item_id': reader.ReadUTFBytesWithLength(),
                    'limit': reader.ReadSignedInt(),
                    'name': reader.ReadUTFBytesWithLength(),
                    'price': reader.ReadSignedInt(),
                    'product_id': reader.ReadSignedInt(),
                    'product_type': reader.ReadSignedInt(),
                    'times': reader.ReadSignedInt(),
                    'type': reader.ReadSignedInt(),
                    'vip': reader.ReadSignedInt(),
                }
                result['root']['item'].append(item)

        return result
