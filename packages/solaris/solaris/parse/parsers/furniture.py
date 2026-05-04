from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class FurnitureInfo(TypedDict):
    func: int
    func_identity: int
    func_param: str
    id: int
    name: str
    type: int
    vip_only: int


class _Root(TypedDict):
    item: list[FurnitureInfo]


class FurnitureConfig(TypedDict):
    root: _Root


class FurnitureParser(BaseParser[FurnitureConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'furniture.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'furniture.json'

    def parse(self, data: bytes) -> FurnitureConfig:
        reader = BytesReader(data)
        result: FurnitureConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        num = reader.ReadSignedInt()
        for _ in range(num):
            item: FurnitureInfo = {
                'func': reader.ReadSignedInt(),
                'func_identity': reader.ReadSignedInt(),
                'func_param': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
                'type': reader.ReadSignedInt(),
                'vip_only': reader.ReadSignedInt(),
            }
            result['root']['item'].append(item)

        return result
