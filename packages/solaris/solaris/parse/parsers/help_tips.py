from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _Item(TypedDict):
    desc: str
    html: str
    id: int
    tips: str
    title: str
    type: int


class _Data(TypedDict):
    data: list[_Item]


class HelpTipsParser(BaseParser[_Data]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'help_tips.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'helpTips.json'

    def parse(self, data: bytes) -> _Data:
        reader = BytesReader(data)
        result: _Data = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: _Item = {
                'desc': reader.ReadUTFBytesWithLength(),
                'html': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'tips': reader.ReadUTFBytesWithLength(),
                'title': reader.ReadUTFBytesWithLength(),
                'type': reader.ReadSignedInt(),
            }
            result['data'].append(item)

        return result
