from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class RetrieveItem(TypedDict):
    id: int
    money: str
    num: list[int]
    ratio: int


class RetrieveConfig(TypedDict):
    data: list[RetrieveItem]


class RetrieveParser(BaseParser[RetrieveConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'retrieve.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'retrieve.json'

    def parse(self, data: bytes) -> RetrieveConfig:
        reader = BytesReader(data)
        result: RetrieveConfig = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            id_val = reader.ReadSignedInt()
            money_val = reader.ReadUTFBytesWithLength()
            num_val: list[int] = []
            if reader.ReadBoolean():
                num_count = reader.ReadSignedInt()
                for _ in range(num_count):
                    num_val.append(reader.ReadSignedInt())
            ratio_val = reader.ReadSignedInt()

            item: RetrieveItem = {
                'id': id_val,
                'money': money_val,
                'num': num_val,
                'ratio': ratio_val,
            }
            result['data'].append(item)

        return result
