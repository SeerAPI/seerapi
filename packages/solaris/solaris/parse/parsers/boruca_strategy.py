from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class BorucaStrategyInfo(TypedDict):
    id: int
    place: int
    role: str
    situation: str
    sotryid: int
    time: int
    title: str


class _Root(TypedDict):
    item: list[BorucaStrategyInfo]


class BorucaStrategyConfig(TypedDict):
    root: _Root


class BorucaStrategyParser(BaseParser[BorucaStrategyConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'boruca_strategy.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'borucaStrategy.json'

    def parse(self, data: bytes) -> BorucaStrategyConfig:
        reader = BytesReader(data)
        result: BorucaStrategyConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        num = reader.ReadSignedInt()
        for _ in range(num):
            item: BorucaStrategyInfo = {
                'id': reader.ReadSignedInt(),
                'place': reader.ReadSignedInt(),
                'role': reader.ReadUTFBytesWithLength(),
                'situation': reader.ReadUTFBytesWithLength(),
                'sotryid': reader.ReadSignedInt(),
                'time': reader.ReadSignedInt(),
                'title': reader.ReadUTFBytesWithLength(),
            }
            result['root']['item'].append(item)

        return result
