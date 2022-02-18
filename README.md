
[![Build](https://github.com/kolotaev/local-compose/workflows/Tests/badge.svg?branch=master)](https://github.com/kolotaev/local-compose/actions)
[![Coverage](https://codecov.io/github/kolotaev/local-compose/coverage.svg?branch=master)](https://codecov.io/github/kolotaev/local-compose?branch=master)
<!-- [![Supported Versions](https://img.shields.io/pypi/pyversions/local-compose.svg)](https://pypi.org/project/local-compose) -->

> Like docker-compose, but for locally installed executables.


## Rationale

For some environments (especially development) it's quite tedious to use containerization (e.g. docker) all the time. Nowadays microservices development has become ubiquitous and when you need to run application as a whole you'll likely end up with a bunch of services running. From the other hand, while developing services you already likely have all the execution environment(s) for your services installed on the host OS (to run REPL, unit tests, etc. right?). This tool tries to build a bridge between declarative definition of your services (akin docker-compose) and running them on the host OS. Some might argue, that it doesn't conform to the principle of a uniform environment, and that's true, but you don't always need that, so having a choice is always a good thing.


## Supported versions

Python:
- CPython >= 2.7

OS:
- Linux
- MacOS
- If you use local-compose on Windows and have issues with it, let us know. Currently we don't support this OS.


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


## Development

- Create a fork and lone the repository
- Make updates to the code
- Run `tox -e py27-test-all` # as an example, to run all tests against Python 2.7
- Commit changes
- Make a pull request
