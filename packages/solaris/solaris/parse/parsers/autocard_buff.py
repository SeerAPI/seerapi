"""Autocard Buff 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AutocardBuffInfo(TypedDict):
    """Autocard Buff 信息条目"""

    is_bf_battle_effect: int
    is_cold_wave_effect: int
    is_death_effect: int
    is_growth_effect: int
    is_place_effect: int
    buff_des: str
    buff_object: str
    buff_param: str
    effect_icon: str
    id: int


class AutocardBuffConfig(TypedDict):
    """Autocard Buff 配置数据"""

    data: list[AutocardBuffInfo]


class AutocardBuffParser(BaseParser[AutocardBuffConfig]):
    """解析 autocardBuff.bytes 配置文件"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'autocardBuff.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'autocardBuff.json'

    def parse(self, data: bytes) -> AutocardBuffConfig:
        reader = BytesReader(data)
        result = AutocardBuffConfig(data=[])

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            is_bf_battle_effect = reader.ReadSignedInt()
            is_cold_wave_effect = reader.ReadSignedInt()
            is_death_effect = reader.ReadSignedInt()
            is_growth_effect = reader.ReadSignedInt()
            is_place_effect = reader.ReadSignedInt()
            buff_des = reader.ReadUTFBytesWithLength()
            buff_object = reader.ReadUTFBytesWithLength()
            buff_param = reader.ReadUTFBytesWithLength()
            effect_icon = reader.ReadUTFBytesWithLength()
            id_val = reader.ReadSignedInt()

            result['data'].append(
                AutocardBuffInfo(
                    is_bf_battle_effect=is_bf_battle_effect,
                    is_cold_wave_effect=is_cold_wave_effect,
                    is_death_effect=is_death_effect,
                    is_growth_effect=is_growth_effect,
                    is_place_effect=is_place_effect,
                    buff_des=buff_des,
                    buff_object=buff_object,
                    buff_param=buff_param,
                    effect_icon=effect_icon,
                    id=id_val,
                )
            )

        return result
