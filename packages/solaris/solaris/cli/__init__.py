import click

from solaris import __package_name__


@click.group(
	invoke_without_command=True,
	context_settings={'help_option_names': ['-h', '--help']},
)
@click.version_option(
	None,
	'-V',
	'--version',
	package_name=__package_name__,
	prog_name='solaris',
)
@click.pass_context
def cli_main(ctx: click.Context) -> None:
	ctx.obj = {}
	if ctx.invoked_subcommand is not None:
		return

	click.echo(ctx.get_help())


from .analyze import analyze
from .parse import parse

cli_main.add_command(parse)
cli_main.add_command(analyze)
