from collections.abc import Sequence
import inspect
from pathlib import Path
from typing import cast

from openapi_pydantic import Server
from seerapi_models.build_model import BaseGeneralModel, BaseResModel
from seerapi_models.metadata import ApiMetadata
from tqdm import tqdm

from solaris.utils import import_all_classes

from .base import BaseAnalyzer, PostAnalyzerMixin
from .output import DBOutputter, JsonOutputter, OpenAPISchemaOutputter, SchemaOutputter
from .output.db import is_mapped_class
from .output.openapi_builder import OpenAPIBuilder
from .output.schema_generate import seerapi_common_models
from .typing_ import AnalyzeResult

ANALYZER_DEFAULT_PACKAGE_NAME = 'solaris.analyze.analyzers'


class AnalyzerDependencyError(Exception):
	"""分析器依赖关系错误

	当分析器的依赖关系存在问题时抛出，例如：
	- 循环依赖
	- 依赖的分析器不存在
	- 依赖链无法满足
	"""

	pass


class AnalyzerExecutionError(Exception):
	"""分析器执行错误

	当分析器执行过程中发生错误时抛出
	"""

	pass


def get_common_models() -> list[type[BaseGeneralModel]]:
	models: list[type[BaseGeneralModel]] = [
		model
		for model_cls_name in cast(list[str], seerapi_common_models.__all__)
		if (
			(model := getattr(seerapi_common_models, model_cls_name))
			and issubclass(model, BaseGeneralModel)
			and not inspect.isabstract(model)
			and not is_mapped_class(model)
		)
	]
	return models


def collect_analyzer_res_models(
	analyzer_classes: list[type[BaseAnalyzer]],
) -> list[type[BaseResModel]]:
	return [
		model
		for analyzer in analyzer_classes
		for model in analyzer.get_result_res_models()
	]


def analyze_result_to_json(
	results: Sequence[AnalyzeResult],
	*,
	metadata: ApiMetadata,
	base_output_dir: str | Path = '.',
	data_output_dir: str | Path,
	base_data_url: str | None = None,
	merge_json_table: bool = False,
	output_named_data: bool = False,
) -> None:
	"""分析数据并输出到 JSON 文件"""
	json_outputter = JsonOutputter(
		metadata=metadata,
		base_output_dir=base_output_dir,
		data_output_dir=data_output_dir,
		base_data_url=base_data_url,
	)
	json_outputter.run(
		results,
		merge_json_table=merge_json_table,
		output_named_data=output_named_data,
	)


def analyze_result_to_db(
	results: Sequence[AnalyzeResult],
	*,
	metadata: ApiMetadata,
	db_url: str = 'sqlite:///solaris.db',
) -> None:
	"""分析数据并输出到数据库（向后兼容的函数包装）"""
	outputter = DBOutputter(
		metadata=metadata,
		db_url=db_url,
		echo=False,
	)
	outputter.init()
	outputter.run(results)


def analyzers_to_jsonschema(
	analyzer_classes: list[type[BaseAnalyzer]],
	*,
	metadata: ApiMetadata,
	base_output_dir: str | Path = '.',
	schema_output_dir: str | Path,
	base_schema_url: str | None = None,
	output_named_data: bool = False,
) -> None:
	schema_outputter = SchemaOutputter(
		metadata=metadata,
		base_output_dir=base_output_dir,
		schema_output_dir=schema_output_dir,
		base_schema_url=base_schema_url,
	)
	schema_outputter.run(
		res_models=collect_analyzer_res_models(analyzer_classes),
		common_models=get_common_models(),
		output_named_data=output_named_data,
	)


def analyzers_to_oad(
	analyzer_classes: list[type[BaseAnalyzer]],
	*,
	metadata: ApiMetadata,
	title: str,
	detail_version: str,
	description: str,
	base_output_dir: str | Path = '.',
	output_filepath: str | Path = 'openapi.json',
	output_named_data: bool = False,
) -> None:
	openapi_builder = OpenAPIBuilder(
		title=title,
		version=detail_version,
		description=description,
		servers=[Server(url=metadata.api_url)],
	)
	schema_outputter = OpenAPISchemaOutputter(
		metadata=metadata,
		openapi_builder=openapi_builder,
		base_output_dir=base_output_dir,
		output_filepath=output_filepath,
	)
	schema_outputter.run(
		res_models=collect_analyzer_res_models(analyzer_classes),
		common_models=get_common_models(),
		output_named_data=output_named_data,
	)


def import_analyzer_classes(
	package_name: str = ANALYZER_DEFAULT_PACKAGE_NAME,
) -> list[type[BaseAnalyzer]]:
	return import_all_classes(package_name, BaseAnalyzer)


