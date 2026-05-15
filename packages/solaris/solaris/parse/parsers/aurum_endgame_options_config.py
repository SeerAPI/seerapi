from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AurumEndgameOptionsConfigInfo(TypedDict):
    attritube: str
    branchid: int
    desc: str
    group: int
    id: int
    maxnum: int
    name: str
    rarity: int
    related: int
    root: int
    treeid: int
    type: int
    value: int


class _Root(TypedDict):
    item: list[AurumEndgameOptionsConfigInfo]


class AurumEndgameOptionsConfigConfig(TypedDict):
    root: _Root


class AurumEndgameOptionsConfigParser(BaseParser[AurumEndgameOptionsConfigConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'aurumEndgameOptionsConfig.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'aurumEndgameOptionsConfig.json'

    def parse(self, data: bytes) -> AurumEndgameOptionsConfigConfig:
        reader = BytesReader(data)
        result: AurumEndgameOptionsConfigConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        num = reader.ReadSignedInt()
        for _ in range(num):
            item: AurumEndgameOptionsConfigInfo = {
                'attritube': reader.ReadUTFBytesWithLength(),
                'branchid': reader.ReadSignedInt(),
                'desc': reader.ReadUTFBytesWithLength(),
                'group': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'maxnum': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
                'rarity': reader.ReadSignedInt(),
                'related': reader.ReadSignedInt(),
                'root': reader.ReadSignedInt(),
                'treeid': reader.ReadSignedInt(),
                'type': reader.ReadSignedInt(),
                'value': reader.ReadSignedInt(),
            }
            result['root']['item'].append(item)

        return result
