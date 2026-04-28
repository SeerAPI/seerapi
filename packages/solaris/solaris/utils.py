from collections.abc import Generator, MutableSequence
from contextlib import contextmanager
from datetime import timedelta, timezone
import importlib
import inspect
from pathlib import Path
import pkgutil
from typing import Any, Final, Literal, TypeVar, get_origin, overload

T = TypeVar('T')


def import_all_classes(package_name: str, base_class: type[T]) -> list[type[T]]:
	"""动态导入并返回指定包及其子包中的所有子类。

	递归遍历指定包及其所有子包，查找并返回继承自指定基类的所有非抽象类。
	该函数会自动处理导入错误，跳过无法导入的模块。

	支持传入包（目录）或单个模块（.py 文件）。

	Args:
		package_name: 要搜索的包名或模块名，如 'solaris.analyze.parsers' 或 'solaris.analyze.parsers.pet'
		base_class: 基类类型，用于筛选子类

	Returns:
		包含所有找到的子类的列表，每个元素都是 base_class 的子类，不会重复出现同一个类。

	Example:
		```python
		# 查找所有解析器类
		parsers = import_all_classes('solaris.parse.parsers', BaseParser)

		# 查找所有分析器类（包）
		analyzers = import_all_classes('solaris.analyze', BaseAnalyzer)

		# 查找单个模块中的分析器类
		analyzers = import_all_classes('solaris.analyze.analyzers.pet.soulmark', BaseAnalyzer)
		```
	"""
	classes = []
	package = importlib.import_module(package_name)

	def _discover_classes_in_module(module: object) -> None:
		"""在指定模块中查找子类。

		Args:
			module: 要搜索的模块对象
		"""
		for attribute_name in dir(module):
			attribute = getattr(module, attribute_name)
			if (
				inspect.isclass(attribute)
				and issubclass(get_origin(attribute) or attribute, base_class)
				and not inspect.isabstract(attribute)
				and attribute not in classes
			):
				classes.append(attribute)

	def _discover_classes(pkg_path: MutableSequence[str], pkg_name: str) -> None:
		"""递归发现指定包及其子包中的子类。

		Args:
			pkg_path: 包路径列表，用于 pkgutil.iter_modules
			pkg_name: 包名，用于构建完整的模块名
		"""
		# 遍历当前包中的所有模块
		for _, module_name, is_pkg in pkgutil.iter_modules(pkg_path, pkg_name + '.'):
			try:
				# 导入模块
				module = importlib.import_module(module_name)
				# 在模块中查找子类
				_discover_classes_in_module(module)

				# 如果是包，递归处理子包
				if is_pkg:
					subpackage = importlib.import_module(module_name)
					_discover_classes(subpackage.__path__, module_name)
			except ImportError:
				# 忽略导入失败的模块
				continue

	# 检查是否为包（有 __path__ 属性）还是模块
	if hasattr(package, '__path__'):
		# 是包，递归遍历
		_discover_classes(package.__path__, package.__name__)
	else:
		# 是单个模块，直接在该模块中查找
		_discover_classes_in_module(package)

	return classes


@contextmanager
def change_workdir(path: str | Path) -> Generator[None, Any, None]:
	"""切换工作路径的上下文管理器"""
	import os

	original_path = os.getcwd()
	try:
		os.chdir(Path(path))
		yield
	finally:
		os.chdir(original_path)


def move_to_last(lst: list, index: int) -> None:
	"""
	将列表中指定索引位置的元素移动到列表的最后一位。

	Args:
		lst: 要操作的列表
		index: 要移动的元素的索引位置

	"""
	if 0 <= index < len(lst):
		# 弹出指定位置的元素并添加到列表末尾
		element = lst.pop(index)
		lst.append(element)


def move_to_first(lst: list, index: int) -> None:
	"""
	将列表中指定索引位置的元素移动到列表的第一位。

	Args:
		lst: 要操作的列表
		index: 要移动的元素的索引位置

	"""
	if 0 <= index < len(lst):
		element = lst.pop(index)
		lst.insert(0, element)


