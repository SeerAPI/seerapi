from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PveEnterItem(TypedDict):
    open_param: str
    pve_name: str
    res: str
    reward: str
    stat_log: str
    time_limit: str
    id: int
    is_open: int
    is_show: int
    kind: int
    module_id: int
    monsterid: int
    order: int
    show_type: int


class _PveEnterData(TypedDict):
    item: list[PveEnterItem]


class PveEnterParser(BaseParser[_PveEnterData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'pveEnter.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'pveEnter.json'

    def parse(self, data: bytes) -> _PveEnterData:
        reader = BytesReader(data)
        result: _PveEnterData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: PveEnterItem = {
                'id': reader.ReadSignedInt(),
                'is_open': reader.ReadSignedInt(),
                'is_show': reader.ReadSignedInt(),
                'kind': reader.ReadSignedInt(),
                'module_id': reader.ReadSignedInt(),
                'monsterid': reader.ReadSignedInt(),
                'open_param': reader.ReadUTFBytesWithLength(),
                'order': reader.ReadSignedInt(),
                'pve_name': reader.ReadUTFBytesWithLength(),
                'res': reader.ReadUTFBytesWithLength(),
                'reward': reader.ReadUTFBytesWithLength(),
                'show_type': reader.ReadSignedInt(),
                'stat_log': reader.ReadUTFBytesWithLength(),
                'time_limit': reader.ReadUTFBytesWithLength(),
            }
            result['item'].append(item)

        return result
