from importlib.metadata import version
from pathlib import Path
from typing import TypeVar

import click

import solaris
from solaris.analyze import (
	analyze_result_to_db,
	analyze_result_to_json,
	analyzers_to_jsonschema,
	import_analyzer_classes,
	run_all_analyzer,
)
from solaris.analyze.base import (
	BaseAnalyzer,
	DataImportConfig,
	DataSourceDirSettings,
)
from solaris.analyze.settings import ApiMetadataSettings
from solaris.settings import BaseSettings, CreateSettingsError

TSettings = TypeVar('TSettings', bound=BaseSettings)


def create_settings(
	ctx: click.Context,
	settings_class: type[TSettings],
	*,
	msg_maps: dict[str, str] | None = None,
	**init_kwargs,
) -> TSettings:
	try:
		settings = settings_class.create_settings(
			msg_maps=msg_maps,
			**init_kwargs,
		)
	except CreateSettingsError as e:
		ctx.fail('\n    ' + e.message.replace('\n', '\n    '))

	return settings


@click.group()
@click.option(
	'-w',
	'--source-dir',
	type=click.Path(file_okay=False, dir_okay=True, exists=True, path_type=Path),
	default=None,
	help='数据源目录，如果未指定，则尝试使用环境变量 SOLARIS_DATA_BASE_DIR 的值，'
	'如果均不存在，则使用./source 目录',
)
@click.option(
	'--package-name',
	type=str,
	multiple=True,
	default=('solaris.analyze.analyzers',),
	show_default=True,
	help='要导入的分析器包名',
)
@click.option(
	'-l',
	'--list-analyzers',
	is_flag=True,
	help='输出分析器信息并退出',
)
@click.pass_context
def analyze(
	ctx: click.Context,
	source_dir: Path | None,
	list_analyzers: bool,
	package_name: tuple[str, ...],
) -> None:
	"""分析赛尔号客户端数据并生成API数据或文档。"""

	ctx.ensure_object(dict)
	analyzer_classes: list[type[BaseAnalyzer]] = []
	for name in package_name:
		analyzer_classes.extend(import_analyzer_classes(name))

	ctx.obj['analyzer_classes'] = analyzer_classes

	if list_analyzers:
		string = f'找到 {len(analyzer_classes)} 个分析器:\n'
		string += '\n'.join(
			analyzer_class.get_list_info() for analyzer_class in analyzer_classes
		)
		click.echo(string)
		ctx.exit()

	# 设置数据源目录
	settings = DataSourceDirSettings()
	if source_dir:
		settings.BASE_DIR = Path(source_dir)
	DataImportConfig.set_source_dir(settings)
	ctx.obj['data_source_settings'] = settings


