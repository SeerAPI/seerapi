from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import KW_ONLY, dataclass, field
import json
from pathlib import Path
from typing import Any, ClassVar, cast

from seerapi_models.build_model import BaseResModel
import xmltodict

from solaris.analyze.settings import DataSourceDirSettings
from solaris.typing import JSON, Paths
from solaris.utils import convert_to_number, get_nested_value

from .typing_ import (
	AnalyzeData,
	AnalyzeResult,
	DataSourceType,
	JSONObject,
	Patch,
	TResModelRequiredId,
)


def _convert_xml_attr_to_number(_, key, value):
	try:
		return key, round(convert_to_number(value), 3)
	except:  # noqa: E722
		return key, value


@dataclass
class DataImportConfig:
	SOURCE_DIR_SETTINGS: ClassVar[DataSourceDirSettings] = DataSourceDirSettings()
	_: KW_ONLY
	patch_paths: Paths = field(default_factory=tuple)
	html5_paths: Paths = field(default_factory=tuple)
	unity_paths: Paths = field(default_factory=tuple)
	flash_paths: Paths = field(default_factory=tuple)

	def __post_init__(self):
		self.patch_paths = self._resolve_paths(
			self.SOURCE_DIR_SETTINGS.PATCH_DIR, self.patch_paths
		)
		self.html5_paths = self._resolve_paths(
			self.SOURCE_DIR_SETTINGS.HTML5_DIR, self.html5_paths
		)
		self.unity_paths = self._resolve_paths(
			self.SOURCE_DIR_SETTINGS.UNITY_DIR, self.unity_paths
		)
		self.flash_paths = self._resolve_paths(
			self.SOURCE_DIR_SETTINGS.FLASH_DIR, self.flash_paths
		)

	def _resolve_paths(self, base_dir: Path, paths: Paths) -> tuple[Path, ...]:
		"""将字符串路径解析为完整的Path对象"""
		return tuple(base_dir.joinpath(path) for path in paths)

	def __add__(self, other: 'DataImportConfig') -> 'DataImportConfig':
		if not isinstance(other, DataImportConfig):
			raise ValueError(f'other must be DataImportConfig, but got {type(other)}')
		obj = DataImportConfig()
		obj.patch_paths = self.patch_paths + other.patch_paths
		obj.html5_paths = self.html5_paths + other.html5_paths
		obj.unity_paths = self.unity_paths + other.unity_paths
		obj.flash_paths = self.flash_paths + other.flash_paths
		return obj

	@classmethod
	def set_source_dir(cls, settings: DataSourceDirSettings) -> None:
		cls.SOURCE_DIR_SETTINGS = settings


class DataLoader(ABC):
	"""数据加载器抽象基类"""

	def __init__(self) -> None:
		super().__init__()
		import_config = self.get_data_import_config()
		base_dirs: DataSourceDirSettings = import_config.SOURCE_DIR_SETTINGS
		self.data: AnalyzeData = {
			'html5': self._load_data_by_category(
				import_config.html5_paths, base_dirs.HTML5_DIR, self._load_html5_data
			),
			'unity': self._load_data_by_category(
				import_config.unity_paths, base_dirs.UNITY_DIR, self._load_unity_data
			),
			'flash': self._load_data_by_category(
				import_config.flash_paths, base_dirs.FLASH_DIR, self._load_flash_data
			),
			'patch': self._load_data_by_category(
				import_config.patch_paths, base_dirs.PATCH_DIR, self._load_patch
			),
		}

		for patch in self.data['patch'].values():
			target = patch['target']
			patch_type = patch['type']
			mode = patch['mode']
			content = patch['content']
			# 如果补丁模式为 create，则直接在指定平台中新建一条数据，
			# 如果已存在同名数据则覆盖
			if mode == 'create':
				content = self._process_create_patch_content(content)
				self.data[patch_type][target] = content  # type: ignore[assignment]
				continue
			# 如果补丁模式为 append，则将内容追加到目标数据的指定位置
			for fp, origin_data in self.data[patch_type].items():
				if target != fp:
					continue

				obj_path = patch['path']
				if (
					origin := get_nested_value(cast(dict, origin_data), obj_path)
				) is None:
					continue

				if not isinstance(origin, type(content)):
					raise ValueError(f'patch {fp} content type mismatch')
				if isinstance(origin, list) and isinstance(content, list):
					origin.extend(content)
				elif isinstance(origin, dict) and isinstance(content, dict):
					origin.update(content)

	@staticmethod
	def _load_data_by_category(
		paths: Paths, base_dir: Path, loader_func: Callable[[str | Path], Any]
	) -> dict[str, Any]:
		"""根据路径列表和加载函数加载数据"""
		return {
			str(Path(path).relative_to(base_dir)): loader_func(path) for path in paths
		}

	@classmethod
	def _load_patch(cls, path: str | Path) -> Patch:
		return cast(Patch, cls._load_data(path))

	@classmethod
	def _load_data(cls, path: str | Path) -> JSONObject:
		"""加载数据，优先尝试以JSON格式加载，如果失败则尝试以XML格式加载"""
		data = Path(path).read_text()
		try:
			return json.loads(Path(path).read_text())
		except json.JSONDecodeError:
			return xmltodict.parse(
				data,
				encoding='utf-8',
				attr_prefix='',
				postprocessor=_convert_xml_attr_to_number,
			)

	@classmethod
	def _load_flash_data(cls, path: str | Path) -> JSONObject:
		return cls._load_data(path)

	@classmethod
	def _load_unity_data(cls, path: str | Path) -> JSONObject:
		return cls._load_data(path)

	@classmethod
	def _load_html5_data(cls, path: str | Path) -> JSONObject:
		return cls._load_data(path)

	@classmethod
	@abstractmethod
	def get_data_import_config(cls) -> 'DataImportConfig':
		pass

	def _get_data(self, source: DataSourceType, key: str) -> Any:
		if not (sub := self.data.get(source)):
			raise ValueError(f'data.{source} is required')
		if not (sub := sub.get(key)):
			raise ValueError(f'data.{source}.{key} is required')
		return sub

	@staticmethod
	def _process_create_patch_content(content: JSON) -> JSONObject:
		"""处理补丁 context，将内容转换为以ID为键的字典格式

		Args:
			content: 输入的JSON内容，可以是字典或列表

		Returns:
			JSONObject: 以ID为键的字典，键为整数类型的ID，值为原始数据

		Raises:
			ValueError: 当ID不是有效的字符串、整数或浮点数类型时抛出异常
		"""
		new_content = {}
		for i, v in enumerate(
			content.values() if isinstance(content, dict) else content
		):
			if isinstance(v, dict):
				id_ = v.get('id') or v.get('ID') or i
			else:
				id_ = i

			if not isinstance(id_, (str, int, float)):
				raise ValueError(f'invalid id: {id_}')

			new_content[int(id_)] = v

		return new_content