def convert_to_number(value: str) -> int | float:
	"""将输入转换为数字。

	- 接受字符串或数值；当为字符串时会先去除首尾空白再解析。
	- 若解析得到的浮点数小数部分为 0，则返回 ``int``，否则返回 ``float``。
	- 传入空字符串、``None`` 或无法解析为数字的内容将抛出 ``ValueError``。

	Args:
		value: 待转换的值（字符串或数值）。

	Returns:
		解析后的数字（``int`` 或 ``float``）。

	Raises:
		ValueError: 当值为 ``None``、空字符串或无法转换为数字时抛出。
	"""
	if isinstance(value, (int, float)):
		return value

	if not value:
		raise ValueError(f'Invalid value: {value}')

	if isinstance(value, str):
		value = value.strip()
		if not value:
			raise ValueError('Empty string')

	float_value = float(value)
	return int(float_value) if float_value.is_integer() else float_value


@overload
def split_string_arg(
	value: Any,
	*,
	split_char: str | None = None,
	handle_float: Literal[False] = False,
) -> list[int]: ...


@overload
def split_string_arg(
	value: Any,
	*,
	split_char: str | None = None,
	handle_float: Literal[True],
) -> list[float | int]: ...


def split_string_arg(
	value: Any,
	*,
	split_char: str | None = None,
	handle_float: bool = True,
) -> list[int] | list[float] | list[int | float]:
	"""将单个值或分隔字符串转换为数字列表。

	支持两种输入模式：
	1. 非字符串输入：直接转换为单元素列表
	2. 字符串输入：按分隔符拆分后逐个转换

	Args:
		value: 待转换的值，可以是数字、字符串或其他类型
		split_char: 字符串分隔符，None 表示按空白字符分割
		handle_float: 转换模式选择
		- True: 智能转换（使用 convert_to_number，整数优先）
		- False: 强制转换为整数（使用 int()）

	Returns:
		数字列表，元素类型取决于 handle_float 参数：
		- handle_float=True: list[int | float]
		- handle_float=False: list[int]

	Raises:
		ValueError: 当输入无法转换为数字时

	Example:
		```python
		split_string_arg("1,2,3,4.2", split_char=",")  # [1, 2, 3, 4.2]
		split_string_arg("1.5 2.0", handle_float=True)  # [1, 2]
		split_string_arg(42)  # [42]
		```
	"""
	if value == '':
		return []
	if not isinstance(value, str):
		return [convert_to_number(value)] if handle_float else [int(value)]
	return [
		convert_to_number(move) if handle_float else int(move)
		for move in value.strip().split(split_char)
	]


def get_nested_value(
	data: dict, path: str | list, *, delete: bool = False
) -> Any | None:
	"""获取嵌套字典中的值。

	支持通过路径字符串或键列表访问嵌套字典的深层值，可选择是否在访问时删除路径上的键。

	Args:
		data: 嵌套字典，要从中获取值的源字典
		path: 访问路径，可以是：
			- 点号分隔的字符串（如 "level1.level2.key"）
			- 键的列表（如 ["level1", "level2", "key"]）
		delete: 是否在访问时删除路径上的键，默认为 False
			- True: 使用 pop() 删除并返回值
			- False: 仅获取值而不删除

	Returns:
		目标路径的值，若路径不存在则返回 None

	Example:
		```python
		data = {"user": {"profile": {"name": "张三", "age": 25}}}

		# 获取嵌套值
		name = get_nested_value(data, "user.profile.name")  # "张三"
		age = get_nested_value(data, ["user", "profile", "age"])  # 25

		# 获取并删除值
		name = get_nested_value(data, "user.profile.name", delete=True)  # "张三"
		# 此时 data["user"]["profile"] 中已不包含 "name" 键

		# 路径不存在时返回 None
		missing = get_nested_value(data, "user.missing.key")  # None
		```
	"""
	if not data:
		return data
	if not path:
		return data
	if isinstance(path, str):
		path = path.split('.')

	for key in path:
		if data is None or key not in data:
			return None
		data = data.pop(key) if delete else data[key]
	return data


def join_url(base_url: str, *parts: str, end_slash: bool = False) -> str:
	url = '/'.join(
		str(i).strip('/') for i in [base_url, *parts] if i and i not in ('.', '/', './')
	)
	if end_slash:
		url += '/'

	return url


CN_TZ: Final[timezone] = timezone(timedelta(hours=8))
