#!/usr/bin/env python
import recon.release
from glob import glob
from numpy import get_include as np_include
from setuptools import setup, find_packages, Extension


version = recon.release.get_info()
recon.release.write_template(version, 'stsci/ndimage')

setup(
    name = 'stsci.ndimage',
    version = version.pep386,
    author = 'STScI',
    author_email = 'help@stsci.edu',
    description = 'Various functions for multi-dimensional image processing--fork of scipy.ndimage for use with stsci_python',
    url = 'https://github.com/spacetelescope/stsci.ndimage',
    classifiers = [
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires = [
        'nose',
        'numpy',
    ],
    packages = find_packages(),
    package_data = {
        '': ['LICENSE.txt'],
        'stsci/ndimage/test': ['*.png']
    },
    ext_modules=[
        Extension('stsci.ndimage._nd_image',
            glob("src/*.c"),
            include_dirs=[np_include()]),
    ],
)
