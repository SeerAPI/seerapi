from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PvpCostModeVoteInfo(TypedDict):
    adjust: int
    id: int
    officialsetpet: str
    previousresultpet: str
    previousresultshowtime: int
    ranklimit1: int
    ranklimit2: int
    subkey: int
    time1: int
    time2: int
    type: int
    votenumber: int
    votepet: str


class PvpCostModeVoteConfig(TypedDict):
    item: list[PvpCostModeVoteInfo]


class PvpCostModeVoteParser(BaseParser[PvpCostModeVoteConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'pvpCostMode_vote.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'pvpCostMode_vote.json'

    def parse(self, data: bytes) -> PvpCostModeVoteConfig:
        reader = BytesReader(data)
        result: PvpCostModeVoteConfig = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: PvpCostModeVoteInfo = {
                'adjust': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'officialsetpet': reader.ReadUTFBytesWithLength(),
                'previousresultpet': reader.ReadUTFBytesWithLength(),
                'previousresultshowtime': reader.ReadSignedInt(),
                'ranklimit1': reader.ReadSignedInt(),
                'ranklimit2': reader.ReadSignedInt(),
                'subkey': reader.ReadSignedInt(),
                'time1': reader.ReadSignedInt(),
                'time2': reader.ReadSignedInt(),
                'type': reader.ReadSignedInt(),
                'votenumber': reader.ReadSignedInt(),
                'votepet': reader.ReadUTFBytesWithLength(),
            }
            result['item'].append(item)

        return result
