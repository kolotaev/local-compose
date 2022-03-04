import os
import re
import time

import pytest
from click.testing import CliRunner

import compose.cli as cli
from compose.info import CONFIG_EXAMPLE


def test_no_args():
    runner = CliRunner()
    result = runner.invoke(cli.root, [])
    assert result.exit_code == 0
    assert 'Usage: root [OPTIONS] COMMAND [ARGS]...' in result.output


def test_banner():
    runner = CliRunner()
    result = runner.invoke(cli.root, [])
    assert result.exit_code == 0
    # we temporarily omitted the banner itself
    assert '''

  Tool for running and managing your services.
''' in result.output


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli.root, ['version'])
    assert result.exit_code == 0
    assert result.output == '0.5.0\n'


def test_example():
    runner = CliRunner()
    result = runner.invoke(cli.root, ['example'])
    assert result.exit_code == 0
    assert result.output == CONFIG_EXAMPLE + '\n'


def test_colors():
    runner = CliRunner()
    result = runner.invoke(cli.root, ['colors'])
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 256
    assert \
'''black
red
green
yellow
blue
magenta
''' in result.output


@pytest.mark.parametrize(
    'command',
    [
        'up',
        'down',
    ]
)
def test_workdir_defaults(command):
    runner = CliRunner()
    result = runner.invoke(cli.root, [command, '--help'])
    # We need it to be '.' so that later it's expanded into current
    assert 'Work dir  [default: .]' in result.output


def test_up_no_file():
    runner = CliRunner()
    result = runner.invoke(cli.root, ['up', '-w', '/path/to/workdir'])
    assert result.exit_code == 1
    assert result.output == '''Configuration file "/path/to/workdir/local-compose.yaml" is invalid.
Errors:
File was not found.
'''


def test_up_one_job():
    runner = CliRunner()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'one-job.yaml')
    result = runner.invoke(cli.root, ['up', '-f', file])
    assert result.exit_code == 0
    out = re.sub(r'pid=\d+', 'pid=22580', result.output)
    assert out == \
''' system  | starting service my-job1
 system  | my-job1 started (pid=22580)
 my-job1 | Hello world
 system  | my-job1 stopped (rc=0)
'''


def test_up_one_malformed_job_command():
    runner = CliRunner()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'malformed-job.yaml')
    result = runner.invoke(cli.root, ['up', '-f', file])
    assert result.exit_code == 0
    out = re.sub(r'pid=\d+', 'pid=22580', result.output)
    assert 'system | starting service job1' in out
    assert 'system | job1 started (pid=22580)' in out
    assert 'expr: division by zero' in out
    assert 'system | job1 stopped (rc=2)' in out


def test_up_silent():
    runner = CliRunner()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'silent.yaml')
    result = runner.invoke(cli.root, ['up', '-f', file])
    assert result.exit_code == 0
    out = re.sub(r'pid=\d+', 'pid=22580', result.output)
    assert out == \
''' system  | starting service my-job1
 system  | my-job1 started (pid=22580)
 system  | my-job1 stopped (rc=0)
'''


@pytest.mark.skip
def test_up_with_color():
    runner = CliRunner()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'with-color.yaml')
    result = runner.invoke(cli.root, ['up', '-f', file], color=True)
    assert result.exit_code == 0
    out = re.sub(r'pid=\d+', 'pid=22580', result.output)
    assert out == \
''' system      | starting service colored-job
 system      | colored-job started (pid=22580)
\033[36m colored-job | Hello world\033[0m
 system      | colored-job stopped (rc=0)
'''


def test_up_with_color_but_explicitly_said_no_color():
    runner = CliRunner()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'with-color.yaml')
    result = runner.invoke(cli.root, ['up', '-f', file, '--no-color'], color=True)
    assert result.exit_code == 0
    out = re.sub(r'pid=\d+', 'pid=22580', result.output)
    assert out == \
''' system      | starting service colored-job
 system      | colored-job started (pid=22580)
 colored-job | Hello world
 system      | colored-job stopped (rc=0)
'''


def test_up_no_prefix():
    runner = CliRunner()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'no-prefix.yaml')
    result = runner.invoke(cli.root, ['up', '-f', file])
    assert result.exit_code == 0
    out = re.sub(r'pid=\d+', 'pid=22580', result.output)
    assert out == \
'''starting service my-job1
my-job1 started (pid=22580)
Hello world
my-job1 stopped (rc=0)
'''


def test_up_with_job_and_daemon():
    runner = CliRunner()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'job-and-daemon.yaml')
    result = runner.invoke(cli.root, ['up', '-f', file])
    assert result.exit_code == 0
    out = re.sub(r'pid=\d+', 'pid=22580', result.output)
    assert \
'''
Job says I'm done
echo1 stopped (rc=0)
Long running says I'm done
web1 stopped (rc=0)
''' in out


def test_up_with_job_retries():
    runner = CliRunner()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'one-job-retries.yaml')
    result = runner.invoke(cli.root, ['up', '-f', file])
    assert result.exit_code == 0
    out = re.sub(r'pid=\d+', 'pid=22580', result.output)
    assert out == \
