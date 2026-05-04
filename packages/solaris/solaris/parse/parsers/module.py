from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class _Item(TypedDict):
    curr_app_do: int
    id: int
    is_full_screen: int
    module_name: str
    res_config: list[str]


class _Data(TypedDict):
    data: list[_Item]


class ModuleParser(BaseParser[_Data]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'module.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'module.json'

    def parse(self, data: bytes) -> _Data:
        reader = BytesReader(data)
        result: _Data = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: _Item = {
                'curr_app_do': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'is_full_screen': reader.ReadSignedInt(),
                'module_name': reader.ReadUTFBytesWithLength(),
                'res_config': [],
            }
            if reader.ReadBoolean():
                res_count = reader.ReadSignedInt()
                for _ in range(res_count):
                    item['res_config'].append(reader.ReadUTFBytesWithLength())
            result['data'].append(item)

        return result
