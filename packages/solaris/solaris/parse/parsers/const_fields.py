from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ConstFieldsInfo(TypedDict):
    const_class_name: str
    id: int
    key_field: str
    table_name: str
    value_field: str


class _Root(TypedDict):
    item: list[ConstFieldsInfo]


class ConstFieldsConfig(TypedDict):
    root: _Root


class ConstFieldsParser(BaseParser[ConstFieldsConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'const_fields.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'constFields.json'

    def parse(self, data: bytes) -> ConstFieldsConfig:
        reader = BytesReader(data)
        result: ConstFieldsConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        num = reader.ReadSignedInt()
        for _ in range(num):
            item: ConstFieldsInfo = {
                'const_class_name': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'key_field': reader.ReadUTFBytesWithLength(),
                'table_name': reader.ReadUTFBytesWithLength(),
                'value_field': reader.ReadUTFBytesWithLength(),
            }
            result['root']['item'].append(item)

        return result
