from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class GainWayInfo(TypedDict):
    front_goto_1: str
    front_goto_2: str
    front_goto_3: str
    front_goto_4: str
    front_goto_5: str
    goto_1: str
    goto_2: str
    goto_3: str
    goto_4: str
    goto_5: str
    item_id: int
    item_name: str
    show_1: str
    show_2: str
    show_3: str
    show_4: str
    show_5: str
    tab_1: str
    tab_2: str
    tab_3: str
    tab_4: str
    tab_5: str
    text_1: str
    text_2: str
    text_3: str
    text_4: str
    text_5: str
    title: int
    type_1: str
    type_2: str
    type_3: str
    type_4: str
    type_5: str
    id: int


class _Root(TypedDict):
    item: list[GainWayInfo]


class GainWayConfig(TypedDict):
    root: _Root


class GainWayParser(BaseParser[GainWayConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'gainWay.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'gainWay.json'

    def parse(self, data: bytes) -> GainWayConfig:
        reader = BytesReader(data)
        result: GainWayConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        num = reader.ReadSignedInt()
        for _ in range(num):
            item: GainWayInfo = {
                'front_goto_1': reader.ReadUTFBytesWithLength(),
                'front_goto_2': reader.ReadUTFBytesWithLength(),
                'front_goto_3': reader.ReadUTFBytesWithLength(),
                'front_goto_4': reader.ReadUTFBytesWithLength(),
                'front_goto_5': reader.ReadUTFBytesWithLength(),
                'goto_1': reader.ReadUTFBytesWithLength(),
                'goto_2': reader.ReadUTFBytesWithLength(),
                'goto_3': reader.ReadUTFBytesWithLength(),
                'goto_4': reader.ReadUTFBytesWithLength(),
                'goto_5': reader.ReadUTFBytesWithLength(),
                'item_id': reader.ReadSignedInt(),
                'item_name': reader.ReadUTFBytesWithLength(),
                'show_1': reader.ReadUTFBytesWithLength(),
                'show_2': reader.ReadUTFBytesWithLength(),
                'show_3': reader.ReadUTFBytesWithLength(),
                'show_4': reader.ReadUTFBytesWithLength(),
                'show_5': reader.ReadUTFBytesWithLength(),
                'tab_1': reader.ReadUTFBytesWithLength(),
                'tab_2': reader.ReadUTFBytesWithLength(),
                'tab_3': reader.ReadUTFBytesWithLength(),
                'tab_4': reader.ReadUTFBytesWithLength(),
                'tab_5': reader.ReadUTFBytesWithLength(),
                'text_1': reader.ReadUTFBytesWithLength(),
                'text_2': reader.ReadUTFBytesWithLength(),
                'text_3': reader.ReadUTFBytesWithLength(),
                'text_4': reader.ReadUTFBytesWithLength(),
                'text_5': reader.ReadUTFBytesWithLength(),
                'title': reader.ReadSignedInt(),
                'type_1': reader.ReadUTFBytesWithLength(),
                'type_2': reader.ReadUTFBytesWithLength(),
                'type_3': reader.ReadUTFBytesWithLength(),
                'type_4': reader.ReadUTFBytesWithLength(),
                'type_5': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
            }
            result['root']['item'].append(item)

        return result
