#!/usr/bin/env python
from setuptools import setup

__version__ = ''
exec(open('src/pubic/_version.py').read())

with open("requirements.txt") as f:
    required = [l for l in f.read().splitlines() if not l.startswith("#")]

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='pubic',
    version=__version__,
    description='A terminal-based GUI client for Git',
    long_description=long_description,
    keywords='git, client, terminal, console',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Topic :: System :: Archiving',
        'Topic :: System :: Backup',
        'Topic :: System :: Mirroring',
        'Topic :: Utilities',
        ],
    author='Tim Legrand',
    author_email='timlegrand.perso+dev@gmail.com',
    url='https://github.com/timlegrand/pubic',
    download_url='https://github.com/timlegrand/pubic',
    license='BSD 2-Clause',
    packages=['pubic'],
    package_dir={'': 'src'},
    install_requires=required,
    entry_points={'console_scripts': ['pubic = pubic.pubic:_main']},
    )
