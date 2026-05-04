from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PrivateTrainExtraRewardItem(TypedDict):
    id: int
    reward: str
    value: int


class PrivateTrainExtraRewardConfig(TypedDict):
    data: list[PrivateTrainExtraRewardItem]


class PrivateTrainExtraRewardParser(BaseParser[PrivateTrainExtraRewardConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'privateTrainExtraReward.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'privateTrainExtraReward.json'

    def parse(self, data: bytes) -> PrivateTrainExtraRewardConfig:
        reader = BytesReader(data)
        result: PrivateTrainExtraRewardConfig = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: PrivateTrainExtraRewardItem = {
                'id': reader.ReadSignedInt(),
                'reward': reader.ReadUTFBytesWithLength(),
                'value': reader.ReadSignedInt(),
            }
            result['data'].append(item)

        return result
