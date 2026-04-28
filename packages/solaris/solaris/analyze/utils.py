from collections.abc import Hashable
import functools
from typing import TYPE_CHECKING, Any, Generic, TypeVar

import pydantic_core

from .typing_ import CsvTable

if TYPE_CHECKING:
	from seerapi_models.build_model import BaseCategoryModel


_KT = TypeVar('_KT', bound=Hashable)
_VT = TypeVar('_VT', bound=Any)
_ET = TypeVar('_ET', bound=Any)


class CategoryMap(dict[_KT, _VT], Generic[_KT, _VT, _ET]):
	def __init__(self, category_key: str):
		super().__init__()
		self.category_key = category_key

	def get_category(self, key: _KT) -> list[_ET]:
		return getattr(self[key], self.category_key)

	def add_element(self, key: _KT, *elements: _ET):
		self.get_category(key).extend(elements)


_CVT = TypeVar('_CVT', bound='BaseCategoryModel')


def create_category_map(
	csv_table: 'CsvTable',
	*,
	model_cls: type[_CVT],
	array_key: str,
	**kwargs: Any,
) -> CategoryMap[int, _CVT, Any]:
	"""创建分类映射表，使用指定的模型类。

	从CSV表格数据创建CategoryMap实例，每个条目使用指定的模型类进行实例化。

	Args:
		csv_table: CSV表格数据，键为ID，值为数据字典
		model_cls: 用于实例化的模型类
		（某行数据为空字典时，仍会实例化对应模型，仅包含 kwargs 与空的 array_key）
		array_key: 数组字段键名，必须存在于模型类的字段中；
		该字段将被强制初始化为一个空列表（即使 CSV 或 kwargs 提供了该字段值也会被覆盖）
		**kwargs: 额外的字段参数，将传递给模型构造函数，若与 CSV 行存在同名字段，
		则覆盖 CSV 中的值

	Returns:
		CategoryMap实例，键为ID，值为模型实例。当 csv_table 为空时，
		返回空的 CategoryMap。

	Raises:
		ValueError: 当array_key不存在于模型类字段中时抛出

	Example:
		```python
		class PetModel(BaseCategoryModel):
			id: int
			name: str
			skills: list[str] = []

		csv_data = {
			1: {"name": "布布种子"},
			2: {"name": "小火猴"}
		}

		result = create_category_map(
			csv_data,
			model_cls=PetModel,
			array_key="skills"
		)

		# 可以添加技能到分类中
		result.add_element(1, "撞击", "疾风刃")
		result.add_element(2, "火花", "抓")

		# 访问数据
		pet1 = result[1]  # PetModel实例
		skills = result.get_category(1)  # ["撞击", "疾风刃"]
		```
	"""
	result = CategoryMap[int, _CVT, Any](array_key)
	if not csv_table:
		return result

	if array_key not in model_cls.model_fields:
		raise ValueError(f'array_key {array_key} not in model {model_cls}')

	for id_, csv_data in csv_table.items():
		kw = {**csv_data, **kwargs, array_key: []}
		sub_obj = model_cls(**kw)
		result[id_] = sub_obj

	return result


T = TypeVar('T', bound=Hashable)


def merge_dict_item(target: dict[T, Any], source: dict[T, Any], key: T) -> None:
	"""将 source 字典中的key对应的值合并到 target 中，
	若 source 中不存在key，则不进行合并
	"""
	if source.get(key) is not None:
		target[key] = source[key]


to_json = functools.partial(
	pydantic_core.to_json,
	by_alias=True,
	indent=2,
)
