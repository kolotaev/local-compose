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
