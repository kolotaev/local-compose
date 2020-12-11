import os
import re

import mock
from click.testing import CliRunner

import compose.cli as cli
from compose.info import config_example


def test_no_args():
    runner = CliRunner()
    result = runner.invoke(cli.root, [])
    assert result.exit_code == 0
    assert 'Usage: root [OPTIONS] COMMAND [ARGS]...' in result.output


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli.root, ['version'])
    assert result.exit_code == 0
    assert '0.1.0\n' == result.output


def test_example():
    runner = CliRunner()
    result = runner.invoke(cli.root, ['example'])
    assert result.exit_code == 0
    assert config_example + '\n' == result.output


def test_up_no_file():
    runner = CliRunner()
    result = runner.invoke(cli.root, ['up'])
    assert result.exit_code == 1
    assert '''Configuration file "local-compose.yaml" is invalid.
Errors found:
File is not found.
''' == result.output


def test_up_one_job():
    runner = CliRunner()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'one-job.yaml')
    result = runner.invoke(cli.root, ['up', '-f', file])
    assert result.exit_code == 0
    out = re.sub(r'pid=\d+', 'pid=22580', result.output)
    assert \
''' system  | starting service my-job1
 system  | my-job1 started (pid=22580)
 my-job1 | I'm OK and I'm done.
 system  | my-job1 stopped (rc=0)
''' == out
