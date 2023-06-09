from setuptools import setup

setup(
    name='tdcreate',
    version='0.1.0',
    description='A better template format for todoist projects',
    author='Joel Carranza',
    author_email='joel@joelcarranza.com',
    url='https://github.com/joelcarranza/tdcreate',
    packages=['tdcreate'],
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'tdcreate = tdcreate.cli:main',
        ]
    },
)