# coding: utf-8

#
# Use settings_fab_ENVIROMENT.ini to set the configurations
#
import os
from fabric.api import *
from fabric.utils import warn
from fabric.contrib.console import confirm


def _sudo_or_run(cmd):
    '''
    Switching between sudo() and run()
    '''
    if env.use_sudo.lower() == 'true':
        return sudo(cmd)
    else:
        return run(cmd)


def test():

    with prefix('source %s/bin/activate' % env.env_path):
        result = _sudo_or_run('python setup.py test')


def install_deps():

    cmd = 'pip install -r requirements.txt'

    with prefix('source %s/bin/activate' % env.env_path):
        result = _sudo_or_run(cmd)


def update_from_tag():
    '''
    This task try to apply the update from a specific tag and ensure using
    tag.
    '''

    _sudo_or_run('git fetch %s' % env.remote_source)

    _sudo_or_run('git tag -l')

    tag_name = prompt('Please specify tag: ')

    cmd = 'git checkout -f tags/%s -b %s' % (tag_name, tag_name)

    result = _sudo_or_run(cmd)

    if result.failed and 'already exists' in result:
        _sudo_or_run('git checkout %s' % tag_name)


def update_from_branch():
    '''
    This task try to apply the update from a specific `remote branch`
    parameter, rollback if any result return failed.
    '''

    _sudo_or_run('git stash')
    _sudo_or_run('git pull %s %s' % (env.remote_source, env.remote_branch))
    _sudo_or_run('git stash pop')


def update():
    '''
    Apply the update switching between tag or branch, asking for parameter
    ``remote_tag`` in settings_fab.ini file
    '''

    if not os.path.exists(env.rcfile):
        exit('set configuration file `-c` param ex.: fab -c settings_fab.ini, default path: $HOME/.fabricrc')

    if env.updated_by_tag.lower() == 'true':
        update_from_tag()
    else:
        update_from_branch()

    install_deps()

    test()
