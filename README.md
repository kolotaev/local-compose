
[![Build](https://github.com/kolotaev/local-compose/workflows/Tests/badge.svg?branch=master)](https://github.com/kolotaev/local-compose/actions)
[![Coverage](https://codecov.io/github/kolotaev/local-compose/coverage.svg?branch=master)](https://codecov.io/github/kolotaev/local-compose?branch=master)
<!-- [![Supported Versions](https://img.shields.io/pypi/pyversions/local-compose.svg)](https://pypi.org/project/local-compose) -->


## Supported versions

Python:
- CPython >= 2.7

OS:
- Linux
- MacOS


## Install

Install from sources:
```bash
# Clone from git
git clone git@github.com:kolotaev/local-compose.git
# Or download any released version from github releases
wget https://github.com/kolotaev/local-compose/archive/{$RELEASE_VERSION}.tar.gz
tar -zxvf {$RELEASE_VERSION}.tar.gz

alias local-compose="python `pwd`/local-compose-{$RELEASE_VERSION}/main.py"
```
