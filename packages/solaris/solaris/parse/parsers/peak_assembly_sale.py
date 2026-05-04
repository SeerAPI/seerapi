from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PeakAssemblySaleItem(TypedDict):
    extra_moves_id: int
    id: int
    is_sell: int
    mintmark_id: int
    monster_id: int
    month: int
    new_se_id: int
    new_stat_log1: int
    new_stat_log2: int
    new_stat_log3: int
    skin_id: int
    year: int


class _PeakAssemblySaleData(TypedDict):
    item: list[PeakAssemblySaleItem]


class PeakAssemblySaleParser(BaseParser[_PeakAssemblySaleData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'PeakAssemblySale.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'peakAssemblySale.json'

    def parse(self, data: bytes) -> _PeakAssemblySaleData:
        reader = BytesReader(data)
        result: _PeakAssemblySaleData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: PeakAssemblySaleItem = {
                'extra_moves_id': reader.ReadSignedInt(),
                'is_sell': reader.ReadSignedInt(),
                'mintmark_id': reader.ReadSignedInt(),
                'monster_id': reader.ReadSignedInt(),
                'month': reader.ReadSignedInt(),
                'new_se_id': reader.ReadSignedInt(),
                'new_stat_log1': reader.ReadSignedInt(),
                'new_stat_log2': reader.ReadSignedInt(),
                'new_stat_log3': reader.ReadSignedInt(),
                'skin_id': reader.ReadSignedInt(),
                'year': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
