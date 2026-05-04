from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class ElGachaItem(TypedDict):
    endtime: str
    name: str
    starttime: str
    id: int
    poolid: int
    s_item: int
    ss_item: int
    ticket: int


class _ElGachaData(TypedDict):
    item: list[ElGachaItem]


class ElGachaParser(BaseParser[_ElGachaData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'elGacha.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'elGacha.json'

    def parse(self, data: bytes) -> _ElGachaData:
        reader = BytesReader(data)
        result: _ElGachaData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ElGachaItem = {
                'ss_item': reader.ReadSignedInt(),
                's_item': reader.ReadSignedInt(),
                'endtime': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
                'poolid': reader.ReadSignedInt(),
                'starttime': reader.ReadUTFBytesWithLength(),
                'ticket': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result


class ElfGachaItem(TypedDict):
    endtime: str
    name: str
    starttime: str
    a_item: int
    b_item: int
    cost1: int
    discost: int
    disitem: int
    exchange_num: int
    id: int
    miditem: int
    poolid: int
    s_item: int
    ss_item: int
    taskred: int
    ticket: int
    tips: int
    videotype: int


class _ElfGachaData(TypedDict):
    item: list[ElfGachaItem]


class ElfGachaParser(BaseParser[_ElfGachaData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'elfGacha.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'elfGacha.json'

    def parse(self, data: bytes) -> _ElfGachaData:
        reader = BytesReader(data)
        result: _ElfGachaData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ElfGachaItem = {
                'a_item': reader.ReadSignedInt(),
                'b_item': reader.ReadSignedInt(),
                'ss_item': reader.ReadSignedInt(),
                's_item': reader.ReadSignedInt(),
                'tips': reader.ReadSignedInt(),
                'cost1': reader.ReadSignedInt(),
                'discost': reader.ReadSignedInt(),
                'disitem': reader.ReadSignedInt(),
                'endtime': reader.ReadUTFBytesWithLength(),
                'exchange_num': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'miditem': reader.ReadSignedInt(),
                'name': reader.ReadUTFBytesWithLength(),
                'poolid': reader.ReadSignedInt(),
                'starttime': reader.ReadUTFBytesWithLength(),
                'taskred': reader.ReadSignedInt(),
                'ticket': reader.ReadSignedInt(),
                'videotype': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result


class ElfGachaDetailsItem(TypedDict):
    itempro: str
    id: int
    item: int
    number: int
    poolid: int
    quality: int


class _ElfGachaDetailsData(TypedDict):
    item: list[ElfGachaDetailsItem]


class ElfGachaDetailsParser(BaseParser[_ElfGachaDetailsData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'elfGachaDetails.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'elfGachaDetails.json'

    def parse(self, data: bytes) -> _ElfGachaDetailsData:
        reader = BytesReader(data)
        result: _ElfGachaDetailsData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ElfGachaDetailsItem = {
                'id': reader.ReadSignedInt(),
                'item': reader.ReadSignedInt(),
                'itempro': reader.ReadUTFBytesWithLength(),
                'number': reader.ReadSignedInt(),
                'poolid': reader.ReadSignedInt(),
                'quality': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result


class ElfGachaRewardItem(TypedDict):
    endtime: str
    starttime: str
    consumeid: int
    consumnum: int
    discount: int
    distance: int
    id: int
    new_msglog_id: int
    pet_5th_move: int
    pet_id: int
    pet_limit: int
    pet_mint: int
    pet_newse_id: int
    poolid: int
    pooltype: int
    quality: int


class _ElfGachaRewardData(TypedDict):
    item: list[ElfGachaRewardItem]


class ElfGachaRewardParser(BaseParser[_ElfGachaRewardData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'elfGachaReward.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'elfGachaReward.json'

    def parse(self, data: bytes) -> _ElfGachaRewardData:
        reader = BytesReader(data)
        result: _ElfGachaRewardData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ElfGachaRewardItem = {
                'discount': reader.ReadSignedInt(),
                'distance': reader.ReadSignedInt(),
                'new_msglog_id': reader.ReadSignedInt(),
                'pet_5th_move': reader.ReadSignedInt(),
                'pet_id': reader.ReadSignedInt(),
                'pet_limit': reader.ReadSignedInt(),
                'pet_mint': reader.ReadSignedInt(),
                'pet_newse_id': reader.ReadSignedInt(),
                'consumeid': reader.ReadSignedInt(),
                'consumnum': reader.ReadSignedInt(),
                'endtime': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'poolid': reader.ReadSignedInt(),
                'pooltype': reader.ReadSignedInt(),
                'quality': reader.ReadSignedInt(),
                'starttime': reader.ReadUTFBytesWithLength(),
            }
            result['item'].append(item)

        return result


class ElfGachaStoreItem(TypedDict):
    endtime: str
    reward: str
    starttime: str
    consumeid: int
    consumnum: int
    id: int
    new_msglog_id: int
    poolid: int
    storeid: int


class _ElfGachaStoreData(TypedDict):
    item: list[ElfGachaStoreItem]


class ElfGachaStoreParser(BaseParser[_ElfGachaStoreData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'elfGachaStore.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'elfGachaStore.json'

    def parse(self, data: bytes) -> _ElfGachaStoreData:
        reader = BytesReader(data)
        result: _ElfGachaStoreData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ElfGachaStoreItem = {
                'new_msglog_id': reader.ReadSignedInt(),
                'consumeid': reader.ReadSignedInt(),
                'consumnum': reader.ReadSignedInt(),
                'endtime': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'poolid': reader.ReadSignedInt(),
                'reward': reader.ReadUTFBytesWithLength(),
                'starttime': reader.ReadUTFBytesWithLength(),
                'storeid': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result


class ElfGachaTaskItem(TypedDict):
    endtime: str
    rewardinfo: str
    title: str
    id: int
    new_msglog_id: int
    poolid: int
    taskid: int
    value: int


class _ElfGachaTaskData(TypedDict):
    item: list[ElfGachaTaskItem]


class ElfGachaTaskParser(BaseParser[_ElfGachaTaskData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'elfGachaTask.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'elfGachaTask.json'

    def parse(self, data: bytes) -> _ElfGachaTaskData:
        reader = BytesReader(data)
        result: _ElfGachaTaskData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: ElfGachaTaskItem = {
                'new_msglog_id': reader.ReadSignedInt(),
                'endtime': reader.ReadUTFBytesWithLength(),
                'id': reader.ReadSignedInt(),
                'poolid': reader.ReadSignedInt(),
                'rewardinfo': reader.ReadUTFBytesWithLength(),
                'taskid': reader.ReadSignedInt(),
                'title': reader.ReadUTFBytesWithLength(),
                'value': reader.ReadSignedInt(),
            }
            result['item'].append(item)

        return result
