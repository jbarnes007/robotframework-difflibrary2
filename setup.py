from setuptools import setup
from os.path import join, dirname

execfile(join(dirname(__file__), 'DiffLibrary2', 'version.py'))


setup(
    name='robotframework-DiffLibrary2',
    version=VERSION,
    author='Jules Barnes',
    author_email='jules@julesbarnes.com',
    packages=['DiffLibrary2', 'DiffLibrary2.test'],
    package_data = {'difflibrary2': ['bin/*.*']},
    url='https://code.google.com/p/robotframework-DiffLibrary2/',
    license='LICENSE.txt',
    description='Robot Framework keyword library that will provide Diff capabilities',
    long_description=open('README.txt').read(),
    install_requires=[
                      'robotframework >= 2.8.3',
                      ],
)