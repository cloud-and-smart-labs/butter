from setuptools import setup

setup(
    name='butter',
    version='0.1.0',
    py_modules=[
        'src/butter',
        'src/inventory/inventory',
        'src/inventory/database',
        'src/ssh'
    ],
    install_requires=[
        'Click',
        'paramiko'
    ],
    entry_points={
        'console_scripts': [
            'butter = src.butter:cli',
            'bx = src.butter:execute_shell'
        ],
    },
)
