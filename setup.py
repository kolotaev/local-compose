from os import path
from setuptools import setup, find_packages


info = {}
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'compose', 'info.py'), mode='r') as f:
    exec(f.read(), info)


if __name__ == '__main__':
    setup(
        name=info['NAME'],
        description='Like docker-compose but for locally installed services',
        # keywords='',
        version=info['VERSION'],
        author='Egor Kolotaev',
        author_email='ekolotaev@gmail.com',
        license='MIT',
        url='http://github.com/kolotaev/local-compose',
        long_description='Like docker-compose but for locally installed services',
        entry_points={
            'console_scripts': [
                '%s = compose.main:execute' % info['NAME'],
            ],
        },
        python_requires='>=2.7',
        install_requires=[
            'watchdog~=0.10',
            'jsonschema~=3.2',
            'PyYAML~=5.3',
            'click~=7.0',
            'colored~=1.4',
            'python-dotenv~=0.15',
            # transitive dependencies fixes:
            'pyrsistent==0.16.0', # see https://github.com/Julian/jsonschema/issues/741
            "importlib_metadata~=2.0;python_version<'3.8'", # to fix issue with importlib_metadata>=3 on py2.7
        ],
        extras_require={
            'dev': [
                'pytest~=4.6',
                'mock==3.0.5',
                'pytest-cov'
            ],
        },
        packages=find_packages(exclude='tests'),
        classifiers=[
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'License :: OSI Approved :: MIT',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: Implementation :: CPython',
        ],
    )
