"""Autocard Season 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AutocardSeasonInfo(TypedDict):
    """Autocard Season 信息条目"""

    Drawing_times: str
    battletimes_userinfo: str
    currscores_userinfo: str
    id: int
    maxscores_userinfo: str
    name: str
    rankgroup: str
    reward_useinfo: str
    scorereward1: str
    scorereward2: str
    scorereward3: str
    scorereward4: str
    scorereward5: str
    scorereward6: str
    seasonreward1: str
    seasonreward2: str
    seasonreward3: str
    seasonreward4: str
    seasonreward5: str
    seasonreward6: str


class AutocardSeasonConfig(TypedDict):
    """Autocard Season 配置数据"""

    data: list[AutocardSeasonInfo]


class AutocardSeasonParser(BaseParser[AutocardSeasonConfig]):
    """解析 autocardSeason.bytes 配置文件"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'autocardSeason.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'autocardSeason.json'

    def parse(self, data: bytes) -> AutocardSeasonConfig:
        reader = BytesReader(data)
        result = AutocardSeasonConfig(data=[])

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            result['data'].append(
                AutocardSeasonInfo(
                    Drawing_times=reader.ReadUTFBytesWithLength(),
                    battletimes_userinfo=reader.ReadUTFBytesWithLength(),
                    currscores_userinfo=reader.ReadUTFBytesWithLength(),
                    id=reader.ReadSignedInt(),
                    maxscores_userinfo=reader.ReadUTFBytesWithLength(),
                    name=reader.ReadUTFBytesWithLength(),
                    rankgroup=reader.ReadUTFBytesWithLength(),
                    reward_useinfo=reader.ReadUTFBytesWithLength(),
                    scorereward1=reader.ReadUTFBytesWithLength(),
                    scorereward2=reader.ReadUTFBytesWithLength(),
                    scorereward3=reader.ReadUTFBytesWithLength(),
                    scorereward4=reader.ReadUTFBytesWithLength(),
                    scorereward5=reader.ReadUTFBytesWithLength(),
                    scorereward6=reader.ReadUTFBytesWithLength(),
                    seasonreward1=reader.ReadUTFBytesWithLength(),
                    seasonreward2=reader.ReadUTFBytesWithLength(),
                    seasonreward3=reader.ReadUTFBytesWithLength(),
                    seasonreward4=reader.ReadUTFBytesWithLength(),
                    seasonreward5=reader.ReadUTFBytesWithLength(),
                    seasonreward6=reader.ReadUTFBytesWithLength(),
                )
            )

        return result
