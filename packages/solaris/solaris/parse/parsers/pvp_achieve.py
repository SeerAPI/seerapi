from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PvpAchieveInfo(TypedDict):
    describe: str
    foreverType: int
    id: int
    rewardinfo: str
    title: str
    value: int


class PvpAchieveConfig(TypedDict):
    data: list[PvpAchieveInfo]


class PvpAchieveParser(BaseParser[PvpAchieveConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return "pvp_achieve.bytes"

    @classmethod
    def parsed_config_filename(cls) -> str:
        return "pvpAchieve.json"

    def parse(self, data: bytes) -> PvpAchieveConfig:
        reader = BytesReader(data)
        result: PvpAchieveConfig = {"data": []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            info: PvpAchieveInfo = {
                "describe": reader.ReadUTFBytesWithLength(),
                "foreverType": reader.ReadSignedInt(),
                "id": reader.ReadSignedInt(),
                "rewardinfo": reader.ReadUTFBytesWithLength(),
                "title": reader.ReadUTFBytesWithLength(),
                "value": reader.ReadSignedInt(),
            }
            result["data"].append(info)

        return result
