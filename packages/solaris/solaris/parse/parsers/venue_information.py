from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class VenueInformationItem(TypedDict):
    id: int
    venue_effect: str
    venue_name: str


class VenueInformationConfig(TypedDict):
    data: list[VenueInformationItem]


class VenueInformationParser(BaseParser[VenueInformationConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'venueInformation.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'venueInformation.json'

    def parse(self, data: bytes) -> VenueInformationConfig:
        reader = BytesReader(data)
        result: VenueInformationConfig = {'data': []}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()
        for _ in range(count):
            item: VenueInformationItem = {
                'id': reader.ReadSignedInt(),
                'venue_effect': reader.ReadUTFBytesWithLength(),
                'venue_name': reader.ReadUTFBytesWithLength(),
            }
            result['data'].append(item)

        return result
