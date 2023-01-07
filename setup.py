from setuptools import setup, find_packages

required = []
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='lazywp',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    entry_points={
        'console_scripts': [
            'lazywp = main:cli',
        ],
    },
)