@analyze.command(name='data')
@click.option(
	'-m',
	'--output-mode',
	type=click.Choice(('json', 'db', 'all')),
	default='json',
	show_default=True,
	help='输出模式，json: 输出JSON表，db: 输出到数据库，all: 两者都输出',
)
@click.option(
	'--base-output-dir',
	type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
	default='output',
	show_default=True,
	help='基础输出目录，仅在 --output-mode 为 json 或 all 时有效。',
)
@click.option(
	'-o',
	'--output-dir',
	type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
	default='data',
	show_default=True,
	help='JSON表输出目录，该目录会与 base_output_dir 和 api.version 拼接，'
	'如：base_output_dir=./output, api.version=v1, output_dir=data, '
	'则最终输出目录为 ./output/v1/data。'
	'仅在 --output-mode 为 json 或 all 时有效',
)
@click.option(
	'--base-json-url',
	type=str,
	default=None,
	help='JSON表引用路径基础URL，该参数会覆盖 api_url 的值，'
	'仅在 --output-mode 为 json 或 all 时有效',
	show_default=True,
)
@click.option(
	'--output-named-data/--no-output-named-data',
	default=False,
	show_default=True,
	help='是否在 JSON 表中包含名称到数据的映射数据，'
	'仅在 --output-mode 为 json 或 all 时有效',
)
@click.option(
	'-d',
	'--db-url',
	type=str,
	default='sqlite:///solaris.db',
	show_default=True,
	help='数据库URL，仅在 --output-mode 为 db 或 all 时有效',
)
@click.option(
	'--api-url',
	type=str,
	default=None,
	help='指定API基础URL，该值会作为基础URL与JSON表中的路径拼接，同时写入到metadata.url，'
	'如果未指定，则尝试使用环境变量 SOLARIS_API_URL 的值',
)
@click.option(
	'--api-version',
	type=str,
	default=None,
	help='指定API版本 (例如"v1beta")，该值会作为API URL中的版本号部分，'
	'并写入到metadata.api_version，如果未指定，'
	'则尝试使用环境变量 SOLARIS_API_VERSION 的值',
)
@click.pass_context
def run_command(
	ctx: click.Context,
	base_output_dir: Path,
	output_mode: str,
	output_dir: Path,
	base_json_url: str | None,
	db_url: str,
	api_url: str | None,
	api_version: str | None,
	output_named_data: bool,
) -> None:
	"""运行分析器并输出结果到JSON文件或数据库"""
	analyzer_classes = ctx.obj['analyzer_classes']

	metadata = create_settings(
		ctx,
		ApiMetadataSettings,
		msg_maps={
			'api_url': (
				'未获取到有效的API URL，请使用 --api-url 指定，'
				'或设置环境变量 SOLARIS_API_URL'
			),
			'api_version': (
				'未获取到有效的API版本，请使用 --api-version 指定，'
				'或设置环境变量 SOLARIS_API_VERSION'
			),
		},
		api_url=api_url,
		api_version=api_version,
		generator_name=solaris.__name__,
		generator_version=solaris.__version__,
	)
	api_url = metadata.api_url
	api_version = metadata.api_version

	results = run_all_analyzer(analyzer_classes)
	if output_mode in ('json', 'all'):
		click.echo('正在输出数据到 JSON 文件...')
		analyze_result_to_json(
			results,
			base_output_dir=base_output_dir,
			data_output_dir=output_dir,
			base_data_url=base_json_url,
			metadata=metadata,
			output_named_data=output_named_data,
		)
	if output_mode in ('db', 'all'):
		click.echo('正在输出数据到数据库...')
		analyze_result_to_db(
			results,
			metadata=metadata,
			db_url=db_url,
		)
		click.echo('数据已输出到数据库')


@analyze.command(name='schemas')
@click.option(
	'--base-output-dir',
	type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
	default='output',
	show_default=True,
	help='基础输出目录',
)
@click.option(
	'-o',
	'--output-dir',
	type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
	default='schemas',
	show_default=True,
	help='JSON Schema 输出目录，该目录会与 base_output_dir 和 api.version 拼接，'
	'如：base_output_dir=./output, api.version=v1, output_dir=schemas/, '
	'则最终输出目录为 ./output/v1/schemas/。',
)
@click.option(
	'--api-url',
	type=str,
	default=None,
	help='指定API基础URL，该值会作为JSON Schema 引用路径的基础URL，'
	'如果未指定，则尝试使用环境变量 SOLARIS_API_URL 的值',
)
@click.option(
	'--api-version',
	type=str,
	default=None,
	help='指定API版本 (例如"v1beta")，该值会作为API URL中的版本号部分，'
	'如果未指定，则尝试使用环境变量 SOLARIS_API_VERSION 的值',
)
@click.option(
	'--base-url',
	type=str,
	default=None,
	help='JSON Schema 引用路径基础URL，该参数会覆盖 api_url 的值，',
	show_default=True,
)
@click.option(
	'--output-named-data/--no-output-named-data',
	default=False,
	show_default=True,
	help='是否在 schema 中包含名称到数据的映射数据 Schems',
)
@click.pass_context
def schemas_command(
	ctx: click.Context,
	base_output_dir: Path,
	output_dir: Path,
	base_url: str | None,
	api_url: str | None,
	api_version: str | None,
	output_named_data: bool,
) -> None:
	"""生成 JSON Schema 文件"""
	analyzer_classes = ctx.obj['analyzer_classes']
	metadata = create_settings(
		ctx,
		ApiMetadataSettings,
		msg_maps={
			'api_url': (
				'未获取到有效的API URL，请使用 --api-url 指定，'
				'或设置环境变量 SOLARIS_API_URL'
			),
			'api_version': (
				'未获取到有效的API版本，请使用 --api-version 指定，'
				'或设置环境变量 SOLARIS_API_VERSION'
			),
		},
		api_url=api_url,
		api_version=api_version,
		generator_name=solaris.__name__,
		generator_version=solaris.__version__,
	)
	api_url = metadata.api_url
	api_version = metadata.api_version

	click.echo('正在生成 JSON Schema...')
	analyzers_to_jsonschema(
		analyzer_classes,
		metadata=metadata,
		base_output_dir=base_output_dir,
		schema_output_dir=output_dir,
		base_schema_url=base_url,
		output_named_data=output_named_data,
	)
	click.echo(f'JSON Schema 已生成: {base_output_dir / api_version / output_dir}')


