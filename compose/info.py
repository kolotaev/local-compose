NAME = 'local-compose'

VERSION = '0.3.0'


CONFIG_EXAMPLE = '''
# Specify version of the local-compose yaml schema.
version: '1'

# All global settings.
settings:
    time-format: '%c'

# All services you want to run.
services:
    # First service with name 'web1'
    web1:
        # How to run service binary
        run: ruby server.rb
        # Directory that will be set for service run
        cwd: ~/work/microservices/billing
        # What color should service output use (console logs from service's stdout, stderr)
        color: red
        # Environment variables that are passed into service run.
        env:
            DB_USER: admin
            DB_PASS: 12345
        # Don't show service's output in console.
        silent: yes
        # Execute run service command in system shell (e.g. bash).
        shell: yes
'''
