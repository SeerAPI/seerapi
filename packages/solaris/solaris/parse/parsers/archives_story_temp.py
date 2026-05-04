from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ArchivesStoryTempInfo(TypedDict):
    classid: int
    classname: str
    id: int
    isrec: int
    monid: int
    monname: str
    samemonid: list[int]
    storyid: int
    txt: str


class _Root(TypedDict):
    item: list[ArchivesStoryTempInfo]


class ArchivesStoryTempConfig(TypedDict):
    root: _Root


class ArchivesStoryTempParser(BaseParser[ArchivesStoryTempConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'archivesStory_temp.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'archivesStoryTemp.json'

    def parse(self, data: bytes) -> ArchivesStoryTempConfig:
        reader = BytesReader(data)
        result: ArchivesStoryTempConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        num = reader.ReadSignedInt()
        for _ in range(num):
            classid = reader.ReadSignedInt()
            classname = reader.ReadUTFBytesWithLength()
            item_id = reader.ReadSignedInt()
            isrec = reader.ReadSignedInt()
            monid = reader.ReadSignedInt()
            monname = reader.ReadUTFBytesWithLength()
            samemonid: list[int] = []
            if reader.ReadBoolean():
                count = reader.ReadSignedInt()
                samemonid = [reader.ReadSignedInt() for _ in range(count)]
            storyid = reader.ReadSignedInt()
            txt = reader.ReadUTFBytesWithLength()

            item: ArchivesStoryTempInfo = {
                'classid': classid,
                'classname': classname,
                'id': item_id,
                'isrec': isrec,
                'monid': monid,
                'monname': monname,
                'samemonid': samemonid,
                'storyid': storyid,
                'txt': txt,
            }
            result['root']['item'].append(item)

        return result
