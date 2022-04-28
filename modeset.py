#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN, <fyb@duck.com>
#
#       modeset.py is a handy theme switcher for multiple applications.
from datetime import datetime
import os
import sys
from subprocess import run 


HOME_FOLDR = '/home/ferit'
PATH_LOGFL = f'{HOME_FOLDR}/navi.log'
DARK_THEME = f'Hardcore'
LGHT_THEME = f'Tango Light'
DARK_WLLPR = f'{HOME_FOLDR}/sources/wallpapers/6kkzj7.png'
LGHT_WLLPR = f'{HOME_FOLDR}/sources/wallpapers/5dd9v9.png'
DARK_FETCH = f'{HOME_FOLDR}/scripts/fetchdark.theme'
LGHT_FETCH = f'{HOME_FOLDR}/scripts/fetchlight.theme'
PATH_KITTY = f'{HOME_FOLDR}/.config/kitty/theme.conf'
PATH_FETCH = f'{HOME_FOLDR}/scripts/fetch.theme'
KBD_NAME = 'asus::kbd_backlight'


def write(status: str):
    log = f'[{datetime.now().strftime("%d/%m/%y-%H.%M.%S")}]'
    log += ' navi is going dark.\n' if status == 'dark' else ' navi is enlightened.\n'
    with open(PATH_LOGFL, 'a') as f:
        f.write(log)
        f.close()


def set_kbdlight(intensity: int):
    run(['brightnessctl', 'set', '--device', KBD_NAME, str(intensity)])


def set_wallpaper(wallpaper: str):
    run(['nitrogen', '--set-centered', wallpaper])    


def set_fetchpy(theme: str):
    try:
        os.remove(PATH_FETCH)
    except FileNotFoundError:
        pass
    os.symlink(theme, PATH_FETCH)


def set_kitty(theme: str):
    run(['kitty', '+kitten', 'themes', '--reload-in=all', theme])


def main():
    sys.argv.reverse()
    sys.argv.pop()
    if len(sys.argv) != 0:
        mode = sys.argv.pop()
        if mode == 'd' or mode == 'dark':
            set_kitty(DARK_THEME)
            set_wallpaper(DARK_WLLPR)
            set_fetchpy(DARK_FETCH)
            set_kbdlight(1)
            write('dark')
        elif mode == 'l' or mode == 'light':
            set_kitty(LGHT_THEME)
            set_wallpaper(LGHT_WLLPR)
            set_fetchpy(LGHT_FETCH)
            set_kbdlight(0)
            write('light')
        else:
            print("Error: expected d, dark, l or light as argument.")
            exit(1)
    exit(0)


if __name__ == '__main__':
    main()
