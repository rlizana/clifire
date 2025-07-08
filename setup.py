# setup.py (for compatibility with Python 3.6)
from setuptools import find_packages, setup

setup(
    name='clifire',
    version='0.1.8',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'jinja2',
        'pyyaml',
        'rich',
    ],
)
