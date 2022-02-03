from setuptools import setup

setup(
    name='butter',
    version='0.1.0',
    py_modules=[
        'src/butter',
        'src/inventory/inventory',
        'src/inventory/database'
    ],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'butter = src.butter:cli',
        ],
    },
)
