from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _Item(TypedDict):
    activity_num: int
    exchange_cut: int
    id: int
    reward_cnt: str
    reward_id: str
    reward_pr: str
    reward_type: str


class _Data(TypedDict):
    data: list[_Item]


class H512thBoxParser(BaseParser[_Data]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'h5_12th_box.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'h512thBox.json'

    def parse(self, data: bytes) -> _Data:
        reader = BytesReader(data)
        result: _Data = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: _Item = {
                'activity_num': reader.ReadSignedInt(),
                'exchange_cut': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'reward_cnt': reader.ReadUTFBytesWithLength(),
                'reward_id': reader.ReadUTFBytesWithLength(),
                'reward_pr': reader.ReadUTFBytesWithLength(),
                'reward_type': reader.ReadUTFBytesWithLength(),
            }
            result['data'].append(item)

        return result
