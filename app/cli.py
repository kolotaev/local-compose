import click

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
    click.echo(detach)
    click.echo(ctx.obj)
