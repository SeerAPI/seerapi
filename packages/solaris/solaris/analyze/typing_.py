from collections.abc import Callable, Mapping, MutableMapping
from dataclasses import dataclass
from typing import (
	Generic,
	Literal,
	TypeAlias,
	TypedDict,
	TypeVar,
)

from seerapi_models.build_model import BaseResModel, BaseResModelWithOptionalId

from solaris.typing import JSON, ClientPlatform, JSONObject

_MT = TypeVar('_MT', bound=MutableMapping)
CsvTable: TypeAlias = dict[int, _MT]


DataSourceType: TypeAlias = Literal[ClientPlatform, 'patch']


class Patch(TypedDict):
	type: DataSourceType
	target: str
	mode: Literal['append', 'create']
	path: str
	content: JSON


_T = TypeVar('_T')
DataMap: TypeAlias = MutableMapping[str, _T]


class AnalyzeData(TypedDict, total=False):
	unity: DataMap[JSONObject]
	flash: DataMap[JSONObject]
	html5: DataMap[JSONObject]
	patch: DataMap[Patch]


ResModel: TypeAlias = 'BaseResModel | BaseResModelWithOptionalId'


TResModelRequiredId = TypeVar('TResModelRequiredId', bound=BaseResModel)
TResModelWithOptionalId = TypeVar(
	'TResModelWithOptionalId', bound=BaseResModelWithOptionalId
)

TResModel = TypeVar('TResModel', bound=ResModel)

NameGenerator: TypeAlias = Callable[[TResModelRequiredId], str | None]


@dataclass(frozen=True, slots=True)
class AnalyzeResult(Generic[TResModelRequiredId]):
	"""分析结果数据结构

	Args:
		model: 资源模型类型
		data: 资源数据字典，键为ID，值为模型实例
		output_mode: 输出模式，控制数据的输出方式
	"""

	model: type[TResModelRequiredId]
	data: Mapping[int, TResModelRequiredId]
	output_mode: Literal['all', 'not_output', 'db', 'json'] = 'all'
