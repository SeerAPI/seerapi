from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class RedItem(TypedDict):
    id: int
    forwhat: int


class _Root(TypedDict):
    red: list[RedItem]


class RedbuttonConfig(TypedDict):
    root: _Root


class RedbuttonParser(BaseParser[RedbuttonConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'redbutton.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'redbutton.json'

    def parse(self, data: bytes) -> RedbuttonConfig:
        reader = BytesReader(data)
        result: RedbuttonConfig = {'root': {'red': []}}

        if not reader.ReadBoolean():
            return result

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: RedItem = {
                'id': reader.ReadSignedInt(),
                'forwhat': reader.ReadSignedInt(),
            }
            result['root']['red'].append(item)

        return result
