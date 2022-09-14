#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <f@fybx.dev>, 2022
#
#
#       Description:
#
#       modeset.py is an wallpaper setting, volume and brightness controlling utility
#       aimed to be used by keyboard shortcuts.
#
#       Dependencies:
#
#       - brightnessctl
#       - pactl
#       - playerctl
#       - wal
#       - betterlockscreen
from datetime import datetime as dt
from subprocess import run, Popen, PIPE, DEVNULL
import shlex
import random
import sys
import os


START_NIGHT = "20.00"
START_DAY = "9.30"
PATH_SCPT_KEYBRD = "$HOME/scripts/keyboard"
PATH_SCPT_LOCKER = "$HOME/scripts/wait_unlock.sh"
PATH_RESC_VOLUME = "$HOME/.config/navi/volume"
PATH_RESC_KBDLGT = "$HOME/.config/navi/keyboard"
PATH_RESC_SCRLGT = "$HOME/.config/navi/screen"
PATH_RESC_LIGHTW = "$HOME/sources/wallpapers/light/"
PATH_RESC_DARKW = "$HOME/sources/wallpapers/dark/"
PATH_RESC_WALLPS = "$HOME/.config/navi/wallpapers"
PATH_RESC_LOCKWP = "$HOME/sources/wallpapers/dark/nbgqfu.jpg"
PATH_RESC_NAVILG = "$HOME/navi.log"
VAR_KBDNAME = "asus::kbd_backlight"


def set_brightness(device: int, value: int, save_state=False):
    state_kbdlgt = get_brightness(1)
    state_scrlgt = get_brightness(0)
    if value == -1:
        with open(os.path.expandvars(PATH_RESC_SCRLGT if device == 0 else PATH_RESC_KBDLGT), 'r') as f:
            value = int(f.read())
            f.close()
    command = f"brightnessctl set {value}%" if device == 0 else f"brightnessctl --device {VAR_KBDNAME} set {value}%"
    run_command(command)
    if save_state:
        with open(os.path.expandvars(PATH_RESC_SCRLGT if device == 0 else PATH_RESC_KBDLGT), 'w') as f:
            f.write(str(state_scrlgt if device == 0 else state_kbdlgt))
            f.close()


def connect_keyboard():
    run_command(f"bash {PATH_SCPT_KEYBRD}")


def set_volume(value: int, save_state=False):
    state = get_volume()
    if value == -1:
        with open(os.path.expandvars(PATH_RESC_VOLUME), 'r') as f:
            value = int(f.read())
            f.close()
    value = 100 if value > 100 else 0 if value < 0 else value
    run_command(f'pactl set-sink-volume @DEFAULT_SINK@ {value}%')
    if save_state:
        with open(os.path.expandvars(PATH_RESC_VOLUME), 'w') as f:
            f.write(str(state))
            f.close()


def set_mouse(value: int):
    if value == 1:
        run_command('rivalcfg --color=#F666F5 --light-effect=breath')
    elif value == 0:
        run_command('rivalcfg --color=#000000')
    elif value == 2:
        run_command('rivalcfg -p=1000 -s=1000 -S=500')


def run_command(cmd: str):
    Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)


def do_query(cmd: str):
    return run(shlex.split(cmd), text=True, capture_output=True).stdout


def change_wallpaper(mode: int, cringe=False):
    wallpaper = PATH_RESC_LIGHTW if mode == 0 else PATH_RESC_DARKW
    wallpaper += "/cringe" if cringe else ""
    run_command(f"wal --iterative -qe -i {wallpaper}")


def lock():
    Popen(["bash", PATH_SCPT_LOCKER])
    Popen(["betterlockscreen", "-l", '--off', '5'], stdout=DEVNULL)


def pause_media():
    run_command("playerctl pause")


def get_brightness(device: int):
    command = "brightnessctl" if device == 0 else f"brightnessctl --device {VAR_KBDNAME}"
    return int(do_query(command).split('(')[1].split(')')[0].replace('%', ''))


def get_volume():
    r = do_query("pactl list")
    for x in r.split("Sink #0")[1].split("Base Volume:")[0].split(' '):
        if '%' in x:
            return int(x.replace('%', ''))


