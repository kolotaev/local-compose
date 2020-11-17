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
@click.option('-d', '--detach', is_flag=True, show_default=True, help='Detached mode: Run services in the background.')
@click.pass_context
def up(ctx, detach):
    '''
    Start services
    '''
    secho(str(detach), fg='red')
    click.echo(ctx.obj)
