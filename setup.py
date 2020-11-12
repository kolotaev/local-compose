from setuptools import setup, find_packages


if __name__ == '__main__':
    setup(
        name='local-compose',
        description='Like docker-compose but for locally installed services',
        # keywords='',
        version='0.0.1',
        author='Egor Kolotaev',
        author_email='ekolotaev@gmail.com',
        license='MIT',
        # url='http://github.com/kolotaev/local-compose',
        long_description='Like docker-compose but for locally installed services',
        entry_points={
            'console_scripts': [
                'local-compose = main:run',
            ],
        },
        # py_modules=['app', 'resources', 'main'],
        # python_requires='>=3.6',
        # install_requires=[
        #     'google_speech',
        #     'googletrans',
        # ],
        extras_require={},
        packages=find_packages(exclude='tests'),
        classifiers=[],
    )
