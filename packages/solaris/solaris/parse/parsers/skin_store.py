from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class SkinStorePoolItem(TypedDict):
    consumid: int
    cos_num: int
    dis_num: int
    disrate: int
    endtime: int
    free_cos_id: int
    free_cos_num: int
    id: int
    poolid: int
    product_id1: int
    product_id2: int
    quality: int
    rate: int
    skinid: int
    starttime: int
    ticket: int
    ticket_num: int


class _SkinStorePoolData(TypedDict):
    item: list[SkinStorePoolItem]


class SkinStorePoolParser(BaseParser[_SkinStorePoolData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'skinStorePool.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'skinStorePool.json'

    def parse(self, data: bytes) -> _SkinStorePoolData:
        reader = BytesReader(data)
        result: _SkinStorePoolData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: SkinStorePoolItem = {
                'consumid': reader.ReadSignedInt(),
                'cos_num': reader.ReadSignedInt(),
                'dis_num': reader.ReadSignedInt(),
                'disrate': reader.ReadSignedInt(),
                'endtime': reader.ReadSignedInt(),
                'free_cos_id': reader.ReadSignedInt(),
                'free_cos_num': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'poolid': reader.ReadSignedInt(),
                'product_id1': reader.ReadSignedInt(),
                'product_id2': reader.ReadSignedInt(),
                'quality': reader.ReadSignedInt(),
                'rate': reader.ReadSignedInt(),
                'skinid': reader.ReadSignedInt(),
                'starttime': reader.ReadSignedInt(),
                'ticket': reader.ReadSignedInt(),
                'ticket_num': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result


class SkinStoreTicketItem(TypedDict):
    para: list[int]
    id: int
    itemid: int
    product_id: int
    tickettype: int


class _SkinStoreTicketData(TypedDict):
    item: list[SkinStoreTicketItem]


class SkinStoreTicketParser(BaseParser[_SkinStoreTicketData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'skinStoreTicket.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'skinStoreTicket.json'

    def parse(self, data: bytes) -> _SkinStoreTicketData:
        reader = BytesReader(data)
        result: _SkinStoreTicketData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: SkinStoreTicketItem = {
                'id': reader.ReadSignedInt(),
                'itemid': reader.ReadSignedInt(),
                'para': [],
                'product_id': 0,
                'tickettype': 0,
            }
            if reader.ReadBoolean():
                p_count = reader.ReadSignedInt()
                item['para'] = [reader.ReadSignedInt() for _ in range(p_count)]
            item['product_id'] = reader.ReadSignedInt()
            item['tickettype'] = reader.ReadSignedInt()
            result['item'].append(item)

        return result
