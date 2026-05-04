from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class RoleInformationItem(TypedDict):
    active_skills: str
    attack: int
    combat_effectiveness: int
    defense: int
    health_points: int
    id: int
    name: str
    passive_skills: str
    petid: int
    resources: str
    speed: int


class RoleInformationConfig(TypedDict):
    data: list[RoleInformationItem]


class RoleInformationParser(BaseParser[RoleInformationConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'roleInformation.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'roleInformation.json'

    def parse(self, data: bytes) -> RoleInformationConfig:
        reader = BytesReader(data)
        result: RoleInformationConfig = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: RoleInformationItem = {
                'active_skills': reader.ReadUTFBytesWithLength(),
                'attack': reader.ReadSignedInt(),
                'combat_effectiveness': reader.ReadSignedInt(),
                'defense': reader.ReadSignedInt(),
                'health_points': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
                'passive_skills': reader.ReadUTFBytesWithLength(),
                'petid': reader.ReadSignedInt(),
                'resources': reader.ReadUTFBytesWithLength(),
                'speed': reader.ReadSignedInt(),
            }
            result['data'].append(item)

        return result
