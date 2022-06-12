#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fyb@duck.com>, 2022
#
import os
import subprocess
from termcolor import colored


def main():
    print(colored('UwU Hewwo goowd siw! I wiww upwate youw wepos :3', 'magenta'))
    print('You smelly self compiling narcissist~ OwO')

    # change folder name below if you keep your repos in a different place
    path_to_folders = os.environ['HOME'] + '/sources/'

    list_of_folders = [d for d in os.listdir(path_to_folders) if os.path.isdir(os.path.join(path_to_folders, d))]
    print('Found folders ', colored(f'{list_of_folders}', 'green'), ' in ', colored(f'{path_to_folders}', 'green'))

    # append base directory to subdirectory names
    for i in range(len(list_of_folders)):
        list_of_folders[i] = path_to_folders + list_of_folders[i]

    # list repos (folders that have '.git' as a subfolder)
    list_of_repos = [d for d in list_of_folders if '.git' in os.listdir(d)]
    print('Found repos ', colored(f'{list_of_repos}', 'yellow'))

    # call git in every repository
    i = 1
    for repo in list_of_repos:
        print(colored(f'\n[{i}/{len(list_of_repos)}]', 'magenta'), 'Calling "git pull" in', colored(f'{repo}:', 'blue'))
        process = subprocess.Popen(['git', 'pull'], cwd=repo)
        output = process.communicate()[0]
        i += 1

    print(f'\nOwO {len(list_of_repos)} tasks compweted successfuwwy')


if __name__ == '__main__':
    main()