@analyze.command(name='openapi')
@click.option(
	'--detail-version',
	type=str,
	default=version('seerapi-models'),
	help='API 详细版本号，该版本号会写入到 OpenAPI 的 info.version 中，'
	'如果未指定，则尝试使用 seerapi-models 的版本号',
)
@click.option(
	'--base-output-dir',
	type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
	default='output',
	show_default=True,
	help='基础输出目录，该目录会与 api.version 和 -o 选项拼接，'
	'如：base_output_dir=./output, api.version=v1, -o=openapi.json, '
	'则最终输出目录为 ./output/v1/openapi.json。',
)
@click.option(
	'-o',
	'--output',
	type=click.Path(file_okay=True, dir_okay=False, path_type=Path),
	default='openapi.json',
	show_default=True,
	help='OpenAPI schema 输出文件路径',
)
@click.option(
	'--title',
	type=str,
	default='SeerAPI',
	show_default=True,
	help='API 标题',
)
@click.option(
	'--description',
	type=str,
	default='赛尔号游戏数据API',
	help='API 描述',
)
@click.option(
	'--api-url',
	type=str,
	default=None,
	help='指定API基础URL，该值会作为OpenAPI中的服务器地址，'
	'如果未指定，则尝试使用环境变量 SOLARIS_API_URL 的值',
)
@click.option(
	'--api-version',
	type=str,
	default=None,
	help='指定API版本 (例如"v1beta")，该值会作为API URL中的版本号部分，'
	'如果未指定，则尝试使用环境变量 SOLARIS_API_VERSION 的值',
)
@click.option(
	'--output-named-data/--no-output-named-data',
	default=False,
	show_default=True,
	help='是否在 schema 中包含名称到数据的映射数据',
)
@click.pass_context
def openapi_command(
	ctx: click.Context,
	base_output_dir: Path,
	output: Path,
	title: str,
	detail_version: str,
	description: str,
	api_url: str | None,
	api_version: str | None,
	output_named_data: bool,
) -> None:
	"""生成 OpenAPI 3.1 schema 文件"""
	from solaris.analyze import analyzers_to_oad

	analyzer_classes = ctx.obj['analyzer_classes']

	metadata = create_settings(
		ctx,
		ApiMetadataSettings,
		msg_maps={
			'api_url': (
				'未获取到有效的API URL，请使用 --api-url 指定，'
				'或设置环境变量 SOLARIS_API_URL'
			),
			'api_version': (
				'未获取到有效的API版本，请使用 --api-version 指定，'
				'或设置环境变量 SOLARIS_API_VERSION'
			),
		},
		api_url=api_url,
		api_version=api_version,
		generator_name=solaris.__name__,
		generator_version=solaris.__version__,
	)
	api_url = metadata.api_url
	api_version = metadata.api_version

	click.echo('正在生成 OpenAPI schema...')
	analyzers_to_oad(
		analyzer_classes,
		metadata=metadata,
		title=title,
		detail_version=detail_version,
		description=description,
		base_output_dir=base_output_dir,
		output_filepath=output,
		output_named_data=output_named_data,
	)
	click.echo(f'OpenAPI schema 已生成: {base_output_dir / api_version / output}')
