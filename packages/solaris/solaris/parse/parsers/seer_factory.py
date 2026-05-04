from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class SeerFactoryItem(TypedDict):
    id: int
    suit_id: int
    suit_part_id: list[int]
    suit_price: int
    vip_only: int


class SeerFactoryConfig(TypedDict):
    data: list[SeerFactoryItem]


class SeerFactoryParser(BaseParser[SeerFactoryConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'seerFactory.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'seerFactory.json'

    def parse(self, data: bytes) -> SeerFactoryConfig:
        reader = BytesReader(data)
        result: SeerFactoryConfig = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            id_val = reader.ReadSignedInt()
            suit_id = reader.ReadSignedInt()
            suit_part_id: list[int] = []
            if reader.ReadBoolean():
                part_count = reader.ReadSignedInt()
                for _ in range(part_count):
                    suit_part_id.append(reader.ReadSignedInt())

            item: SeerFactoryItem = {
                'id': id_val,
                'suit_id': suit_id,
                'suit_part_id': suit_part_id,
                'suit_price': reader.ReadSignedInt(),
                'vip_only': reader.ReadSignedInt(),
            }
            result['data'].append(item)

        return result
