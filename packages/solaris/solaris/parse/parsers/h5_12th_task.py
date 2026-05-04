from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _Item(TypedDict):
    is_daily_task: int
    task_description: str
    task_schedule: int
    task_tags: str
    task_type: int
    user_info: int
    id: int
    reward_cnt: str
    reward_id: str
    reward_type: str


class _Data(TypedDict):
    data: list[_Item]


class H512thTaskParser(BaseParser[_Data]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'h5_12th_task.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'h512thTask.json'

    def parse(self, data: bytes) -> _Data:
        reader = BytesReader(data)
        result: _Data = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: _Item = {
                'is_daily_task': reader.ReadSignedInt(),
                'task_description': reader.ReadUTFBytesWithLength(),
                'task_schedule': reader.ReadSignedInt(),
                'task_tags': reader.ReadUTFBytesWithLength(),
                'task_type': reader.ReadSignedInt(),
                'user_info': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'reward_cnt': reader.ReadUTFBytesWithLength(),
                'reward_id': reader.ReadUTFBytesWithLength(),
                'reward_type': reader.ReadUTFBytesWithLength(),
            }
            result['data'].append(item)

        return result
