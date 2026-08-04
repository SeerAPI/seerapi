"""Autocard Season Effect 配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class AutocardSeasonEffectInfo(TypedDict):
    """Autocard Season Effect 信息条目"""

    BuffDisplay: str
    BuffId: str
    BuffParam: str
    CountNum: int
    DefaultNum: int
    effectGroup: int
    effectName: str
    effectTxt: str
    id: int
    opTurn: int
    picID: int
    season: int
    stageLevel: int


class AutocardSeasonEffectConfig(TypedDict):
    """Autocard Season Effect 配置数据"""

    data: list[AutocardSeasonEffectInfo]


class AutocardSeasonEffectParser(BaseParser[AutocardSeasonEffectConfig]):
    """解析 autocardSeasonEffect.bytes 配置文件"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'autocardSeasonEffect.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'autocardSeasonEffect.json'

    def parse(self, data: bytes) -> AutocardSeasonEffectConfig:
        reader = BytesReader(data)
        result = AutocardSeasonEffectConfig(data=[])

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            result['data'].append(
                AutocardSeasonEffectInfo(
                    BuffDisplay=reader.ReadUTFBytesWithLength(),
                    BuffId=reader.ReadUTFBytesWithLength(),
                    BuffParam=reader.ReadUTFBytesWithLength(),
                    CountNum=reader.ReadSignedInt(),
                    DefaultNum=reader.ReadSignedInt(),
                    effectGroup=reader.ReadSignedInt(),
                    effectName=reader.ReadUTFBytesWithLength(),
                    effectTxt=reader.ReadUTFBytesWithLength(),
                    id=reader.ReadSignedInt(),
                    opTurn=reader.ReadSignedInt(),
                    picID=reader.ReadSignedInt(),
                    season=reader.ReadSignedInt(),
                    stageLevel=reader.ReadSignedInt(),
                )
            )

        return result
