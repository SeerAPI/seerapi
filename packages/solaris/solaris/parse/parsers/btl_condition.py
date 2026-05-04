from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class BtlConditionInfo(TypedDict):
    baseconid: int
    btldesc: str
    id: int
    send_number: int


class _Root(TypedDict):
    item: list[BtlConditionInfo]


class BtlConditionConfig(TypedDict):
    root: _Root


class BtlConditionParser(BaseParser[BtlConditionConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'btl_condition.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'btlCondition.json'

    def parse(self, data: bytes) -> BtlConditionConfig:
        reader = BytesReader(data)
        result: BtlConditionConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        num = reader.ReadSignedInt()
        for _ in range(num):
            item: BtlConditionInfo = {
                'baseconid': reader.ReadSignedInt(),
                'btldesc': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'send_number': reader.ReadSignedInt(),
            }
            result['root']['item'].append(item)

        return result
