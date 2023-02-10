#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <f@fybx.dev>, 2023
#
import os
import shlex
from subprocess import run
import sys
from datetime import datetime as dt
from termcolor import colored, cprint

# Modify SETTINGS dictionary to set runtime variables
# Access values in dictionary using pre-defined names
SETTINGS = {
    'URL_REPO': 'https://github.com/fybx/dotfiles',         # remote repository URL
    'SHN_REPO': 'fybx/dotfiles'                             # remote shortname
    'DIR_REPO': '$HOME/repos/dotfiles',                     # local repository directory
    'DIR_CONF': '$HOME/.config',                            # local .config directory
    'F_DEPLOY': '$HOME/.config/dotman/deploy_list.json',    # path to deploy_list.json file
}

WHEREAMI = '$HOME/scripts'
VER = 'v1.8'
WER = 'v1.1'
help_message = f'''
dotman {VER} dotfiles manager by ferityigitbalaban

Unrecognized keys are ignored. If every key supplied is unrecognized,
this have the same effect as calling dotman without any key.
 
Keys:
-i, --interactive       Interactively backup or deploy dotfiles. Not supplying any key will result in interactive mode.
-s, --setup-dotman      Interactively set variables (DOTFILES_REPOSITORY, LOCAL_CONFIG, etc.) for your dotman setup.
-b, --backup            Backup your dotfiles. Doesn't require user assistance but errors may occur.
-d, --deploy            Deploy your dotfiles. Doesn't require user assistance but errors may occur.
-v, --version           Shows the version and quits
-h, --help              Shows this message and quits
'''


DL_FILES = []
DL_DIRS = []


def get_nth_key(n: int, d: dict[str, str]):
    c = 0
    for k in d.keys():
        if n == c:
            return k
        c += 1


def read_file(path: str):
    with open(path, 'r') as f:
        content = f.readlines()
        f.close()
    return content


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


def rrem(text: str, char: str):
    """
    Remove characters from right until character supplied with char
    :param text: Where to remove characters from
    :param char: Which character to stop removing at
    :return: Returns text with all characters until specified character removed
    """
    iterator = len(text) - 1
    buffer = ''
    while text[iterator] != char:
        buffer += text[iterator]
        iterator -= 1
    return text.removesuffix(buffer[::-1])


def proc(command, cwd=''):
    if 'cp -av' in command:
        r = run(command, shell=True)
    else:
        if cwd == '':
            r = run(command, shell=True, capture_output=True, text=True)
        else:
            r = run(command, shell=True, capture_output=True, text=True, cwd=cwd)
    return r.returncode, str(r.stdout) + str(r.stderr)


def print_settings():
    count = 1
    for key, value in SETTINGS.items():
        print(f'{count}. {key}:{value}')
        count += 1


def grab_dotfiles():
    os.mkdir(rrem(SETTINGS['DOTFILES_REPOSITORY'], '/'))
    code, output = proc(f"git clone {SETTINGS['REMOTE_REPOSITORY']}", SETTINGS['DOTFILES_REPOSITORY'])
    return code == 0, code


def copy(source, dest):
    proc(f'cp -av {source} {dest}')


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
        'rofi',
        'xfce4',
        'navi',
        'gtk-4.0',
        'flameshot'
    ]
    dirs = os.listdir(source)
    selected_dirs = []
    for each_name in dirs:
        if each_name in whitelist:
            selected_dirs.append(f'{source}{each_name}' if source.endswith('/') else f'{source}/{each_name}')
    for directory in selected_dirs:
        copy(directory, dest)


