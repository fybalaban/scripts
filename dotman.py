#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fyb@fybx.dev>, 2024
#
import os
import shlex
from subprocess import run
import sys

# Modify SETTINGS dictionary to set runtime variables
# Access values in dictionary using pre-defined names
SETTINGS = {
    'URL_REPO': 'https://github.com/fybx/dotfiles',         # remote repository URL
    'SHN_REPO': 'fybx/dotfiles',                            # remote shortname
    'DIR_REPO': '$HOME/shoka/300-399 repos/dotfiles',                     # local repository directory
    'DIR_CONF': '$HOME/.config',                            # local .config directory
    'F_DEPLOY': '$HOME/.config/dotman/deploy_list.json',    # path to deploy_list.json file
}

VER = 'v1.8'
help_message = f'''
dotman {VER} dotfiles manager by ferityigitbalaban

Unrecognized keys are ignored. If every key supplied is unrecognized,
this have the same effect as calling dotman without any key.
 
Keys:
-i, --interactive       Interactively backup or deploy dotfiles. Not supplying any key will result in interactive mode.
-b, --backup            Backup your dotfiles. Doesn't require user assistance but errors may occur.
-d, --deploy            Deploy your dotfiles. Doesn't require user assistance but errors may occur.
-v, --version           Shows the version and quits
-h, --help              Shows this message and quits
'''


DL_FILES = []
DL_DIRS = []


def read_deploy_list():
    """
    Reads file from SETTINGS.F_DEPLOY to get list of directories and files to deploy
    """
    path_deploy_list = SETTINGS['F_DEPLOY']
    if os.path.exists(path_deploy_list):
        with open(path_deploy_list, 'r') as f:
            file = f.read()
            f.close()
        dict_deploy_list = json.loads(file)
        DL_FILES = dict_deploy_list['files']
        DL_DIRS  = dict_deploy_list['dirs']
    else:
        create_deploy_list()


def create_deploy_list():
    """
    Creates the default deploy_list.json in path SETTINGS.F_DEPLOY
    """
    dl_default = {
            "files": [],
            "dirs": ["dotman"],
            }
    with open(SETTINGS['F_DEPLOY'], 'w') as f:
        f.write(json.dumps(dl_default, indent = 4))
        f.close()


def copy(source, dest, interactive=False):
    if interactive:
        run(shlex.split(f"cp -av {source} {dest}"))
        return
    run(shlex.split(f"cp -a {source} {dest}"))


def backup():
    """
    Aggresively executes the steps to do checksum comparisons between local
    config directory and local repository to decide which files to copy,
    copy only changed files, commit and push to remote.
    """
    # get list of files and directories to change (F_DEPLOY)
    # get list of checksums of (F_DEPLOY), compute and compare with local repository
    # if checksum(local_config) != checksum(local_repo)
        # copy local_config to local_repo
    # if exists(local_config in local_repo) is False
        # copy local_config to local_repo
    # if exists(F_DEPLOY) but not in local_config
        # warn for lost file, user must either copy from local_repo to local_config or delete from F_DEPLOY
    # exec git commit -m "[message]" && git push


def deploy(interactive=False):
    """
    Kindly executes the steps to get a up-to-date local repository, 
    deploy (copy) files and directories to the local config directory.
    """
    if not os.path.exists(SETTINGS.DIR_REPO):
        r = SETTINGS.DIR_REPO
        r.removesuffix("/")[:r.removesuffix("/").rindex("/")]
        if interactive:
            print(f"Local repository at {SETTINGS['DIR_REPO']} wasn't found. Cloning at {r}")
        run(shlex.split(f"/usr/bin/git clone {SETTINGS[URL_REPO]}"), text=True, cwd=r)
    if interactive:
        print("Pulling changes")
    run(shlex.split("/usr/bin/git pull"), text=True, cwd=r)
    for file in DL_FILES:
        copy(files, interactive=interactive)
    for directory in DL_DIRS:
        copy(directory, interactive=interactive)


def expand_settings():
    """
    Expands variables used in SETTINGS
    """
    SETTINGS['DIR_REPO'] = os.path.expandvars(SETTINGS['DIR_REPO'])
    SETTINGS['DIR_CONF'] = os.path.expandvars(SETTINGS['DIR_CONF'])
    SETTINGS['F_DEPLOY'] = os.path.expandvars(SETTINGS['F_DEPLOY'])


def main():
    expand_settings()

    exists_dir_repo = os.path.exists(SETTINGS['DIR_REPO'])

    flag_interactive = False
    flag_backup = False
    flag_deploy = False
    flag_version = False
    flag_help = False
    sys.argv.remove(sys.argv[0])
    sys.argv.reverse()
    if len(sys.argv) != 0:
        while len(sys.argv) > 0:
            key = sys.argv.pop()
            flag_interactive = flag_interactive or key == '-i' or key == '--interactive'
            flag_backup = flag_backup or key == '-b' or key == '--backup'
            flag_deploy = flag_deploy or key == '-d' or key == '--deploy'
            flag_version = flag_version or key == '-v' or key == '--version'
            flag_help = flag_help or key == '-h' or key == '--help'
    else:
        flag_interactive = True

    if exists_dir_repo:
        if flag_interactive: 
            while True:
                ans = input('(B)ackup or (D)eploy is possible, select one: ').lower()
                if ans == 'b' or ans == 'd':
                    break
            if ans == 'b':
                backup(flag_interactive)
            elif ans == 'd':
                deploy(flag_deploy)
        else:
            if flag_backup and not flag_deploy:
                backup(flag_interactive)
            elif flag_deploy and not flag_backup:
                deploy(flag_interactive)
            else:
                exit(0)
    else:
        if flag_interactive:
            print(f"local repository directory for {SETTINGS['SHN_REPO']} does not exist")
            print("You can clone and deploy this repository to local config directory")
            ans = input("Continue (y/N): ").lower()
            if ans == "n" and not ans == "y":
                exit(0)
            if not flag_interactive and not flag_deploy:
                exit(0)
            deploy(flag_interactive)


if __name__ == '__main__':
    main()

# Description
# dotman is a simple dotfiles manager that can be used to backup and deploy dotfiles.
# 
# It manages a git repository to deploy a list of files and directories to 
# the local .config directory. When the backup command is executed, it 
# copies the files and directories in the deploy_list.json to the 
# local repository. git is used to keep track of changes.
#
# Deploying a configuration is possible by either directly calling it, or
# by specifying a git tag. The tag is used to checkout the repository to a
# specific commit, and then deploy the configuration on that time.
# 
# Similar to deploying, backing up a configuration is possible by specifying
# a tag name. The tag is created after the files and directories are copied,
# essentially creating a snapshot of the configuration at that time.
