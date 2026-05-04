from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PrivateTrainTaskItem(TypedDict):
    group: int
    id: int
    jump: int
    rewardinfo: str
    title: str
    value: int


class PrivateTrainTaskConfig(TypedDict):
    data: list[PrivateTrainTaskItem]


class PrivateTrainTaskParser(BaseParser[PrivateTrainTaskConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'privateTrainTask.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'privateTrainTask.json'

    def parse(self, data: bytes) -> PrivateTrainTaskConfig:
        reader = BytesReader(data)
        result: PrivateTrainTaskConfig = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: PrivateTrainTaskItem = {
                'group': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'jump': reader.ReadSignedInt(),
                'rewardinfo': reader.ReadUTFBytesWithLength(),
                'title': reader.ReadUTFBytesWithLength(),
                'value': reader.ReadSignedInt(),
            }
            result['data'].append(item)

        return result
