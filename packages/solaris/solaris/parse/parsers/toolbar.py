from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ToolbarItem(TypedDict):
    chs: str
    id: int
    key: str
    limit_flag: str
    pos: int
    reddot: str
    res: str
    response: str
    stat: str
    type: str


class ToolbarConfig(TypedDict):
    data: list[ToolbarItem]


class ToolbarParser(BaseParser[ToolbarConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'toolbar.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'toolbar.json'

    def parse(self, data: bytes) -> ToolbarConfig:
        reader = BytesReader(data)
        result: ToolbarConfig = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ToolbarItem = {
                'chs': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'key': reader.ReadUTFBytesWithLength(),
                'limit_flag': reader.ReadUTFBytesWithLength(),
                'pos': reader.ReadSignedInt(),
                'reddot': reader.ReadUTFBytesWithLength(),
                'res': reader.ReadUTFBytesWithLength(),
                'response': reader.ReadUTFBytesWithLength(),
                'stat': reader.ReadUTFBytesWithLength(),
                'type': reader.ReadUTFBytesWithLength(),
            }
            result['data'].append(item)

        return result
