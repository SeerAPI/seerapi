from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class EmojiInfo(TypedDict):
    icon: str
    id: int


class _Root(TypedDict):
    item: list[EmojiInfo]


class EmojiConfig(TypedDict):
    root: _Root


class EmojiParser(BaseParser[EmojiConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'emoji.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'emoji.json'

    def parse(self, data: bytes) -> EmojiConfig:
        reader = BytesReader(data)
        result: EmojiConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        num = reader.ReadSignedInt()
        for _ in range(num):
            item: EmojiInfo = {
                'icon': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
            }
            result['root']['item'].append(item)

        return result