def commit_then_push():
    # I forget checking out to main after testing on a seperate branch
    # Line below checks out for me every time it's run
    proc('/usr/bin/git checkout main', SETTINGS['DOTFILES_REPOSITORY'])
    proc('/usr/bin/git fetch', SETTINGS['DOTFILES_REPOSITORY'])
    proc('/usr/bin/git pull', SETTINGS['DOTFILES_REPOSITORY'])
    proc('/usr/bin/git add .', SETTINGS['DOTFILES_REPOSITORY'])
    date = dt.now().strftime('%d.%m.%Y %H.%M')
    _, output = proc(f'/usr/bin/git commit -m "dotman {date}"', SETTINGS['DOTFILES_REPOSITORY'])
    if 'nothing to commit' not in output:
        code, output = proc('/usr/bin/git push', SETTINGS['DOTFILES_REPOSITORY'])
        if code == 0:
            _, output = proc('/usr/bin/git log', SETTINGS['DOTFILES_REPOSITORY'])
            commit = output.split('\n')[0].replace('commit ', '')
            return 3, commit
        return 0, None if code == 0 else 2, None
    return 1, None


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


def deploy():
    """
    Kindly executes the steps to get a up-to-date local repository, 
    deploy (copy) files and directories to the local config directory.
    """
    if not os.path.exists(SETTINGS.DIR_REPO):
        r = SETTINGS.DIR_REPO
        r.removesuffix("/")[:r.removesuffix("/").rindex("/")]
        run(shlex.split(f"/usr/bin/git clone {SETTINGS[URL_REPO]}"), text=True, cwd=r)
    run(shlex.split("/usr/bin/git pull"), text=True, cwd=r)
    for file in DL_FILES:
        copy(files)
    for directory in DL_DIRS:
        copy(directory)


def expand_settings():
    """
    Expands variables used in SETTINGS
    """
    SETTINGS['DIR_REPO'] = os.path.expandvars(SETTINGS['DIR_REPO'])
    SETTINGS['DIR_CONF'] = os.path.expandvars(SETTINGS['DIR_CONF'])
    SETTINGS['F_DEPLOY'] = os.path.expandvars(SETTINGS['F_DEPLOY'])