def _build_dependency_graph(
	analyzers: list[type[BaseAnalyzer]],
) -> dict[type[BaseAnalyzer], list[type[BaseAnalyzer]]]:
	"""构建分析器的依赖关系图

	Args:
		analyzers: 分析器类列表

	Returns:
		依赖关系图，键为分析器类，值为其依赖的分析器类列表

	Raises:
		AnalyzerDependencyError: 当存在循环依赖或依赖的分析器不存在时
	"""
	analyzer_set = set(analyzers)
	dependency_graph: dict[type[BaseAnalyzer], list[type[BaseAnalyzer]]] = {}

	# 构建依赖图
	for analyzer in analyzers:
		# 检查是否是后处理分析器（使用 Mixin 检查而不是具体类）
		if issubclass(analyzer, PostAnalyzerMixin):
			# 直接调用类方法获取依赖，不需要创建实例
			dependencies = list(analyzer.get_input_analyzers())

			# 检查依赖是否都存在
			for dep in dependencies:
				if dep not in analyzer_set:
					raise AnalyzerDependencyError(
						f'分析器 {analyzer.__name__} 依赖的分析器 '
						f'{dep.__name__} 不在分析器列表中'
					)

			dependency_graph[analyzer] = dependencies
		else:
			# 数据源分析器没有依赖
			dependency_graph[analyzer] = []

	# 检测循环依赖
	def _has_cycle(
		node: type[BaseAnalyzer],
		visited: set[type[BaseAnalyzer]],
		rec_stack: set[type[BaseAnalyzer]],
	) -> bool:
		visited.add(node)
		rec_stack.add(node)

		for neighbor in dependency_graph.get(node, []):
			if neighbor not in visited:
				if _has_cycle(neighbor, visited, rec_stack):
					return True
			elif neighbor in rec_stack:
				return True

		rec_stack.remove(node)
		return False

	visited: set[type[BaseAnalyzer]] = set()
	for analyzer in analyzers:
		if analyzer not in visited:
			if _has_cycle(analyzer, visited, set()):
				raise AnalyzerDependencyError(
					f'检测到循环依赖，涉及分析器：{analyzer.__name__}'
				)

	return dependency_graph


def _topological_sort_analyzers(
	analyzers: list[type[BaseAnalyzer]],
	dependency_graph: dict[type[BaseAnalyzer], list[type[BaseAnalyzer]]],
) -> list[type[BaseAnalyzer]]:
	"""使用拓扑排序确定分析器的执行顺序

	在依赖图中，dependency_graph[A] = [B, C] 表示 A 依赖 B 和 C，
	因此 B 和 C 必须在 A 之前执行。

	Args:
		analyzers: 分析器类列表
		dependency_graph: 依赖关系图，键为分析器，值为它依赖的分析器列表

	Returns:
		排序后的分析器列表，保证依赖的分析器在前

	Raises:
		AnalyzerDependencyError: 当存在循环依赖时（理论上不应该发生）
	"""
	# 计算每个节点的入度（该节点依赖多少个其他节点）
	in_degree: dict[type[BaseAnalyzer], int] = {
		analyzer: len(dependency_graph.get(analyzer, [])) for analyzer in analyzers
	}

	# 找出所有入度为 0 的节点（没有依赖的节点）
	queue: list[type[BaseAnalyzer]] = [
		analyzer for analyzer in analyzers if in_degree[analyzer] == 0
	]
	sorted_analyzers: list[type[BaseAnalyzer]] = []

	while queue:
		# 取出入度为 0 的节点
		current = queue.pop(0)
		sorted_analyzers.append(current)

		# 找出所有依赖当前节点的节点，将它们的入度减 1
		for analyzer in analyzers:
			if current in dependency_graph.get(analyzer, []):
				in_degree[analyzer] -= 1
				if in_degree[analyzer] == 0:
					queue.append(analyzer)

	# 检查是否所有节点都已排序
	if len(sorted_analyzers) != len(analyzers):
		raise AnalyzerDependencyError('无法完成拓扑排序，可能存在循环依赖')

	return sorted_analyzers


def run_all_analyzer(
	analyzers: list[type[BaseAnalyzer]],
) -> list[AnalyzeResult]:
	"""执行所有分析器，自动处理依赖关系

	该函数会：
	1. 分析依赖关系并进行拓扑排序
	2. 按依赖顺序执行分析器
	3. 为后处理分析器传入其依赖的分析器结果

	Args:
		analyzers: 分析器类列表

	Returns:
		所有分析器的结果列表

	Raises:
		AnalyzerDependencyError: 当依赖关系存在问题时
		AnalyzerExecutionError: 当分析器执行失败时
	"""
	if not analyzers:
		return []

	# 构建依赖图并排序
	dependency_graph = _build_dependency_graph(analyzers)
	sorted_analyzers = _topological_sort_analyzers(analyzers, dependency_graph)

	# 存储所有分析器的结果
	analyzer_results: dict[type[BaseAnalyzer], list[AnalyzeResult]] = {}
	all_results: list[AnalyzeResult] = []

	# 按顺序执行分析器
	for analyzer_cls in (pbar_analyzer := tqdm(sorted_analyzers, leave=False)):
		pbar_analyzer.set_description(
			f'正在分析数据 | 调用{analyzer_cls.__name__}',
			refresh=True,
		)

		try:
			# 根据类型创建分析器实例
			# 检查是否使用了 PostAnalyzerMixin
			if issubclass(analyzer_cls, PostAnalyzerMixin):
				# 后处理分析器需要传入依赖结果
				analyzer = analyzer_cls(input_results=analyzer_results)
			else:
				# 数据源分析器直接创建
				analyzer = analyzer_cls()

			# 执行分析

			result = analyzer.analyze()

			# 存储结果
			analyzer_results[analyzer_cls] = list(result)
			all_results.extend(result)

		except Exception as e:
			raise AnalyzerExecutionError(
				f'分析器 {analyzer_cls.__name__} 执行失败：{e}'
			) from e

	return all_results
