from typing import TypedDict

from ..base import BaseParser


class ProfilephotoAutoGiveConfig(TypedDict):
    pass


class ProfilephotoAutoGiveParser(BaseParser[ProfilephotoAutoGiveConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return 'profilephotoAutoGive.bytes'

    @classmethod
    def parsed_config_filename(cls) -> str:
        return 'profilephotoAutoGive.json'

    def parse(self, _data: bytes) -> ProfilephotoAutoGiveConfig:
        return {}