def log(message: str):
    with open(PATH_RESC_NAVILG, 'a') as f:
        f.write(f"[{dt.now().strftime('%m/%d/%y-%H.%M.%S')}] {message}\n")
        f.close()


def get_hour():
    if 0 <= dt.now().minute <= 9:
        return f"{dt.now().hour}.0{dt.now().minute}"
    return f"{dt.now().hour}.{dt.now().minute}"


def get_hour_spec(hour_str=None):
    if hour_str is not None:
        return (int(hour_str.split('.')[0]) * 60) + int(hour_str.split('.')[0])
    return (dt.now().hour * 60) + dt.now().minute


def get_mode():
    low = get_hour_spec(START_DAY)
    now = get_hour_spec()
    hgh = get_hour_spec(START_NIGHT)
    return 0 if low <= now < hgh else 1


def expand_vars():
    global PATH_SCPT_KEYBRD
    global PATH_SCPT_LOCKER
    global PATH_RESC_VOLUME
    global PATH_RESC_KBDLGT
    global PATH_RESC_SCRLGT
    global PATH_RESC_LIGHTW
    global PATH_RESC_DARKW
    global PATH_RESC_WALLPS
    global PATH_RESC_NAVILG
    PATH_SCPT_KEYBRD = os.path.expandvars(PATH_SCPT_KEYBRD)
    PATH_SCPT_LOCKER = os.path.expandvars(PATH_SCPT_LOCKER)
    PATH_RESC_VOLUME = os.path.expandvars(PATH_RESC_VOLUME)
    PATH_RESC_KBDLGT = os.path.expandvars(PATH_RESC_KBDLGT)
    PATH_RESC_SCRLGT = os.path.expandvars(PATH_RESC_SCRLGT)
    PATH_RESC_LIGHTW = os.path.expandvars(PATH_RESC_LIGHTW)
    PATH_RESC_DARKW = os.path.expandvars(PATH_RESC_DARKW)
    PATH_RESC_WALLPS = os.path.expandvars(PATH_RESC_WALLPS)
    PATH_RESC_NAVILG = os.path.expandvars(PATH_RESC_NAVILG)


def main():
    sys.argv.remove(sys.argv[0])
    expand_vars()
    mode = 3 if "-dark" in sys.argv else (2 if "-light" in sys.argv else get_mode())
    if len(sys.argv) == 0:
        print("modeset by fyb")
        print(f"local machine time:  {get_hour()}")
        print(f"current mode is:     {'e' if mode==2 or mode==3 else ''}{mode-2}")
        print(f"current sink volume: {get_volume()}")
        exit(0)

    mode = (mode - 2) if (mode == 2 or mode == 3) else mode
    if sys.argv[0] == "--login":
        log("modeset started with \"--login\"")
        set_volume(0)
        if mode == 0:
            set_brightness(0, 70)
            set_brightness(1, 0)
        else:
            set_brightness(0, 40)
            set_brightness(1, 100)
        set_mouse(1)
        change_wallpaper(mode)
    elif sys.argv[0] == "--lock":
        log("modeset started with \"--lock\"")
        set_volume(0, save_state=True)
        set_brightness(0, 0, save_state=True)
        if mode == 1: 
            set_brightness(1, 0, save_state=True)
        else:
            set_brightness(1, 1, save_state=True)
        pause_media()
        set_mouse(0)
        lock()
    elif sys.argv[0] == "--unlock":
        log("modeset started with \"--unlock\"")
        set_volume(-1)
        set_brightness(0, -1)
        set_brightness(1, -1)
        set_mouse(1)
    elif sys.argv[0] == "--shutdown":
        log("modeset started with \"--shutdown\"")
        set_brightness(0, 50)
        set_brightness(1, 100)
    elif sys.argv[0] == "--wallc":
        log("modeset started with \"--wallc\"")
        change_wallpaper(mode, cringe=True)
    elif sys.argv[0] == "--wallp":
        log("modeset started with \"--wallp\"")
        change_wallpaper(mode)
    elif sys.argv[0] == "-setl":
        log("modeset started with \"-setl\"")
        run_command(f"betterlockscreen -u {PATH_RESC_LOCKWP}")
    exit(0)


if __name__ == '__main__':
    main()
