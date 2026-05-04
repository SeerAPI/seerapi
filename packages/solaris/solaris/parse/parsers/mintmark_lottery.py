from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class MintMarkItem(TypedDict):
    """刻印项"""

    des: str
    id: int
    level: int
    exchange_id: int
    max_num: int
    price: int
    puton: int


class MenuItem(TypedDict):
    """菜单项"""

    level: int
    mint_mark: list[MintMarkItem]


class Shop(TypedDict):
    """商店"""

    mint_mark: list[MintMarkItem]
    name: str
    num: int


class _Mintmarks(TypedDict):
    """刻印容器"""

    menu: list[MenuItem]
    shop: Shop | None


class MintmarkLotteryConfig(TypedDict):
    """刻印抽奖配置"""

    mintmarks: _Mintmarks


class MintmarkLotteryParser(BaseParser[MintmarkLotteryConfig]):
    """刻印抽奖解析器"""

    @classmethod
    def source_config_filename(cls) -> str:
        return 'mintmark_lottery.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'mintmarkLottery.json'

    def parse(self, data: bytes) -> MintmarkLotteryConfig:
        reader = BytesReader(data)
        result: MintmarkLotteryConfig = {'mintmarks': {'menu': [], 'shop': None}}

        if not reader.ReadBoolean():
            return result

        if reader.ReadBoolean():
            menu_count = reader.ReadSignedInt()
            for _ in range(menu_count):
                menu_level = reader.ReadSignedInt()
                mintmark_list: list[MintMarkItem] = []
                if reader.ReadBoolean():
                    mark_count = reader.ReadSignedInt()
                    for _ in range(mark_count):
                        des = reader.ReadUTFBytesWithLength()
                        mark_id = reader.ReadSignedInt()
                        mark_level = reader.ReadSignedInt()
                        exchange_id = reader.ReadSignedInt()
                        max_num = reader.ReadSignedInt()
                        price = reader.ReadSignedInt()
                        puton = reader.ReadSignedInt()

                        mark_item: MintMarkItem = {
                            'des': des,
                            'id': mark_id,
                            'level': mark_level,
                            'exchange_id': exchange_id,
                            'max_num': max_num,
                            'price': price,
                            'puton': puton,
                        }
                        mintmark_list.append(mark_item)

                menu_item: MenuItem = {
                    'level': menu_level,
                    'mint_mark': mintmark_list,
                }
                result['mintmarks']['menu'].append(menu_item)

        if reader.ReadBoolean():
            shop_mark_list: list[MintMarkItem] = []
            if reader.ReadBoolean():
                shop_mark_count = reader.ReadSignedInt()
                for _ in range(shop_mark_count):
                    des = reader.ReadUTFBytesWithLength()
                    mark_id = reader.ReadSignedInt()
                    mark_level = reader.ReadSignedInt()
                    exchange_id = reader.ReadSignedInt()
                    max_num = reader.ReadSignedInt()
                    price = reader.ReadSignedInt()
                    puton = reader.ReadSignedInt()

                    mark_item: MintMarkItem = {
                        'des': des,
                        'id': mark_id,
                        'level': mark_level,
                        'exchange_id': exchange_id,
                        'max_num': max_num,
                        'price': price,
                        'puton': puton,
                    }
                    shop_mark_list.append(mark_item)

            shop_name = reader.ReadUTFBytesWithLength()
            shop_num = reader.ReadSignedInt()

            shop: Shop = {
                'mint_mark': shop_mark_list,
                'name': shop_name,
                'num': shop_num,
            }
            result['mintmarks']['shop'] = shop

        return result
