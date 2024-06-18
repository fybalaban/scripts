#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fyb@fybx.dev>, 2024
#

# Description
# dotman is a simple dotfiles manager that can be used to backup and deploy dotfiles.
# 
# It manages a git repository to deploy a list of files and directories to 
# the local .config directory. When the backup command is executed, it 
# copies the files and directories in the deploy_list to the 
# local repository. git is used to keep track of changes.
#
# Deploying a configuration is possible by either directly calling it, or
# by specifying a git tag. The tag is used to checkout the repository to a
# specific commit, and then deploy the configuration on that time.
# 
# Similar to deploying, backing up a configuration is possible by specifying
# a tag name. The tag is created after the files and directories are copied,
# essentially creating a snapshot of the configuration at that time.

# Details
# * The configuration file for dotman is searched in    $HOME/dotman/config
# * The repository managed by dotman is searched in     $HOME/dotman/managed_repo
# * The deploy list for selecting what and what not 
#   to backup/deploy is searched in                     $HOME/dotman/deploy_list


import os
import shutil
import tomllib
import sys

from git.repo import Repo
from crispy.crispy import Crispy


VER = 'v1.8'
help_message = f'''
dotman {VER} dotfiles manager by ferityigitbalaban

Unrecognized keys are ignored. If every key supplied is unrecognized,
this have the same effect as calling dotman without any key.
 
Keys:
-b, --backup            Backup your dotfiles. Doesn't require user assistance but errors may occur.
-d, --deploy            Deploy your dotfiles. Doesn't require user assistance but errors may occur.
-v, --version           Shows the version and quits
-h, --help              Shows this message and quits
'''


dir_home = os.path.expandvars('$HOME')
dir_config = os.path.join(dir_home, '.config')
params = {}
list_ignore = []
list_deploy = []


def util_get_all_files(directory: str) -> list[str]:
    if not os.path.exists(directory):
        return []

    files = []
    for root, _, filenames in os.walk(directory):
        files.extend(os.path.join(root, filename) for filename in filenames)
    return files


def util_errout(msg: str, code: int):
    print(msg)
    sys.exit(code)


def task_init():
    global params
    params = {
        'managed_repo': f'{dir_config}/dotman/managed_repo',
        'deploy_list': f'{dir_config}/dotman/deploy_list',
        'config_file': f'{dir_config}/dotman/config',
        'repo_url': '',
    }


def task_config():
    """Reads and parses the configuration file
    """
    with open(params['config_file'], 'rb') as f:
        conf = tomllib.load(f)
    
    if 'repo_url' not in conf.keys():
        util_errout(f'[ERR] expected "repo_url" in {params["config_file"]}', 1)
    
    params['repo_url'] = conf['repo_url']


def task_repo():
    is_repo = os.path.exists(f"{params['managed_repo']}/.git")
    
    if not is_repo:
        Repo.clone_from(params['repo_url'], params['managed_repo'])
    else:
        repo = Repo(params['managed_repo'])
        repo.remotes.origin.pull()


def task_list():
    with open(params['deploy_list'], 'r') as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        lines = [l for l in lines if l]
    
    for line in lines:
        ignore_it = False
        if line.startswith('#'):
            continue
        if line.startswith('!'):
            ignore_it = True
            line = line.removeprefix('!')
        if line.startswith('%'):
            line = os.path.join(dir_config, line.replace('%', ''))
        else:
            line = os.path.join(dir_home, line)
        
        
        if os.path.isfile(line):
            if ignore_it:   list_ignore.append(line)
            else:           list_deploy.append(line)
        else:
            if ignore_it:   list_ignore.extend(util_get_all_files(line))
            else:           list_deploy.extend(util_get_all_files(line))
        
        for element in list_ignore:
            if element in list_deploy:
                list_deploy.remove(element)
    
    with open(f'{dir_home}/dotman.log', 'w') as f:
        f.writelines(map(lambda x: x + '\n', list_deploy))


def backup(tag=''):
    """Copies files and directories denoted in deploy_list from their source to
    managed_repo directory.

    Args:
        tag (str, optional): Git tag to publish for the commit. Defaults to ''.
    """
    for file in list_deploy:
        file_in_repo = util_path('backup', file)
        print(file_in_repo)
        os.makedirs(os.path.dirname(file_in_repo), exist_ok=True)
        shutil.copy(file, file_in_repo)
    
    repo = Repo(params['managed_repo'])
    repo.git.add(all=True)
    repo.git.commit('-m', 'committed by dotman')
    repo.remotes.origin.push()
    
    if tag != '':
        if tag in map(lambda x: x.replace('refs/tags/', ''), repo.tags):
            return
        created_tag = repo.create_tag(tag)
        repo.remotes.origin.push(created_tag.name)


def deploy(tag=''):
    """Copies files and directories in managed Git repository to 
    local .config directory, if they are present in the deploy list.
    
    Optinally, a tag can be specified to deploy a specific configuration.

    Args:
        tag (str, optional): Git tag for a specific configuration. Defaults to ''.
    """
    if tag != '':
        repo = Repo(params['managed_repo'])
        repo.git.checkout(tag)
        task_list()
    
    for file in list_deploy:
        file_in_repo = util_path('deploy', file)
        os.makedirs(os.path.dirname(file), exist_ok=True)
        shutil.copy(file_in_repo, file)


def util_path(mode, path):
    if mode == 'deploy':
        return os.path.join(params['managed_repo'], os.path.relpath(path, dir_home))
    elif mode == 'backup':
        return os.path.join(params['managed_repo'], os.path.relpath(path, dir_home))
    else:
        raise ValueError(mode)


def main():
    if len(sys.argv) == 1:
        print(help_message)
        sys.exit(0)
    
    task_init()
    task_config()
    task_repo()
    task_list()
    
    c = Crispy()
    c.add_variable('backup', bool)
    c.add_variable('deploy', bool)
    c.add_variable('tag', str)
    
    args = c.parse_arguments(sys.argv[1:])[1]

    if args['backup'] and args['deploy']:
        util_errout('[ERR] can\'t do both, sorry :(', 11)
    elif args['backup']:
        backup(args['tag'] if 'tag' in args.keys() else '')
    elif args['deploy']:
        deploy(args['tag'])


if __name__ == '__main__':
    main()

# Tasks
# 1. expand dir_config
# 2. read configuration file
# 3. check managed_repo status
#       1. create if necessary
#       2. or pull changes
# 4. read deploy_list

# command is deploy (tag?)
# 1. if tag is specified, checkout to that tag
# 2. copy files and directories in deploy_list (ask for using the same deploy_list) to local .config directory

# command is backup (tag?)
# 1. copy using deploy_list from sources to repository directory
# 2. create a new commit and push
# 3. if tag is specified, check if tag exists
#       1. if tag does not exist, create tag and push
#       2. if tag exists, warn and exit

