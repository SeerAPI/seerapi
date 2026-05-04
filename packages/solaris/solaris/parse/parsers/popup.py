from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PopupItem(TypedDict):
    daily: int
    goto: str
    id: int
    num: int
    pic: int
    show_end: str
    show_start: str


class PopupConfig(TypedDict):
    data: list[PopupItem]


class PopupParser(BaseParser[PopupConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'Popup.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'Popup.json'

    def parse(self, data: bytes) -> PopupConfig:
        reader = BytesReader(data)
        result: PopupConfig = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: PopupItem = {
                'daily': reader.ReadSignedInt(),
                'goto': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'num': reader.ReadSignedInt(),
                'pic': reader.ReadSignedInt(),
                'show_end': reader.ReadUTFBytesWithLength(),
                'show_start': reader.ReadUTFBytesWithLength(),
            }
            result['data'].append(item)

        return result
