from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _Item(TypedDict):
    difficulty: int
    id: int
    imagine: int
    inspiration: int
    observe: int
    obstacles_num: int
    reward: str
    skill: int
    unlock_time: int


class _Data(TypedDict):
    data: list[_Item]


class LanglangshanArtCourseConfigParser(BaseParser[_Data]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'langlangshanArtCourseConfig.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'langlangshanArtCourseConfig.json'

    def parse(self, data: bytes) -> _Data:
        reader = BytesReader(data)
        result: _Data = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: _Item = {
                'difficulty': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'imagine': reader.ReadSignedInt(),
                'inspiration': reader.ReadSignedInt(),
                'observe': reader.ReadSignedInt(),
                'obstacles_num': reader.ReadSignedInt(),
                'reward': reader.ReadUTFBytesWithLength(),
                'skill': reader.ReadSignedInt(),
                'unlock_time': reader.ReadSignedInt(),
            }
            result['data'].append(item)

        return result
