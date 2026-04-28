"""PVP 任务配置解析器"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PvpTaskInfo(TypedDict):
    """PVP 任务信息"""

    describe: str
    exp: int
    id: int
    pos: int
    rarity: int
    rewardinfo: str
    subkey: int
    time: int
    title: str
    userinfo: int
    value: int


class PvpTaskConfig(TypedDict):
    """PVP 任务配置"""

    data: list[PvpTaskInfo]


class PvpTaskParser(BaseParser[PvpTaskConfig]):
    """解析 pvp_task.bytes"""

    @classmethod
    def source_config_filename(cls) -> str:
        return "pvp_task.bytes"

    @classmethod
    def parsed_config_filename(cls) -> str:
        return "pvpTask.json"

    def parse(self, data: bytes) -> PvpTaskConfig:
        reader = BytesReader(data)
        result: PvpTaskConfig = {"data": []}

        if not reader.read_bool():
            return result

        count = reader.read_i32()

        for _ in range(count):
            info: PvpTaskInfo = {
                "describe": reader.ReadUTFBytesWithLength(),
                "exp": reader.read_i32(),
                "id": reader.read_i32(),
                "pos": reader.read_i32(),
                "rarity": reader.read_i32(),
                "rewardinfo": reader.ReadUTFBytesWithLength(),
                "subkey": reader.read_i32(),
                "time": reader.read_i32(),
                "title": reader.ReadUTFBytesWithLength(),
                "userinfo": reader.read_i32(),
                "value": reader.read_i32(),
            }
            result["data"].append(info)

        return result
