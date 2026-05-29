from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ActivityShopConfigInfo(TypedDict):
    activityid: int
    commodity: str
    consumeitemid: int
    exchangeID: int
    id: int
    limit: int
    price: int
    quantity: int
    shoptype: str
    sort: int
    timeend: int
    timelimit: int
    timestart: int
    userinfo: int


class _ActivityShopConfigData(TypedDict):
    item: list[ActivityShopConfigInfo]


class ActivityShopConfigParser(BaseParser[_ActivityShopConfigData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'Activity_ShopConfig.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'Activity_ShopConfig.json'

    def parse(self, data: bytes) -> _ActivityShopConfigData:
        reader = BytesReader(data)
        result: _ActivityShopConfigData = {'item': []}
        if not reader.ReadBoolean():
            return result
        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ActivityShopConfigInfo = {
                'activityid': reader.ReadSignedInt(),
                'commodity': reader.ReadUTFBytesWithLength(),
                'consumeitemid': reader.ReadSignedInt(),
                'exchangeID': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'limit': reader.ReadSignedInt(),
                'price': reader.ReadSignedInt(),
                'quantity': reader.ReadSignedInt(),
                'shoptype': reader.ReadUTFBytesWithLength(),
                'sort': reader.ReadSignedInt(),
                'timeend': reader.ReadSignedInt(),
                'timelimit': reader.ReadSignedInt(),
                'timestart': reader.ReadSignedInt(),
                'userinfo': reader.ReadSignedInt(),
            }
            result['item'].append(item)
        return result
