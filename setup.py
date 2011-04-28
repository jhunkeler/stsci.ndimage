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


SETUP_REQUIRES = ['d2to1', 'stsci.tools==2.9']


# This project requires utilities from the stsci.tools package in order to
# build.  If stsci.tools is not already installed, it may automatically be
# downloaded from PyPI.  However, in a full source distribution of
# stsci_python, it should also be available in a sibling directory to this one,
# so that should be used instead if possible.
for requirement in pkg_resources.parse_requirements(SETUP_REQUIRES):
    if requirement.project_name != 'stsci.tools':
        continue

    try:
        # See if the required version of stsci.tools is already available
        pkg_resources.get_distribution(requirement)
        has_stsci_tools = True
    except (pkg_resources.VersionConflict,
            pkg_resources.DistributionNotFound):
        has_stsci_tools = False

    if has_stsci_tools:
        break

    tools_dir = os.path.join(os.path.pardir, 'tools')
    setup_cfg = os.path.join(tools_dir, 'setup.cfg')
    if os.path.exists(setup_cfg):
        # Check the setup.cfg in ../tools; make sure it is in fact for
        # stsci.tools and that the version is as required
        cfg = ConfigParser()
        cfg.read(setup_cfg)
        if not cfg.has_option('metadata', 'name'):
            break
        name = cfg.get('metadata', 'name')
        if name != 'stsci.tools':
            break
        if cfg.has_option('metadata', 'version'):
            version = cfg.get('metadata', 'version')
        else:
            version = None
        if version not in requirement:
            break

        # stsci.tools will almost always have packages_root = lib, but better
        # not to make assumptions
        if cfg.has_option('files', 'packages_root'):
            location = os.path.join(tools_dir,
                                    cfg.get('files', 'packages_root'))
        else:
            location = tools_dir

        # If a different version of stsci.tools is already in the current
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
