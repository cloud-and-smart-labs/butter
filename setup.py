from setuptools import setup

setup(
    name='butter',
    version='0.0.1',
    description='SSH Client Utility tool',
    url='https://github.com/cloud-and-smart-labs/butter.git',
    license='Apache License 2.0',
    py_modules=[
        'src/butter',
        'src/inventory/inventory',
        'src/inventory/commands',
        'src/inventory/printer',
        'src/ssh/ssh',
        'src/ssh/commands',
        'src/ssh/printer'
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
