from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class JackPotShopItem(TypedDict):
    product_name: str
    product_id: list[int]
    batch: int
    endtime: int
    exchange_id: int
    forever: int
    id: int
    opentime: int
    product_price: int
    shopkind: int


class _JackPotShopBlueChipShops(TypedDict):
    bulechip_shop: list[JackPotShopItem]
    endday: str
    endtime: str
    openday: str


class _JackPotShopRoot(TypedDict):
    blue_chip_shops: _JackPotShopBlueChipShops


class JackPotShopConfig(TypedDict):
    root: _JackPotShopRoot


class JackPotShopParser(BaseParser[JackPotShopConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'JackPotShop.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'jackPotShop.json'

    def parse(self, data: bytes) -> JackPotShopConfig:
        reader = BytesReader(data)
        shops: _JackPotShopBlueChipShops = {
            'bulechip_shop': [],
            'endday': '',
            'endtime': '',
            'openday': '',
        }

        if not reader.ReadBoolean():
            return {'root': {'blue_chip_shops': shops}}

        if not reader.ReadBoolean():
            return {'root': {'blue_chip_shops': shops}}

        if reader.ReadBoolean():
            sc = reader.ReadSignedInt()
            for _ in range(sc):
                endtime = reader.ReadSignedInt()
                item_id = reader.ReadSignedInt()
                opentime = reader.ReadSignedInt()
                batch = reader.ReadSignedInt()
                exchange_id = reader.ReadSignedInt()
                forever = reader.ReadSignedInt()
                product_id: list[int] = []
                if reader.ReadBoolean():
                    pid_count = reader.ReadSignedInt()
                    product_id = [reader.ReadSignedInt() for _ in range(pid_count)]
                product_name = reader.ReadUTFBytesWithLength()
                product_price = reader.ReadSignedInt()
                shopkind = reader.ReadSignedInt()
                item: JackPotShopItem = {
                    'product_name': product_name,
                    'product_id': product_id,
                    'batch': batch,
                    'endtime': endtime,
                    'exchange_id': exchange_id,
                    'forever': forever,
                    'id': item_id,
                    'opentime': opentime,
                    'product_price': product_price,
                    'shopkind': shopkind,
                }
                shops['bulechip_shop'].append(item)

        shops['endday'] = reader.ReadUTFBytesWithLength()
        shops['endtime'] = reader.ReadUTFBytesWithLength()
        shops['openday'] = reader.ReadUTFBytesWithLength()

        return {'root': {'blue_chip_shops': shops}}


class JackPotShopTempParser(BaseParser[JackPotShopConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'JackPotShop_temp.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'jackPotShopTemp.json'

    def parse(self, data: bytes) -> JackPotShopConfig:
        reader = BytesReader(data)
        shops: _JackPotShopBlueChipShops = {
            'bulechip_shop': [],
            'endday': '',
            'endtime': '',
            'openday': '',
        }

        if not reader.ReadBoolean():
            return {'root': {'blue_chip_shops': shops}}

        if not reader.ReadBoolean():
            return {'root': {'blue_chip_shops': shops}}

        if reader.ReadBoolean():
            sc = reader.ReadSignedInt()
            for _ in range(sc):
                endtime = reader.ReadSignedInt()
                item_id = reader.ReadSignedInt()
                opentime = reader.ReadSignedInt()
                batch = reader.ReadSignedInt()
                exchange_id = reader.ReadSignedInt()
                forever = reader.ReadSignedInt()
                product_id: list[int] = []
                if reader.ReadBoolean():
                    pid_count = reader.ReadSignedInt()
                    product_id = [reader.ReadSignedInt() for _ in range(pid_count)]
                product_name = reader.ReadUTFBytesWithLength()
                product_price = reader.ReadSignedInt()
                shopkind = reader.ReadSignedInt()
                item: JackPotShopItem = {
                    'product_name': product_name,
                    'product_id': product_id,
                    'batch': batch,
                    'endtime': endtime,
                    'exchange_id': exchange_id,
                    'forever': forever,
                    'id': item_id,
                    'opentime': opentime,
                    'product_price': product_price,
                    'shopkind': shopkind,
                }
                shops['bulechip_shop'].append(item)

        shops['endday'] = reader.ReadUTFBytesWithLength()
        shops['endtime'] = reader.ReadUTFBytesWithLength()
        shops['openday'] = reader.ReadUTFBytesWithLength()

        return {'root': {'blue_chip_shops': shops}}
