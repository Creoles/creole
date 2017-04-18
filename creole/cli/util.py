# coding: utf-8
import os
from contextlib import contextmanager
from subprocess import check_output, check_call, CalledProcessError


@contextmanager
def cd(dir_path):
    orig_dir = os.path.abspath('.')
    os.chdir(dir)
    yield
    os.chdir(orig_dir)


@contextmanager
def cd_root():
    """Change working dir to root of current git repo"""
    orig_dir = os.path.abspath('.')
    root = get_repo_root()
    os.chdir(root)
    yield
    os.chdir(orig_dir)


def get_repo_root():
    """Get root path of current working repo utilzing `git`"""
    return check_output(['git', 'rev-parse', '--show-toplevel']).strip()


def run(cmd, shell=False):
    """Run command, using :func:`~subprocess.check_call`. Won't raise
    :class:`~subprocess.CalledProcessError`, thus rely on the command's
    output and exit code to properly present the error.

    Args:
        cmd: A list of string, format is same as
             :func:`~subprocess.check_call`
        shell: Use shell to run the command, see doc of
               :func:`~subprocess.check_call` for the security concern

    Returns:
        An integer of the command's exit code
    """
    try:
        rv = check_call(cmd, shell=shell)
    except CalledProcessError as e:
        rv = e.returncode
    return rv
