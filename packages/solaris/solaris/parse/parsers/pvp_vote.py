"""PVP 投票配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PvpVoteInfo(TypedDict):
    """PVP 投票信息"""

    id: int
    name: str
    number: int
    oldresult: str
    ranklimit1: int
    ranklimit2: int
    result: str
    subkey: int
    time1: int
    time2: int
    type: int


class PvpVoteConfig(TypedDict):
    """PVP 投票配置"""

    data: list[PvpVoteInfo]


class PvpVoteParser(BaseParser[PvpVoteConfig]):
    """解析 pvp_vote.bytes"""

    @classmethod
    def source_config_filename(cls) -> str:
        return "pvp_vote.bytes"

    @classmethod
    def parsed_config_filename(cls) -> str:
        return "pvpVote.json"

    def parse(self, data: bytes) -> PvpVoteConfig:
        reader = BytesReader(data)
        result: PvpVoteConfig = {"data": []}

        if not reader.read_bool():
            return result

        count = reader.read_i32()

        for _ in range(count):
            info: PvpVoteInfo = {
                "id": reader.read_i32(),
                "name": reader.ReadUTFBytesWithLength(),
                "number": reader.read_i32(),
                "oldresult": reader.ReadUTFBytesWithLength(),
                "ranklimit1": reader.read_i32(),
                "ranklimit2": reader.read_i32(),
                "result": reader.ReadUTFBytesWithLength(),
                "subkey": reader.read_i32(),
                "time1": reader.read_i32(),
                "time2": reader.read_i32(),
                "type": reader.read_i32(),
            }
            result["data"].append(info)

        return result
