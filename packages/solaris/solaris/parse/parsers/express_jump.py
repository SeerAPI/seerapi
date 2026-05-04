from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ExpressJumpInfo(TypedDict):
    click_lock: int
    closeother: int
    dest: str
    id: int
    image: str
    ios_lock: int
    name: str
    priority: int
    reddotid: int
    statlog: str


class _Root(TypedDict):
    item: list[ExpressJumpInfo]


class ExpressJumpConfig(TypedDict):
    root: _Root


class ExpressJumpParser(BaseParser[ExpressJumpConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'express_jump.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'expressJump.json'

    def parse(self, data: bytes) -> ExpressJumpConfig:
        reader = BytesReader(data)
        result: ExpressJumpConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        num = reader.ReadSignedInt()
        for _ in range(num):
            item: ExpressJumpInfo = {
                'click_lock': reader.ReadSignedInt(),
                'closeother': reader.ReadSignedInt(),
                'dest': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'image': reader.ReadUTFBytesWithLength(),
                'ios_lock': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
                'priority': reader.ReadSignedInt(),
                'reddotid': reader.ReadSignedInt(),
                'statlog': reader.ReadUTFBytesWithLength(),
            }
            result['root']['item'].append(item)

        return result
