import click


@click.group()
@click.option('-f', '--file', help='Specify compose file')
def root():
    '''
    Local-compose is a local services orchestrator.
    '''

@root.command()
@click.option('-d', '--detach', is_flag=True, help='Detached mode: Run services in the background')
def up(detach):
    '''
    Run services
    '''
    click.echo(detached)
