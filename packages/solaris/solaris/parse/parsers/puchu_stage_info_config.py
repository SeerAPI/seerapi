from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PuchuStageInfoConfigItem(TypedDict):
    id: int
    stage_initial_step: int
    stage_main_map: list[int]
    stage_name: str
    stage_price: int
    stage_tutorial: str
    stage_type: int
    stage_unlock: int


class PuchuStageInfoConfigConfig(TypedDict):
    data: list[PuchuStageInfoConfigItem]


class PuchuStageInfoConfigParser(BaseParser[PuchuStageInfoConfigConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'puchuStageInfoConfig.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'puchuStageInfoConfig.json'

    def parse(self, data: bytes) -> PuchuStageInfoConfigConfig:
        reader = BytesReader(data)
        result: PuchuStageInfoConfigConfig = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            id_val = reader.ReadSignedInt()
            stage_initial_step = reader.ReadSignedInt()
            stage_main_map: list[int] = []
            if reader.ReadBoolean():
                map_count = reader.ReadSignedInt()
                for _ in range(map_count):
                    stage_main_map.append(reader.ReadSignedInt())

            item: PuchuStageInfoConfigItem = {
                'id': id_val,
                'stage_initial_step': stage_initial_step,
                'stage_main_map': stage_main_map,
                'stage_name': reader.ReadUTFBytesWithLength(),
                'stage_price': reader.ReadSignedInt(),
                'stage_tutorial': reader.ReadUTFBytesWithLength(),
                'stage_type': reader.ReadSignedInt(),
                'stage_unlock': reader.ReadSignedInt(),
            }
            result['data'].append(item)

        return result
