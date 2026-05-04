from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class BossInfoItem(TypedDict):
    move: str
    se: str
    id: int
    level: int
    pet_id: int


class _BossInfoData(TypedDict):
    item: list[BossInfoItem]


class BossInfoParser(BaseParser[_BossInfoData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'bossInfo.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'bossInfo.json'

    def parse(self, data: bytes) -> _BossInfoData:
        reader = BytesReader(data)
        result: _BossInfoData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: BossInfoItem = {
                'id': reader.ReadSignedInt(),
                'level': reader.ReadSignedInt(),
                'move': reader.ReadUTFBytesWithLength(),
                'pet_id': reader.ReadSignedInt(),
                'se': reader.ReadUTFBytesWithLength(),
            }
            result['item'].append(item)

        return result
