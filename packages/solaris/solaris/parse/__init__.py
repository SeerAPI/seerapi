from collections.abc import Sequence
from pathlib import Path
import warnings

from solaris.parse.base import BaseParser
from solaris.utils import change_workdir, import_all_classes

PARSER_DEFAULT_PACKAGE_NAME = 'solaris.parse.parsers'


def import_parser_classes(
	package_name: str = PARSER_DEFAULT_PACKAGE_NAME,
) -> list[type[BaseParser]]:
	"""导入包下的所有解析器类

	Args:
		package_name: 包名，默认为 "solaris.parse.parsers"

	Returns:
		解析器类列表
	"""
	parsers = import_all_classes(
		package_name,
		BaseParser,
	)
	parsed_files = {}
	for parser in parsers:
		filename = parser.parsed_config_filename()
		if filename in parsed_files:
			warnings.warn(
				f'解析器的输出文件名重复: "{filename}"，'
				f'冲突的解析器: {parsed_files[filename].__name__} 和 {parser.__name__}，'
				f'请修改解析器的输出文件名，或者删除重复的解析器',
				UserWarning,
			)
		parsed_files[filename] = parser
	return parsers


def filter_parser_classes(
	parser_classes: list[type[BaseParser]],
	names: Sequence[str],
) -> tuple[list[type[BaseParser]], set[str]]:
	"""按源文件名筛选解析器类

	支持带扩展名（如 "monsters.bytes"）或不带扩展名（如 "monsters"）的匹配。
	不带扩展名时会去掉 source_config_filename 的扩展名后进行比较。

	Args:
		parser_classes: 解析器类列表
		names: 要匹配的源文件名列表

	Returns:
		(匹配的解析器类列表, 未匹配到的名称集合)
	"""
	name_set = set(names)

	def _matches(cls: type[BaseParser]) -> bool:
		source = cls.source_config_filename()
		stem = source.rsplit('.', 1)[0] if '.' in source else source
		return source in name_set or stem in name_set

	filtered = [cls for cls in parser_classes if _matches(cls)]
	matched_names: set[str] = set()
	for cls in filtered:
		source = cls.source_config_filename()
		stem = source.rsplit('.', 1)[0] if '.' in source else source
		matched_names.update(name_set & {source, stem})
	not_found = name_set - matched_names
	return filtered, not_found


def run_all_parser(
	parser_classes: list[type[BaseParser]],
	source_dir: Path,
	output_dir: Path,
) -> None:
	"""运行所有解析器

	Args:
		parser_classes: 解析器类列表
		source_dir: 源配置文件目录
		output_dir: 解析结果输出目录
	"""

	parsed_data = {}
	with change_workdir(source_dir):
		for parser_cls in parser_classes:
			parser = parser_cls()
			data = parser.load_source_config()
			parsed_data[parser_cls] = parser.parse(data)

	with change_workdir(output_dir):
		for parser_cls in parser_classes:
			parser = parser_cls()
			parser.save_parsed_config(parsed_data[parser_cls])


__all__ = [
	'BaseParser',
	'filter_parser_classes',
	'import_parser_classes',
	'run_all_parser',
]
