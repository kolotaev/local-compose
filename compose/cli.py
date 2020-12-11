import click

from .configuration import Config
from .runtime import Scheduler
from .printing import Printer, ClickEchoWriter, SimplePrintWriter
from .info import version as app_version


@click.group()
def root():
    pass
    # ctx.ensure_object(dict)
    # ctx.obj['color'] = color


@root.command()
def version():
    '''
    Version of the tool
    '''
    click.echo(app_version)


@root.command()
def example():
    '''
    Show detailed configuration example
    '''
    click.echo(Config.example())


@root.command()
@click.option('-f', '--file', show_default=True, default='local-compose.yaml', help='Configuration file.')
# @click.option('-b', '--build', is_flag=True, show_default=True, help='Build services before run.')
@click.option('--color/--no-color', default=True, show_default=True, help='Use colored output?')
@click.pass_context
def up(ctx, file, color):
    '''
    Start services
    '''
    conf = Config(file).try_parse()
    if color:
        writer = ClickEchoWriter()
    else:
        writer = SimplePrintWriter()
    printer = Printer(writer, time_format=conf.settings.get('time-format'))
    rt = Scheduler(printer=printer)
    for s in conf.services:
        rt.add_service(s)
    rt.start()
