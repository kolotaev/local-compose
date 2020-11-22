from os import path
from setuptools import setup, find_packages


about = {}
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'compose', 'info.py'), mode='r') as f:
    exec(f.read(), about)


if __name__ == '__main__':
    setup(
        name=about['name'],
        description='Like docker-compose but for locally installed services',
        # keywords='',
        version=about['version'],
        author='Egor Kolotaev',
        author_email='ekolotaev@gmail.com',
        license='MIT',
        url='http://github.com/kolotaev/local-compose',
        long_description='Like docker-compose but for locally installed services',
        entry_points={
            'console_scripts': [
                '%s = main:run' % about['name'],
            ],
        },
        py_modules=['app', 'main'],
        python_requires='>=2.7',
        install_requires=[
            # 'six~=1.15',
            'watchdog~=0.10',
            'jsonschema~=3.2',
            # 'delegator.py~=0.1',
            # 'colorama', # Colorama is only required for Windows
            'PyYAML~=5.3',
            'click~=7.0',
            # 'https://github.com/feluxe/sty'
        ],
        extras_require={
            'dev': [
                'pytest~=4.6',
            ],
        },
        # test_requirements = [],
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
            'Programming Language :: Python :: Implementation :: PyPy'
        ],
    )
