"""刻印进阶相关配置解析器

解析赛尔号客户端的刻印进阶数据文件，包含刻印进阶的各项配置信息。
"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class MintmarkElevareInfo(TypedDict):
    """刻印进阶项"""

    desc: str
    cost: list[int]
    elevare_mintmark: int
    id: int
    origin_mintmark: int
    primum_mintmark: int
    statinfo: int
    type: int


class _MintmarkElevare(TypedDict):
    """刻印进阶容器"""

    mintmark_elevare: list[MintmarkElevareInfo]


class MintmarkElevareConfig(TypedDict):
    """刻印进阶配置数据"""

    mintmark_elevare: _MintmarkElevare


class MintmarkElevareParser(BaseParser[MintmarkElevareConfig]):
    """刻印进阶配置解析器"""

    @classmethod
    def source_config_filename(cls) -> str:
        return "mintmarkElevare.bytes"

    @classmethod
    def parsed_config_filename(cls) -> str:
        return "mintmarkElevare.json"

    def parse(self, data: bytes) -> MintmarkElevareConfig:
        reader = BytesReader(data)
        result: MintmarkElevareConfig = {"mintmark_elevare": {"mintmark_elevare": []}}

        if reader.ReadBoolean():
            elevare_count = reader.ReadSignedInt()
            for _ in range(elevare_count):
                cost_list: list[int] = []
                if reader.ReadBoolean():
                    cost_count = reader.ReadSignedInt()
                    cost_list = [reader.ReadSignedInt() for _ in range(cost_count)]

                desc = reader.ReadUTFBytesWithLength()

                elevare_mintmark = reader.ReadSignedInt()
                id_value = reader.ReadSignedInt()
                origin_mintmark = reader.ReadSignedInt()
                primum_mintmark = reader.ReadSignedInt()
                statinfo = reader.ReadSignedInt()
                type_value = reader.ReadSignedInt()

                elevare_item: MintmarkElevareInfo = {
                    "desc": desc,
                    "cost": cost_list,
                    "elevare_mintmark": elevare_mintmark,
                    "id": id_value,
                    "origin_mintmark": origin_mintmark,
                    "primum_mintmark": primum_mintmark,
                    "statinfo": statinfo,
                    "type": type_value,
                }
                result["mintmark_elevare"]["mintmark_elevare"].append(elevare_item)

        return result
