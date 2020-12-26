
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
# Set the release version you'd like
RELEASE_VERSION=0.2.1
wget https://github.com/kolotaev/local-compose/archive/${RELEASE_VERSION}.tar.gz

# Either install the package with pip
pip install ./${RELEASE_VERSION}.tar.gz

# Or install the package with setuptools
tar -zxvf ${RELEASE_VERSION}.tar.gz
python local-compose-${RELEASE_VERSION}/setup.py install
```
