
from setuptools import setup
from os.path import join, dirname, abspath


def requirements():
    basedir = abspath(dirname(__file__))
    with open(join(basedir, 'requirements.txt')) as f:
        return f.read().splitlines()


setup(
    name='mazure',
    version='1.0.0',
    py_modules=['mazure'],
    include_package_data=True,
    install_requires=requirements(),
)