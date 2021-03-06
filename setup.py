from setuptools import setup, find_packages
import versioneer
from edat.edat_cmd_class import Tox


def get_cmd_class():
    cmd_class = versioneer.get_cmdclass()
    cmd_class['test'] = Tox
    return cmd_class


setup(
    name='edat',
    version=versioneer.get_version(),
    tests_require=['tox'],
    cmdclass=get_cmd_class(),
    description='EDAT - Extensible Data Anonymization Tool',
    author='Sebastian Rodriguez, Gustavo Silva de Sousa',
    author_email='sebastianr213@gmail.com, gustavosilvadesousa@gmail.com',
    url='http://github.com/s-rodriguez/edat/',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    test_suite='edat.tests.test_edat',
    extras_require={
        'testing': ['pytest'],
    },
    # Para futuros entry points
    entry_points={
       'console_scripts': [
           'edat = edat:main',
           'edat_project = edat:create_project'
       ]
    },
)
