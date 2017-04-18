#!/usr/bin/env python
# coding: utf-8
"""
Usage:
    creole deploy <host>
    creole deploy <host> [--rev <rev-name>] [--remote-user <user>]
                         [--yes] [--verbose]
    creole deploy --install-ansible-roles [--verbose]
    creole deploy --help

Options:
  --rev <rev-name>                 Specify git revision name to deploy
  -u <user>, --remote-user <user>  Specify remote user to run the deploy
                                   task [default: deploy]
  --install-ansible-roles          Install required ansible roles
  -y, --yes                        Answer `yes` when prompted, useful for
                                   script automation
  -v, --verbose                    Make ouput more verbose
"""
import os
import tempfile
from sys import stdout

from docopt import docopt

from .util import run, cd, get_repo_root

ANSIBLE_DIR = os.path.join(get_repo_root(), 'ansible')

INSTALL_ANSIBLE_ROLES_YML = """\
- src: git+ssh://git@github.com/Creoles/ansible-role-creole.log.git
  name: creole.log
  version: master
- src: git+ssh://git@github.com/Creoles/ansible-role-creole.sync_code.git
  name: creole.sync_code
  version: master
- src: git+ssh://git@github.com/Creoles/ansible-role-creole.docker.git
  name: creole.docker
  version: master
- src: git+ssh://git@github.com/Creoles/ansible-role-creole.service.git
  name: creole.service
  version: master
"""


def install_ansible_roles(verbose=False):
    tmpfile = tempfile.NamedTemporaryFile(prefix='creole_deploy_roles-',
                                          suffix='.yml')
    if verbose:
        print 'temp file name:', tmpfile.name
    with tmpfile.file as f:
        f.write(INSTALL_ANSIBLE_ROLES_YML)
        f.flush()
        if verbose:
            print 'roles to be installed: \n', INSTALL_ANSIBLE_ROLES_YML
        return run(['ansible-galaxy', 'install', '--force', '-p', 'roles',
                    '-r', tmpfile.name])

DEPLOY_INFO_HEADER_TEMPLATE = """\
# Deploying creole service #
---
Hosts/Groups: {host}
Version: {revision}
ansible-playbook command to run: {cmd}
---
"""
CONFIRMATION = 'Confirm to proceed? [y/N] '

def _deploy(host, playbook, revision=None, remote_user=None,
            yes=False, verbose=False):
    cmd = ['ansible-playbook', '-l', host]
    if revision:
        cmd += ['-e', '"sync_code_git_revision={}"'.format(revision)]
    if remote_user:
        cmd += ['-u', remote_user]
    if verbose:
        cmd += ['-vvv']
    cmd.append(playbook)
    cmd = ' '.join(cmd)
    deploy_info_header = DEPLOY_INFO_HEADER_TEMPLATE.format(
        host=host, revision=revision, cmd=cmd)
    stdout.write(deploy_info_header)
    stdout.flush()

    if yes:
        return run(cmd, True)
    else:
        try:
            yorn = raw_input(CONFIRMATION)
        except BaseException:
            return
        if yorn == 'y':
            return run(cmd, True)


DEPLOY_PLAYBOOK = 'service.yml'


def deploy_service(service_host, revision=None, remote_user=None,
                   yes=None, verbose=None):
    return _deploy(host=service_host, revision=revision,
                   remote_user=remote_user, yes=yes,
                   verbose=verbose, playbook=DEPLOY_PLAYBOOK)


def main(argv=None):
    args = docopt(__doc__, argv=argv)
    with cd(ANSIBLE_DIR):
        if args['--install-ansible-roles']:
            return install_ansible_roles(args['--verbose'])
        else:
            return deploy_service(
                service_host=args['<host>'], revision=args['--rev'],
                remote_user=args['--remote-user'],
                yes=args['--yes'], verbose=args['--verbose'])
