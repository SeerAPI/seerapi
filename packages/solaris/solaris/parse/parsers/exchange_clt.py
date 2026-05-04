from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ExchangeCltItem(TypedDict):
    monappend: str
    batch: int
    bitset_id: int
    boundmonster: int
    coinid: int
    cointype: int
    count: int
    id: int
    isjustone: int
    limit_cnt: int
    limittype: int
    popid: int
    price: int
    realid: int
    shopid: int
    subtag: int
    top: int
    type: int
    user_info_bit_pos: int
    user_info_id: int


class _ExchangeCltData(TypedDict):
    item: list[ExchangeCltItem]


class ExchangeCltParser(BaseParser[_ExchangeCltData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'exchange_clt.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'exchangeClt.json'

    def parse(self, data: bytes) -> _ExchangeCltData:
        reader = BytesReader(data)
        result: _ExchangeCltData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ExchangeCltItem = {
                'bitset_id': reader.ReadSignedInt(),
                'limit_cnt': reader.ReadSignedInt(),
                'limittype': reader.ReadSignedInt(),
                'popid': reader.ReadSignedInt(),
                'subtag': reader.ReadSignedInt(),
                'user_info_bit_pos': reader.ReadSignedInt(),
                'user_info_id': reader.ReadSignedInt(),
                'batch': reader.ReadSignedInt(),
                'boundmonster': reader.ReadSignedInt(),
                'coinid': reader.ReadSignedInt(),
                'cointype': reader.ReadSignedInt(),
                'count': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'isjustone': reader.ReadSignedInt(),
                'monappend': reader.ReadUTFBytesWithLength(),
                'price': reader.ReadSignedInt(),
                'realid': reader.ReadSignedInt(),
                'shopid': reader.ReadSignedInt(),
                'top': reader.ReadSignedInt(),
                'type': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
