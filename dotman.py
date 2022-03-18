#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fyb@duck.com>, 2022
#
import os.path
import subprocess as sp
import sys
from datetime import datetime as dt


DOTFILES_REPOSITORY = '$HOME/repos/dotfiles'
REMOTE_REPOSITORY = 'https://github.com/fybalaban/dotfiles'
LOCAL_CONFIG = '$HOME/.config'
VER = 'v1.1'
help_message = f'''
dotman {VER} dotfiles manager by fyb

Unrecognized keys are ignored. If every key supplied is unrecognized,
this have the same effect as calling dotman without any key.
 
Keys:
-i, --interactive       Interactively backup or deploy dotfiles. Not supplying any key will result in interactive mode.
-b, --backup            Backup your dotfiles. Doesn't require user assistance but errors may occur.
-d, --deploy            Deploy your dotfiles. Doesn't require user assistance but errors may occur.
-v, --version           Shows the version and quits
-h, --help              Shows this message and quits
'''


def remove_from_left_until_slash(text):
    iterator = len(text) - 1
    buffer = ''
    while text[iterator] != '/':
        buffer += text[iterator]
        iterator -= 1
    return text.removesuffix(buffer[::-1])


def grab_dotfiles():
    os.mkdir(remove_from_left_until_slash(DOTFILES_REPOSITORY))
    p = sp.Popen(['git', 'clone https://github.com/fybalaban/dotfiles'], cwd=DOTFILES_REPOSITORY)
    _ = p.communicate()[0]
    return p.returncode == 0, p.returncode


def copy(source, dest, method='subprocess'):
    if method == 'subprocess':
        p = sp.Popen(['cp', '-av', source, dest])
        _ = p.communicate()[0]


def special_copy(source, dest):
    whitelist = [
        'fish',
        'gtk-2.0',
        'gtk-3.0',
        'htop',
        'i3',
        'kitty',
        'neofetch',
        'nitrogen',
        'picom',
        'polybar',
        'rofi'
    ]
    dirs = os.listdir(source)
    full_dirs = []
    for each_name in dirs:
        if each_name not in whitelist:
            dirs.remove(each_name)
        elif source.endswith('/'):
            full_dirs.append(source + each_name)
        else:
            full_dirs.append(source + '/' + each_name)
    for directory in full_dirs:
        copy(directory, dest, 'subprocess')


def git_commit():
    p1 = sp.Popen(['/usr/bin/git', 'add', '.'], cwd=DOTFILES_REPOSITORY)
    _ = p1.communicate()[0]

    date = dt.now().strftime('%d.%m.%Y %H.%M')
    commit_name = f'"dotman {date}"'
    p2 = sp.Popen(['/usr/bin/git', 'commit', '-m', commit_name], cwd=DOTFILES_REPOSITORY)
    _ = p2.communicate()[0]


def push_remote():
    p = sp.Popen(['/usr/bin/git', 'push'], cwd=DOTFILES_REPOSITORY)
    _ = p.communicate()[0]
    return p.returncode == 0, p.returncode


def main():
    global DOTFILES_REPOSITORY
    global LOCAL_CONFIG
    DOTFILES_REPOSITORY = os.path.expandvars(DOTFILES_REPOSITORY)
    LOCAL_CONFIG = os.path.expandvars(LOCAL_CONFIG)
    remote_shortname = REMOTE_REPOSITORY.removeprefix("https://github.com/")

    local_repo_exists = os.path.exists(DOTFILES_REPOSITORY)

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

    if flag_interactive:
        print(f"dotman {VER} by fyb, 2022")
        if not local_repo_exists:
            print(f'Important warning: dotfiles repository cannot be located at: {DOTFILES_REPOSITORY}')
            print('Edit DOTFILES_REPOSITORY variable in this script to specify its location')
            ans = input(f'If you want to use this script to grab dotfiles from {remote_shortname}, type Y. (y/N): ')
            if ans.lower() == 'y' or 'yes':
                grab_successed, exit_code = grab_dotfiles()
                if grab_successed:
                    print(f'Successfully grabbed dotfiles from {remote_shortname}')
                else:
                    print(f'git exited with result code: {exit_code}. An error may have occured.')
                    exit(128)
            else:
                print('There isn\'t anything left for dotman to do. Have a nice day!')
                exit(0)
        print('dotman is ready for your command. ')
        print('You can either backup to remote, or copy local repo to local config (deploy)')
        ans = input('(B)ackup or (D)eploy: ')
        if ans.lower() == 'b' or ans.lower() == 'backup':
            print(f'Step 1: Copy from local config {LOCAL_CONFIG} to local repo {DOTFILES_REPOSITORY}')
            special_copy(LOCAL_CONFIG, DOTFILES_REPOSITORY)
            print(f'Step 2: Create a commit and push to remote repo {REMOTE_REPOSITORY}')
            git_commit()
            push_remote()
            print('Backup completed. Have a nice day!')
            exit(0)
        elif ans.lower() == 'd' or ans.lower() == 'deploy':
            print(f'Step 1: Copy from local repo to local config')
            special_copy(DOTFILES_REPOSITORY, LOCAL_CONFIG)
            print('Deploy completed. Have a nice day!')
            exit(0)
    elif flag_backup and not flag_deploy:
        if local_repo_exists:
            special_copy(LOCAL_CONFIG, DOTFILES_REPOSITORY)
            git_commit()
            push_remote()
            exit(0)
        else:
            print('[CRITICAL] Local repository couldn\'t be located. Aborting...')
            exit(128)
    elif flag_deploy and not flag_backup:
        if local_repo_exists:
            special_copy(DOTFILES_REPOSITORY, LOCAL_CONFIG)
            exit(0)
        else:
            print('[CRITICAL] Local repository couldn\'t be located. Aborting...')
            exit(128)
    elif flag_version:
        print(f'dotman version: {VER.removeprefix("v")}')
        exit(0)
    elif not flag_deploy and not flag_backup and not flag_interactive or flag_help:
        print(help_message)
        exit(0)


if __name__ == '__main__':
    main()
