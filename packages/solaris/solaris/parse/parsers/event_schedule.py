from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class EventScheduleInfo(TypedDict):
    event_time: int
    event_venue: int
    id: int
    odds_left: int
    odds_right: int
    player_left: int
    player_right: int
    userinfo1: int
    userinfo2: int


class _Root(TypedDict):
    item: list[EventScheduleInfo]


class EventScheduleConfig(TypedDict):
    root: _Root


class EventScheduleParser(BaseParser[EventScheduleConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'eventSchedule.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'eventSchedule.json'

    def parse(self, data: bytes) -> EventScheduleConfig:
        reader = BytesReader(data)
        result: EventScheduleConfig = {'root': {'item': []}}

        if not reader.ReadBoolean():
            return result

        num = reader.ReadSignedInt()
        for _ in range(num):
            item: EventScheduleInfo = {
                'event_time': reader.ReadSignedInt(),
                'event_venue': reader.ReadSignedInt(),
                'id': reader.ReadSignedInt(),
                'odds_left': reader.ReadSignedInt(),
                'odds_right': reader.ReadSignedInt(),
                'player_left': reader.ReadSignedInt(),
                'player_right': reader.ReadSignedInt(),
                'userinfo1': reader.ReadSignedInt(),
                'userinfo2': reader.ReadSignedInt(),
            }
            result['root']['item'].append(item)

        return result