def main():
    global WHEREAMI
    WHEREAMI = rrem(sys.argv[0], '/')
    expand_settings()

    exists_dir_repo = os.path.exists(SETTINGS['DIR_REPO'])

    flag_interactive = False
    flag_backup = False
    flag_deploy = False
    flag_setup = False
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
            flag_setup = flag_setup or key == '-s' or key == '--setup-dotman'
            flag_version = flag_version or key == '-v' or key == '--version'
            flag_help = flag_help or key == '-h' or key == '--help'
    else:
        flag_interactive = True

    if exists_dir_repo:
        # local repository directory exists. Backup or deploy is possible.
        if flag_interactive:
            # if interactive flag was fed, ignore backup and deploy key
            # ask user for action (backup or deploy) 
            while True:
                ans = input('(B)ackup or (D)eploy is possible, select one: ').lower()
                if ans == 'b' or ans == 'd':
                    break
            if ans = 'b':
                # interactive backup
            elif ans = 'd':
                # interactive deploy

        else:
            # continue according to set flag, XOR
            if flag_backup and not flag_deploy:
                # backup
            elif flag_deploy and not flag_backup:
                # deploy
            else:
                # either both flags are set OR both are unset
                exit(0)
    else:
        # local repository directory does not exist. Only deploy is possible.
        # if interactive, ask for deploy, else if deploy flag is set, deploy, otherwise quit.
        if flag_interactive:
            print(f"local repository directory for {SETTINGS.SHN_REPO} does not exist")
            print("You can clone and deploy this repository to local config directory")
            ans = input("Continue (y/N): ").lower()
            if ans == "n" and not ans == "y":
                exit(0)
            if not flag_interactive and not flag_deploy:
                exit(0)
            # run deploy

    # ^^^ new logic ^^^
    # 
    # vvv old logic vvv
    return

    if flag_interactive:
        print(f"dotman {VER} by ferityigitbalaban")
        if not local_repo_exists:
            print(colored('Important warning:', 'red'), 'dotfiles repository cannot be located at: ',
                  colored(SETTINGS['DOTFILES_REPOSITORY'], 'yellow'))
            print('Edit DOTFILES_REPOSITORY variable in this script to specify its location')
            print(f'To grab dotfiles from', colored(f'"{remote_shortname}"', 'yellow'), end='')
            ans = input('type Y. (y/N): ')
            if ans.lower() == 'y' or 'yes':
                grab_successed, exit_code = grab_dotfiles()
                if grab_successed:
                    print(f'Successfully grabbed dotfiles from', colored(f'"{remote_shortname}"', 'yellow'))
                else:
                    print(f'git exited with result code:', colored(str(exit_code), 'red'),
                          '. An error may have occured.')
                    exit(128)
            else:
                cprint('There isn\'t anything left for dotman to do. Have a nice day!', 'green')
                exit(0)
        print('dotman is', colored('ready', 'green'), 'for your command. ')
        print('You can either backup to remote, or copy local repo to local config (deploy)')
        ans = input('(B)ackup or (D)eploy: ')
        if ans.lower() == 'b' or ans.lower() == 'backup':
            print(colored('Step 1: ', 'magenta'), 'Copy from local config', colored(f"\"{SETTINGS['LOCAL_CONFIG']}\"", 'yellow'),
                  'to local repo', colored(f"\"{SETTINGS['DOTFILES_REPOSITORY']}\"", 'yellow'))
            special_copy(SETTINGS['LOCAL_CONFIG'], SETTINGS['DOTFILES_REPOSITORY'])
            print(colored('Step 2: ', 'magenta'), f'Create a commit and push to remote repo',
                  colored(f"\"{SETTINGS['REMOTE_REPOSITORY']}\"", 'yellow'))
            stat, _ = commit_then_push()
            if stat == 0:
                cprint('Backup completed. Have a nice day!', 'green')
            elif stat == 1:
                cprint('There was nothing to commit, aborting.', 'red')
            elif stat == 2:
                cprint('Couldn\'t push local to remote, aborting.', 'red')
            elif stat == 3:
                url = f"{SETTINGS['REMOTE_REPOSITORY']}/commit/{_}"
                cprint(f'Backup completed: {url}. Have a nice day!', 'green')
            exit(stat)
        elif ans.lower() == 'd' or ans.lower() == 'deploy':
            print(colored('Step 1:', 'magenta'), ' Copy from local repo to local config')
            special_copy(SETTINGS['DOTFILES_REPOSITORY'], SETTINGS['LOCAL_CONFIG'])
            cprint('Deploy completed. Have a nice day!', 'green')
            exit(0)
    elif flag_backup and not flag_deploy:
        if local_repo_exists:
            special_copy(SETTINGS['LOCAL_CONFIG'], SETTINGS['DOTFILES_REPOSITORY'])
            exit(commit_then_push())
        else:
            print(colored('[CRITICAL]', 'red'), 'Local repository couldn\'t be located. Aborting...')
            exit(128)
    elif flag_deploy and not flag_backup:
        if local_repo_exists:
            special_copy(SETTINGS['DOTFILES_REPOSITORY'], SETTINGS['LOCAL_CONFIG'])
            exit(0)
        else:
            print(colored('[CRITICAL]', 'red'), 'Local repository couldn\'t be located. Aborting...')
            exit(128)
    elif flag_setup:
        print(f'dotman interactive setup wizard {WER}')
        print_settings()
        ans = input('Edit settings (y/N): ')
        if ans.lower() == 'y' or ans.lower() == 'yes':
            print('Type in number of setting you wish to modify, and "e" or "exit" when done')
            while True:
                num = input('Input: ')
                if num.lower() == 'exit' or num.lower() == 'e':
                    break
                elif num.isnumeric() and 1 <= int(num) <= len(SETTINGS):
                    key = get_nth_key(int(num) - 1, SETTINGS)
                    SETTINGS[key] = input(f'Enter new value for {key}: ').strip()
            print('Saving changes to file')
            write_setup()

    elif flag_version:
        print(f'dotman version: {VER.removeprefix("v")}')
        exit(0)
    elif not flag_deploy and not flag_backup and not flag_interactive or flag_help:
        print(help_message)
        exit(0)


if __name__ == '__main__':
    main()

