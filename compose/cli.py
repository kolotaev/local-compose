# -*- coding: utf-8 -*-
import subprocess
import sys

import click

from .configuration import Config
from .runtime import Scheduler, Runner
from .printing import Printer, SimplePrintWriter, ColoredPrintWriter
from .info import VERSION, CONFIG_FILE_NAME, NAME
from .system import Storage


UP_DETACHED_FLAGS = ['-d', '--detached']

@click.group()
def root():
    # pylint: disable=anomalous-backslash-in-string
    """
    \b
    ┏┓━━━━━━━━━━━┓━━━━━━━━━━━━━━━━━━━━━━━━━━
    ┃┃━━━━━━━━━━━┃━━━━━━━━━━━━━━━━━━━━━━━━━━
    ┃┃━━━┓━━┓━━┓━┃━━━━━━━┓━━┓┓┏┓━━┓━━┓━━┓━━┓
    ┃┃━┏┓┃┏━┛━┓┃━┃━━━━┓┏━┛┏┓┃┗┛┃┏┓┃┏┓┃━━┫┏┓┃
    ┃┗┓┗┛┃┗━┓┗┛┗┓┗┓━━━┛┗━┓┗┛┃┃┃┃┗┛┃┗┛┃━━┃┃━┫
    ┗━┛━━┛━━┛━━━┛━┛━━━━━━┛━━┛┻┻┛┏━┛━━┛━━┛━━┛
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃━━━━━━━━━━━
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛━━━━━━━━━━━

    Tool for running and managing your services.
    """


@root.command()
def version():
    '''
    Version of the tool
    '''
    click.echo(VERSION)


@root.command()
def colors():
    '''
    Show available colors you can use for services output
    '''
    for c in Config.available_colors():
        click.echo(c)


@root.command()
def example():
    '''
    Show detailed configuration example
    '''
    click.echo(Config.example())


@root.command()
@click.option('-f', '--file', show_default=True, default=CONFIG_FILE_NAME, help='Configuration file')
@click.option('-w', '--workdir', show_default=True, default='.', help='Work dir')
@click.option(*UP_DETACHED_FLAGS, is_flag=True, show_default=True, help='Detached mode: Run services in the background')
@click.option('--color/--no-color', default=True, show_default=True, help='Use colored output?')
def up(file, workdir, detached, color):
    '''
    Start services
    '''
    conf = Config(file, workdir).try_parse()
    if color:
        writer = ColoredPrintWriter()
    else:
        writer = SimplePrintWriter()
    printer = Printer(writer,
                      time_format=conf.logging.get('time-format'),
                      use_prefix=conf.logging.get('use-prefix', True))
    scheduler = Scheduler(printer=printer)
    for s in conf.services:
        scheduler.register_service(s)
    runner = Runner(Storage(workdir, file), scheduler)
    try:
        runner.check_can_start()
    except RuntimeError as e:
        click.echo(e)
        sys.exit(1)
    if not detached:
        runner.up()
    else:
        new_args = [sys.executable] + [a for a in sys.argv if a not in UP_DETACHED_FLAGS]
        bg = subprocess.Popen(new_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        click.echo('Started %s with pid = %d' % (NAME, bg.pid))


@root.command()
@click.option('-f', '--file', show_default=True, default=CONFIG_FILE_NAME, help='Configuration file')
@click.option('-w', '--workdir', show_default=True, default='.', help='Work dir')
def down(file, workdir):
    '''
    Stop services
    '''
    runner = Runner(Storage(workdir, file), None)
    runner.down()
    click.echo('Stopped %s' % (NAME,))
