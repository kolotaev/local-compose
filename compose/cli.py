import click
from click.termui import secho

from .config import Config
from .version import VERSION


@click.group()
def root():
    pass


@root.command()
def version():
    '''
    Version of the tool
    '''
    click.echo(VERSION)


@root.command()
@click.option('-f', '--file', show_default=True, default='local-compose.yaml', help='Configuration file.')
@click.option('-d', '--detach', is_flag=True, show_default=True, help='Detached mode: Run services in the background.')
@click.pass_context
def up(ctx, file, detach):
    '''
    Start services
    '''
    conf = Config(file).try_parse()
    secho(str(conf))