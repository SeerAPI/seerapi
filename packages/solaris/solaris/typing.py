from pathlib import Path
from typing import Literal, TypeAlias

ClientPlatform: TypeAlias = Literal['unity', 'flash', 'html5']

Paths: TypeAlias = tuple[str | Path, ...]

JSONValue: TypeAlias = 'JSONObject | JSONArray | str | int | float | bool | None'
JSONObject: TypeAlias = dict[str, 'JSONValue']
JSONArray: TypeAlias = list['JSONValue']
JSON: TypeAlias = JSONObject | JSONArray
