import os
import re

import mock
import pytest
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


def test_colors():
    runner = CliRunner()
    result = runner.invoke(cli.root, ['colors'])
    assert result.exit_code == 0
    assert 256 == len(result.output.splitlines())
    assert \
'''black
red
green
yellow
blue
magenta
''' in result.output


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
 my-job1 | Hello world
 system  | my-job1 stopped (rc=0)
''' == out


def test_up_silent():
    runner = CliRunner()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'silent.yaml')
    result = runner.invoke(cli.root, ['up', '-f', file])
    assert result.exit_code == 0
    out = re.sub(r'pid=\d+', 'pid=22580', result.output)
    assert \
''' system  | starting service my-job1
 system  | my-job1 started (pid=22580)
 system  | my-job1 stopped (rc=0)
''' == out


@pytest.mark.skip
def test_up_with_color():
    runner = CliRunner()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'with-color.yaml')
    result = runner.invoke(cli.root, ['up', '-f', file], color=True)
    assert result.exit_code == 0
    out = re.sub(r'pid=\d+', 'pid=22580', result.output)
    assert \
''' system      | starting service colored-job\033[0m
 system      | colored-job started (pid=22580)\033[0m
\033[36m colored-job | Hello world\033[0m
 system      | colored-job stopped (rc=0)\033[0m
''' == out


def test_up_with_color_but_explicitly_said_no_color():
    runner = CliRunner()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'with-color.yaml')
    result = runner.invoke(cli.root, ['up', '-f', file, '--no-color'], color=True)
    assert result.exit_code == 0
    out = re.sub(r'pid=\d+', 'pid=22580', result.output)
    assert \
''' system      | starting service colored-job
 system      | colored-job started (pid=22580)
 colored-job | Hello world
 system      | colored-job stopped (rc=0)
''' == out


def test_up_no_prefix():
    runner = CliRunner()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'no-prefix.yaml')
    result = runner.invoke(cli.root, ['up', '-f', file])
    assert result.exit_code == 0
    out = re.sub(r'pid=\d+', 'pid=22580', result.output)
    assert \
'''starting service my-job1
my-job1 started (pid=22580)
Hello world
my-job1 stopped (rc=0)
''' == out
