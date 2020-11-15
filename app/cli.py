import click


@click.group()
def root():
    '''
    Local-compose is a local services orchestrator.
    '''
    pass

@root.command()
@click.option('-d', '--detached', default=True, help='Attach stdout/stderr to current console')
def up(detached):
    '''
    Run services
    '''
    for x in range(1):
        click.echo('Hello %s!' % name)
