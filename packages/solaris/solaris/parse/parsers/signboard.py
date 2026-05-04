from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class SignboardItem(TypedDict):
    content: str
    endtime: list[int]
    id: int
    monid: int
    month: list[int]
    starttime: list[int]
    voice: str
    x: int
    y: int


class SignboardConfig(TypedDict):
    data: list[SignboardItem]


class SignboardParser(BaseParser[SignboardConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'Signboard.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'Signboard.json'

    def parse(self, data: bytes) -> SignboardConfig:
        reader = BytesReader(data)
        result: SignboardConfig = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            content_val = reader.ReadUTFBytesWithLength()
            endtime_val: list[int] = []
            if reader.ReadBoolean():
                end_count = reader.ReadSignedInt()
                for _ in range(end_count):
                    endtime_val.append(reader.ReadSignedInt())

            id_val = reader.ReadSignedInt()
            monid_val = reader.ReadSignedInt()

            month_val: list[int] = []
            if reader.ReadBoolean():
                month_count = reader.ReadSignedInt()
                for _ in range(month_count):
                    month_val.append(reader.ReadSignedInt())

            starttime_val: list[int] = []
            if reader.ReadBoolean():
                start_count = reader.ReadSignedInt()
                for _ in range(start_count):
                    starttime_val.append(reader.ReadSignedInt())

            voice_val = reader.ReadUTFBytesWithLength()
            x_val = reader.ReadSignedInt()
            y_val = reader.ReadSignedInt()

            item: SignboardItem = {
                'content': content_val,
                'endtime': endtime_val,
                'id': id_val,
                'monid': monid_val,
                'month': month_val,
                'starttime': starttime_val,
                'voice': voice_val,
                'x': x_val,
                'y': y_val,
            }
            result['data'].append(item)

        return result
