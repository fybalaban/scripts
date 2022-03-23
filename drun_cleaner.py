#!/usr/bin/env python3

# This script adds 'NoDisplay=true' to blacklisted application 
# desktop entries commonly found in /usr/share/applications 
# and $HOME/.local/share/applications.
#
# Ferit Yigit BALABAN <fyb@duck.com>, 2022

# Usage:
# This script will check append every filename in blacklist
# to every directory name in search_folders. Resulting paths
# will then be checked if they exist. Files that exist will
# get appended with 'NoDisplay=true'.
#
# Note: You can use environment variables in search_directories,
# but you mustn't use them in blacklist.
import os


def modify_file(path):
    with open(path, 'a') as stream:
        if 'NoDisplay=true' not in stream:
            stream.write('NoDisplay=true')
            return True
        else:
            return False


def main():
    blacklist = [
        'avahi-discover.desktop',
        'electron16.desktop',
        'bssh.desktop',
        'bvnc.desktop',
        'qv4l2.desktop',
        'qvidcap.desktop'
    ]

    search_directories = ['/usr/share/applications', '$HOME/.local/share/applications']
    search_directories = [os.path.expandvars(path) for path in search_directories]
    for directory in search_directories:
        for file in blacklist:
            if os.path.exists(directory + '/' + file):
                full_path = directory + '/' + file
                _ = modify_file(full_path)
                if _:
                    print(f'Appended "NoDisplay=true" 0 {full_path}')
                else:
                    print(f'File {full_path} already had "NoDisplay=true"')
    print('Reached end of combinations. Good bye!')


if __name__ == '__main__':
    main()
