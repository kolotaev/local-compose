import click

from .config import Config
from .executor import Executor
from .printing import Printer, ClickEchoWriter
from .info import version as app_version


@click.group()
def root():
    pass


@root.command()
def version():
    '''
    Version of the tool
    '''
    click.echo(app_version)


@root.command()
@click.option('-f', '--file', show_default=True, default='local-compose.yaml', help='Configuration file.')
@click.option('-b', '--build', is_flag=True, show_default=True, help='Build services before run.')
@click.pass_context
def up(ctx, file, build):
    '''
    Start services
    '''
    conf = Config(file).try_parse()
    processes = []
    writer = ClickEchoWriter()
    executor = Executor(printer=Printer(writer))
    services = conf['services']
    import os
    import os.path
    for name, srv in services.items():
        if srv.get('cwd'):
            cwd = os.path.join(os.getcwd(), srv.get('cwd'))
        else:
            cwd = None
        executor.add_process(name, cmd=srv.get('run'), cwd=cwd, color=srv.get('color'))
    executor.start()
