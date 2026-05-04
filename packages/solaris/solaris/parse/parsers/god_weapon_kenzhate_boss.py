from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class GodWeaponKenzhateBossItem(TypedDict):
    parm1: str
    parm2: str
    id: int
    petid: int


class _GodWeaponKenzhateBossData(TypedDict):
    item: list[GodWeaponKenzhateBossItem]


class GodWeaponKenzhateBossParser(BaseParser[_GodWeaponKenzhateBossData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'GodWeaponKenzhateBoss.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'godWeaponKenzhateBoss.json'

    def parse(self, data: bytes) -> _GodWeaponKenzhateBossData:
        reader = BytesReader(data)
        result: _GodWeaponKenzhateBossData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: GodWeaponKenzhateBossItem = {
                'id': reader.ReadSignedInt(),
                'parm1': reader.ReadUTFBytesWithLength(),
                'parm2': reader.ReadUTFBytesWithLength(),
                'petid': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
