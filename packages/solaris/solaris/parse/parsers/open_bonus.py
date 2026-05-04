from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class Mintmark(TypedDict):
    """刻印信息"""

    id: int


class OutItem(TypedDict):
    """产出项"""

    mintmark: Mintmark | None


class BonusItem(TypedDict):
    """奖励项"""

    id: int
    out: list[OutItem]


class _Root(TypedDict):
    """根数据结构"""

    bonus: list[BonusItem]


class OpenBonusConfig(TypedDict):
    """开箱奖励配置"""

    root: _Root


class OpenBonusParser(BaseParser[OpenBonusConfig]):
    """开箱奖励解析器"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'open_bonus.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'openBonus.json'

    def parse(self, data: bytes) -> OpenBonusConfig:
        reader = BytesReader(data)
        result: OpenBonusConfig = {'root': {'bonus': []}}

        if not reader.ReadBoolean():
            return result

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            bonus_id = reader.ReadSignedInt()
            out_list: list[OutItem] = []
            if reader.ReadBoolean():
                out_count = reader.ReadSignedInt()
                for _ in range(out_count):
                    mintmark: Mintmark | None = None
                    if reader.ReadBoolean():
                        mintmark = {'id': reader.ReadSignedInt()}

                    out_item: OutItem = {
                        'mintmark': mintmark,
                    }
                    out_list.append(out_item)

            bonus_item: BonusItem = {
                'id': bonus_id,
                'out': out_list,
            }
            result['root']['bonus'].append(bonus_item)

        return result