'''starting service my-job1
my-job1 started (pid=22580)
Hello world
my-job1 stopped (rc=1)
my-job1 is restarting
starting service my-job1
my-job1 started (pid=22580)
Hello world
my-job1 stopped (rc=1)
my-job1 is restarting
starting service my-job1
my-job1 started (pid=22580)
Hello world
my-job1 stopped (rc=1)
my-job1 is restarting
starting service my-job1
my-job1 started (pid=22580)
Hello world
my-job1 stopped (rc=1)
'''


def test_up_down_detached():
    runner = CliRunner()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'web-daemon.yaml')
    try:
        result = runner.invoke(cli.root, ['up', '-f', file, '--detached'])
        assert result.exit_code == 0
        out = re.sub(r'pid = \d+', 'pid = 22580', result.output)
        assert out == 'Started local-compose with pid = 22580\n'
    finally:
        result = runner.invoke(cli.root, ['down', '-f', file])
        assert result.exit_code == 0
        assert result.output == 'Stopped local-compose\n'


@pytest.mark.skip('For some reason it doesn\'t take into account the first run')
def test_up_several_times_same_config_file_is_not_allowed():
    runner = CliRunner()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'web-daemon.yaml')
    result = runner.invoke(cli.root, ['up', '-f', file, '--detached'])
    assert result is not None
    assert result.exit_code == 0
    assert 'Started local-compose with pid = ' in result.output
    import time; time.sleep(5)
    result = runner.invoke(cli.root, ['up', '-f', file])
    assert result.exit_code == 1
    assert result.output == 'System is already running'


@pytest.mark.skip('For some reason it doesn\'t take into account the first run')
def test_up_several_times_different_config_files_is_allowed():
    runner = CliRunner()
    file1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'web-daemon.yaml')
    file2 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'one-job-retries.yaml')
    result = runner.invoke(cli.root, ['up', '-f', file1, '--detached'])
    assert result is not None
    assert result.exit_code == 0
    assert 'Started local-compose with pid = ' in result.output
    import time; time.sleep(5)
    result = runner.invoke(cli.root, ['up', '-f', file2])
    assert result.exit_code == 0
    assert 'Started local-compose with pid = ' in result.output


def test_up_down_in_the_workdir_with_default_filename():
    runner = CliRunner()
    current_work_dir = os.getcwd()
    fixtures_work_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
    try:
        os.chdir(fixtures_work_dir)
        result = runner.invoke(cli.root, ['up'])
        assert result.exit_code == 0
        out = re.sub(r'pid=\d+', 'pid=22580', result.output)
        assert out == \
'''starting service my-defaults
my-defaults started (pid=22580)
I am a default name
my-defaults stopped (rc=0)
'''
        result = runner.invoke(cli.root, ['down'])
        assert result.exit_code == 0
        assert result.output == 'Stopped local-compose\n'
    finally:
        os.chdir(current_work_dir)


def test_up_down_in_the_workdir_with_specific_filename():
    runner = CliRunner()
    current_work_dir = os.getcwd()
    fixtures_work_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
    try:
        os.chdir(fixtures_work_dir)
        result = runner.invoke(cli.root, ['up', '-f', 'no-prefix.yaml'])
        assert result.exit_code == 0
        out = re.sub(r'pid=\d+', 'pid=22580', result.output)
        assert out == \
'''starting service my-job1
my-job1 started (pid=22580)
Hello world
my-job1 stopped (rc=0)
'''
        result = runner.invoke(cli.root, ['down', '-f', 'no-prefix.yaml'])
        assert result.exit_code == 0
        assert result.output == 'Stopped local-compose\n'
    finally:
        os.chdir(current_work_dir)


def test_up_down_when_the_workdir_is_specified_and_no_filename_given():
    runner = CliRunner()
    fixtures_work_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
    result = runner.invoke(cli.root, ['up', '-w', fixtures_work_dir])
    assert result.exit_code == 0
    out = re.sub(r'pid=\d+', 'pid=22580', result.output)
    assert out == \
'''starting service my-defaults
my-defaults started (pid=22580)
I am a default name
my-defaults stopped (rc=0)
'''
    result = runner.invoke(cli.root, ['down', '-w', fixtures_work_dir])
    assert result.exit_code == 0
    assert result.output == 'Stopped local-compose\n'


def test_up_down_when_the_workdir_is_specified_and_filename_given():
    # we need to add it for slow CI runs where cleanup doesn't catchup
    time.sleep(10)
    runner = CliRunner()
    fixtures_work_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
    result = runner.invoke(cli.root, ['up', '-w', fixtures_work_dir, '-f', 'no-prefix.yaml'])
    assert result.exit_code == 0
    out = re.sub(r'pid=\d+', 'pid=22580', result.output)
    assert out == \
'''starting service my-job1
my-job1 started (pid=22580)
Hello world
my-job1 stopped (rc=0)
'''
    result = runner.invoke(cli.root, ['down', '-w', fixtures_work_dir, '-f', 'no-prefix.yaml'])
    assert result.exit_code == 0
    assert result.output == 'Stopped local-compose\n'
