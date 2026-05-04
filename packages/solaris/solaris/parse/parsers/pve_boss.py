from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class PveBossBraveTowerItem(TypedDict):
    bossgettext: str
    raidunlocktext: str
    bosslist: list[int]
    rewardid: list[int]
    rewardnum: list[int]
    bossgetarg: int
    id: int


class _PveBossBraveTowerData(TypedDict):
    item: list[PveBossBraveTowerItem]


class PveBossBraveTowerParser(BaseParser[_PveBossBraveTowerData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'PveBossBraveTower.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'pveBossBraveTower.json'

    def parse(self, data: bytes) -> _PveBossBraveTowerData:
        reader = BytesReader(data)
        result: _PveBossBraveTowerData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            bossgetarg = reader.ReadSignedInt()
            bossgettext = reader.ReadUTFBytesWithLength()
            bosslist: list[int] = []
            if reader.ReadBoolean():
                bc = reader.ReadSignedInt()
                bosslist = [reader.ReadSignedInt() for _ in range(bc)]
            item_id = reader.ReadSignedInt()
            raidunlocktext = reader.ReadUTFBytesWithLength()
            rewardid: list[int] = []
            if reader.ReadBoolean():
                ric = reader.ReadSignedInt()
                rewardid = [reader.ReadSignedInt() for _ in range(ric)]
            rewardnum: list[int] = []
            if reader.ReadBoolean():
                rnc = reader.ReadSignedInt()
                rewardnum = [reader.ReadSignedInt() for _ in range(rnc)]
            item: PveBossBraveTowerItem = {
                'bossgettext': bossgettext,
                'raidunlocktext': raidunlocktext,
                'bosslist': bosslist,
                'rewardid': rewardid,
                'rewardnum': rewardnum,
                'bossgetarg': bossgetarg,
                'id': item_id,
            }
            result['item'].append(item)

        return result


class PveBossExperienceTrainingItem(TypedDict):
    raidunlocktext: str
    bosslist: list[int]
    rewardid: list[int]
    rewardnum: list[int]
    id: int
    raidunlockarg: int


class _PveBossExperienceTrainingData(TypedDict):
    item: list[PveBossExperienceTrainingItem]


class PveBossExperienceTrainingParser(BaseParser[_PveBossExperienceTrainingData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'PveBossExperienceTraining.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'pveBossExperienceTraining.json'

    def parse(self, data: bytes) -> _PveBossExperienceTrainingData:
        reader = BytesReader(data)
        result: _PveBossExperienceTrainingData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            bosslist: list[int] = []
            if reader.ReadBoolean():
                bc = reader.ReadSignedInt()
                bosslist = [reader.ReadSignedInt() for _ in range(bc)]
            item_id = reader.ReadSignedInt()
            raidunlockarg = reader.ReadSignedInt()
            raidunlocktext = reader.ReadUTFBytesWithLength()
            rewardid: list[int] = []
            if reader.ReadBoolean():
                ric = reader.ReadSignedInt()
                rewardid = [reader.ReadSignedInt() for _ in range(ric)]
            rewardnum: list[int] = []
            if reader.ReadBoolean():
                rnc = reader.ReadSignedInt()
                rewardnum = [reader.ReadSignedInt() for _ in range(rnc)]
            item: PveBossExperienceTrainingItem = {
                'raidunlocktext': raidunlocktext,
                'bosslist': bosslist,
                'rewardid': rewardid,
                'rewardnum': rewardnum,
                'id': item_id,
                'raidunlockarg': raidunlockarg,
            }
            result['item'].append(item)

        return result


class PveBossLearningTrainingItem(TypedDict):
    raidunlocktext: str
    bosslist: list[int]
    rewardid: list[int]
    rewardnum: list[int]
    id: int
    raidunlockarg: int


class _PveBossLearningTrainingData(TypedDict):
    item: list[PveBossLearningTrainingItem]


class PveBossLearningTrainingParser(BaseParser[_PveBossLearningTrainingData]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'PveBossLearningTraining.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'pveBossLearningTraining.json'

    def parse(self, data: bytes) -> _PveBossLearningTrainingData:
        reader = BytesReader(data)
        result: _PveBossLearningTrainingData = {'item': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            bosslist: list[int] = []
            if reader.ReadBoolean():
                bc = reader.ReadSignedInt()
                bosslist = [reader.ReadSignedInt() for _ in range(bc)]
            item_id = reader.ReadSignedInt()
            raidunlockarg = reader.ReadSignedInt()
            raidunlocktext = reader.ReadUTFBytesWithLength()
            rewardid: list[int] = []
            if reader.ReadBoolean():
                ric = reader.ReadSignedInt()
                rewardid = [reader.ReadSignedInt() for _ in range(ric)]
            rewardnum: list[int] = []
            if reader.ReadBoolean():
                rnc = reader.ReadSignedInt()
                rewardnum = [reader.ReadSignedInt() for _ in range(rnc)]
            item: PveBossLearningTrainingItem = {
                'raidunlocktext': raidunlocktext,
                'bosslist': bosslist,
                'rewardid': rewardid,
                'rewardnum': rewardnum,
                'id': item_id,
                'raidunlockarg': raidunlockarg,
            }
            result['item'].append(item)

        return result
