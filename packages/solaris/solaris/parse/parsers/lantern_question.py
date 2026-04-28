"""元宵节问题相关配置解析器

解析赛尔号客户端的元宵节问题文件。
"""

from typing import TypedDict

from ..base import BaseParser
from ..bytes_reader import BytesReader


class LanternQuestionItem(TypedDict):
    achoose: str
    bchoose: str
    cchoose: str
    dchoose: str
    answer: int
    describe: str
    id: int
    title: int


class _Root(TypedDict):
    lantern_question: list[LanternQuestionItem]


class LanternQuestionConfig(TypedDict):
    root: _Root


class LanternQuestionParser(BaseParser[LanternQuestionConfig]):
    @classmethod
    def source_config_filename(cls) -> str:
        return "lanternQuestion.bytes"

    @classmethod
    def parsed_config_filename(cls) -> str:
        return "lanternQuestion.json"

    def parse(self, data: bytes) -> LanternQuestionConfig:
        reader = BytesReader(data)
        result: LanternQuestionConfig = {"root": {"lantern_question": []}}

        if not reader.ReadBoolean():
            return result

        count = reader.ReadSignedInt()

        for _ in range(count):
            item: LanternQuestionItem = {
                "achoose": reader.ReadUTFBytesWithLength(),
                "bchoose": reader.ReadUTFBytesWithLength(),
                "cchoose": reader.ReadUTFBytesWithLength(),
                "dchoose": reader.ReadUTFBytesWithLength(),
                "answer": reader.ReadSignedInt(),
                "describe": reader.ReadUTFBytesWithLength(),
                "id": reader.ReadSignedInt(),
                "title": reader.ReadSignedInt(),
            }
            result["root"]["lantern_question"].append(item)

        return result
