from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AnnouncementInfo(TypedDict):
    beginning: str
    ending: str
    id: int
    shouldread: int
    sorting: int
    subtitle: str
    text: str
    title: str
    type: int


class _Root(TypedDict):
    item: list[AnnouncementInfo]


class AnnouncementConfig(TypedDict):
    root: _Root


class AnnouncementParser(BaseParser[AnnouncementConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'announcement.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'announcement.json'

    def parse(self, data: bytes) -> AnnouncementConfig:
        reader = BytesReader(data)
        result: AnnouncementConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        num = reader.ReadSignedInt()
        for _ in range(num):
            item: AnnouncementInfo = {
                'beginning': reader.ReadUTFBytesWithLength(),
                'ending': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'shouldread': reader.ReadSignedInt(),
                'sorting': reader.ReadSignedInt(),
                'subtitle': reader.ReadUTFBytesWithLength(),
                'text': reader.ReadUTFBytesWithLength(),
                'title': reader.ReadUTFBytesWithLength(),
                'type': reader.ReadSignedInt(),
            }
            result['root']['item'].append(item)

        return result
