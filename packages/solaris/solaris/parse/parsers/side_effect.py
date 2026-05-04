from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class SideEffectItem(TypedDict):
    id: int
    side_effect_arg: str
    side_effect_argcount: int


class _SideEffects(TypedDict):
    side_effect: list[SideEffectItem]


class SideEffectConfig(TypedDict):
    side_effects: _SideEffects


class SideEffectParser(BaseParser[SideEffectConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'side_effect.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'side_effect.json'

    def parse(self, data: bytes) -> SideEffectConfig:
        reader = BytesReader(data)
        result: SideEffectConfig = {'side_effects': {'side_effect': []}}

        if not reader.ReadBoolean():
            return result

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: SideEffectItem = {
                'id': reader.ReadSignedInt(),
                'side_effect_arg': reader.ReadUTFBytesWithLength(),
                'side_effect_argcount': reader.ReadSignedInt(),
            }
            result['side_effects']['side_effect'].append(item)

        return result
