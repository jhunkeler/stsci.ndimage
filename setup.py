#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

import os
from ConfigParser import ConfigParser

import pkg_resources


SETUP_REQUIRES = ['d2to1', 'stsci.distutils==0.2']


# This project requires utilities from the stsci.distutils package in order to
# build.  If stsci.distutils is not already installed, it may automatically be
# downloaded from PyPI.  However, in a full source distribution of
# stsci_python, it should also be available in a sibling directory to this one,
# so that should be used instead if possible.
for requirement in pkg_resources.parse_requirements(SETUP_REQUIRES):
    if requirement.project_name != 'stsci.distutils':
        continue

    try:
        # See if the required version of stsci.distutils is already available
        pkg_resources.get_distribution(requirement)
        has_stsci_distutils = True
    except (pkg_resources.VersionConflict,
            pkg_resources.DistributionNotFound):
        has_stsci_distutils = False

    if has_stsci_distutils:
        break

    tools_dir = os.path.join(os.path.pardir, 'distutils')
    setup_cfg = os.path.join(tools_dir, 'setup.cfg')
    if os.path.exists(setup_cfg):
        # Check the setup.cfg in ../distutils; make sure it is in fact for
        # stsci.distutils and that the version is as required
        cfg = ConfigParser()
        cfg.read(setup_cfg)
        if not cfg.has_option('metadata', 'name'):
            break
        name = cfg.get('metadata', 'name')
        if name != 'stsci.distutils':
            break
        if cfg.has_option('metadata', 'version'):
            version = cfg.get('metadata', 'version')
        else:
            version = None
        if version not in requirement:
            break

        # stsci.distutils will almost always have packages_root = lib, but
        # better not to make assumptions
        if cfg.has_option('files', 'packages_root'):
            location = os.path.join(tools_dir,
                                    cfg.get('files', 'packages_root'))
        else:
            location = tools_dir

        # If a different version of stsci.distutils is already in the current
        # distribution list, remove it and add a distribution pointing to our
        # source-local copy
        dist = pkg_resources.Distribution(
                location=location, project_name=name, version=version,
                precedence=pkg_resources.CHECKOUT_DIST)
        if name in pkg_resources.working_set.by_key:
            del pkg_resources.working_set.by_key[name]
        pkg_resources.working_set.add(dist)
    break


setup(
    setup_requires=SETUP_REQUIRES,
    d2to1=True,
    use_2to3=True
)
