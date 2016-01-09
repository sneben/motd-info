from pybuilder.core import use_plugin, init, task, depends, Author

use_plugin('python.core')
use_plugin('python.unittest')
use_plugin('python.install_dependencies')
use_plugin('python.flake8')
use_plugin('python.coverage')
use_plugin('python.distutils')


name = 'motd-info'
summary = 'Generate infos for displaying in addition to the motd'
description = """Python module for enhancing the output of the motd.
Several info types are available for display (ram, disk, users)."""
license = 'Apache License 2.0'
authors = [Author('Stefan Neben', 'stefan.neben@mailfoo.net')]
url = 'https://github.com/sneben/motd-info'
version = '0.1'
default_task = ['clean', 'analyze', 'package']


@init
def set_properties(project):
    project.build_depends_on('unittest2')
    project.build_depends_on('mock')
    project.depends_on('psutil')


@task
@depends('prepare')
def build_directory(project):
    print project.expand_path("$dir_dist")