class BaseAnalyzer(ABC):
	"""分析器抽象基类"""

	@abstractmethod
	def analyze(self) -> tuple[AnalyzeResult, ...]:
		pass

	@classmethod
	@abstractmethod
	def get_result_res_models(cls) -> tuple[type[BaseResModel], ...]:
		"""获取该分析器返回为 JSON 类型的资源模型类型列表，该方法必须被子类实现"""
		pass

	@classmethod
	def get_list_info(cls) -> str:
		"""获取在列表选项中显示的信息字符串

		Returns:
			str: 包含分析器信息的字符串，包括类名和数据导入配置
		"""
		class_name = cls.__name__
		class_path = cls.__module__
		return f'分析器: {class_name} | {class_path}'


class BaseDataSourceAnalyzer(DataLoader, BaseAnalyzer):
	"""数据源分析器抽象基类"""

	@classmethod
	def get_list_info(cls) -> str:
		"""获取在列表选项中显示的信息字符串

		Returns:
			str: 包含分析器信息的字符串，包括类名、模块路径和数据导入配置
		"""
		class_name = cls.__name__
		class_path = cls.__module__
		config = cls.get_data_import_config()

		# 基本信息
		info_parts = [f'分析器: {class_name} | {class_path}']

		# 格式化路径信息
		def _format_paths(paths: Paths, source_type: str) -> str:
			if not paths:
				return ''
			base_dir = config.SOURCE_DIR_SETTINGS.BASE_DIR
			paths_str = '\n'.join(
				f'    {Path(path).relative_to(base_dir)}' for path in paths
			)
			return f'{source_type}: \n{paths_str}'

		# 收集数据源路径信息
		path_info = []
		if config.patch_paths:
			path_info.append(_format_paths(config.patch_paths, '补丁文件'))
		if config.html5_paths:
			path_info.append(_format_paths(config.html5_paths, 'HTML5文件'))
		if config.unity_paths:
			path_info.append(_format_paths(config.unity_paths, 'Unity文件'))
		if config.flash_paths:
			path_info.append(_format_paths(config.flash_paths, 'Flash文件'))

		if path_info:
			info_parts.extend(path_info)

		return '\n  '.join(info_parts)


