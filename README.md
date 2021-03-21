
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
RELEASE_VERSION=X.Y.Z
wget https://github.com/kolotaev/local-compose/archive/${RELEASE_VERSION}.tar.gz

# Either install the package with pip
pip install ./${RELEASE_VERSION}.tar.gz

# Or install the package with setuptools
tar -zxvf ${RELEASE_VERSION}.tar.gz
python local-compose-${RELEASE_VERSION}/setup.py install
```

## Milestones

- [x] Configurable restarts for failed services/jobs
- [ ] Log output configuration
- [ ] Watch file changes a.k.a. dev-mode
- [x] Running `up` command with file / current working directory / defaults
- [x] Detached mode
- [x] More flexible ENV variables support (env-maps)
- [x] Env-files support, Env from OS
- [ ] Add docs
- [ ] Config files merge
- [ ] Configurable Cron restarts for services/jobs
