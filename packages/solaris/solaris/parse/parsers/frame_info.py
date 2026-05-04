from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class FrameInfoInfo(TypedDict):
    defautl_frame_id: int
    frame_type: int
    id: int
    userinfo: int


class _Root(TypedDict):
    item: list[FrameInfoInfo]


class FrameInfoConfig(TypedDict):
    root: _Root


class FrameInfoParser(BaseParser[FrameInfoConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'FrameInfo.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'frameInfo.json'

    def parse(self, data: bytes) -> FrameInfoConfig:
        reader = BytesReader(data)
        result: FrameInfoConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        num = reader.ReadSignedInt()
        for _ in range(num):
            item: FrameInfoInfo = {
                'defautl_frame_id': reader.ReadSignedInt(),
                'frame_type': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'userinfo': reader.ReadSignedInt(),
            }
            result['root']['item'].append(item)

        return result