class PostAnalyzerMixin:
	"""后处理分析器Mixin，提供接收和访问其他分析器结果的功能

	该Mixin可以与任何分析器基类组合使用，使分析器能够接收其他分析器的结果。
	使用Mixin模式可以支持多重继承，例如同时继承DataLoader和后处理功能。

	使用该Mixin的类需要实现 get_input_analyzers() 类方法来声明依赖的分析器。
	"""

	def __init__(self, **kwargs: Any) -> None:
		"""初始化后处理分析器Mixin

		Args:
			**kwargs: 关键字参数，包括：
				- input_results: 依赖分析器的结果字典，
					键为分析器类，值为该分析器的结果列表
				- 其他参数将传递给父类
		"""
		# 从kwargs中提取input_results参数
		self._input_results: dict[type[BaseAnalyzer], list[AnalyzeResult]] = (
			kwargs.pop('input_results', None) or {}
		)
		# 调用父类的__init__，支持多重继承链
		super().__init__(**kwargs)

	@classmethod
	@abstractmethod
	def get_input_analyzers(cls) -> tuple[type[BaseAnalyzer], ...]:
		"""返回该分析器依赖的分析器类列表

		Returns:
			依赖的分析器类元组，这些分析器必须在当前分析器之前执行
		"""
		pass

	def _get_input_data(
		self,
		analyzer_cls: type[BaseAnalyzer],
		model_cls: type[TResModelRequiredId],
	) -> dict[int, TResModelRequiredId]:
		"""获取指定分析器的指定模型数据字典

		Args:
			analyzer_cls: 分析器类
			model_cls: 模型类

		Returns:
			数据字典，键为ID，值为模型实例

		Raises:
			ValueError: 如果找不到指定的分析器或模型
		"""
		result = self._get_input_result(analyzer_cls, model_cls)
		return dict(result.data)

	def _get_input_result(
		self,
		analyzer_cls: type[BaseAnalyzer],
		model_cls: type[TResModelRequiredId],
	) -> AnalyzeResult[TResModelRequiredId]:
		"""获取指定分析器的指定模型 AnalyzeResult

		Args:
			analyzer_cls: 分析器类
			model_cls: 模型类

		Returns:
			AnalyzeResult 对象

		Raises:
			ValueError: 如果找不到指定的分析器或模型
		"""
		results = self._get_all_input_results(analyzer_cls)
		for result in results:
			if result.model == model_cls:
				return result

		raise ValueError(
			f'未找到分析器 {analyzer_cls.__name__} 的模型 {model_cls.__name__} 的结果'
		)

	def _get_all_input_results(
		self,
		analyzer_cls: type[BaseAnalyzer],
	) -> list[AnalyzeResult]:
		"""获取指定分析器的所有结果

		Args:
			analyzer_cls: 分析器类

		Returns:
			AnalyzeResult 列表

		Raises:
			ValueError: 如果找不到指定的分析器
		"""
		if analyzer_cls not in self._input_results:
			raise ValueError(f'未找到分析器 {analyzer_cls.__name__} 的结果')

		return self._input_results[analyzer_cls]


class BasePostAnalyzer(PostAnalyzerMixin, BaseAnalyzer):
	"""后处理分析器抽象基类，该类型的分析器使用其他分析器的分析结果作为输入

	后处理分析器需要实现 get_input_analyzers() 类方法来声明依赖的分析器。
	在构造时会接收所有依赖分析器的结果，可以通过辅助方法获取需要的数据。

	Example:
		```python
		class MyPostAnalyzer(BasePostAnalyzer):
			@classmethod
			def get_input_analyzers(cls) -> tuple[type[BaseAnalyzer], ...]:
				return (SkillAnalyzer, EffectAnalyzer)

			def analyze(self) -> tuple[AnalyzeResult, ...]:
				# 获取技能数据
				skill_data = self._get_input_data(SkillAnalyzer, Skill)
				# 获取效果结果
				effect_result = self._get_input_result(EffectAnalyzer, PetEffect)
				# 处理数据...
				return (AnalyzeResult(model=MyModel, data=my_data),)
		```
	"""

	pass


class BaseDataSourcePostAnalyzer(PostAnalyzerMixin, BaseDataSourceAnalyzer):
	"""混合分析器抽象基类，既能加载数据源又能接收其他分析器结果

	该类结合了 DataLoader 和 PostAnalyzerMixin 的功能，
	适用于需要同时访问原始数据源和其他分析器处理结果的场景。

	Example:
		```python
		class MyHybridAnalyzer(BaseDataSourcePostAnalyzer):
			@classmethod
			def get_data_import_config(cls) -> DataImportConfig:
				return DataImportConfig(
					unity_paths=['some_data.json']
				)

			@classmethod
			def get_input_analyzers(cls) -> tuple[type[BaseAnalyzer], ...]:
				return (SkillAnalyzer,)

			def analyze(self) -> tuple[AnalyzeResult, ...]:
				# 可以访问数据源
				raw_data = self._get_data('unity', 'some_data.json')
				# 也可以访问其他分析器的结果
				skill_data = self._get_input_data(SkillAnalyzer, Skill)
				# 处理数据...
				return (AnalyzeResult(model=MyModel, data=my_data),)
		```
	"""

	pass
