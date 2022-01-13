## scripts

This repository contains scripts that I actively develop & use on my GNU/Linux machine.

### launch_searx.sh

create a cron job to execute this script.

dependencies:
 - sudo (i haven't tried it with doas yet)
 - docker installation (do not use snap)

### pi & piw

ssh into my dear raspberry pi, static ip's change according to connection medium (lan vs wlan)

### volumeup.sh

used in i3wm to set maximum volume level. calling this script increases current volume level by 5%
change the number in condition part of script ($current -lt 200) to set the maximum level

dependencies:
 - pactl
 - pulseaudio (?)
 - awk
 - sed

### update_repos.py

updates repositories kept in $HOME/sources by calling 'git pull' using subprocess

dependencies:
 - [termcolor](https://pypi.org/project/termcolor)

### launch_polybar.sh

used by i3wm to launch polybar on occasions. ripped it off from arch wiki ;)

dependencies:
 - [polybar](https://github.com/polybar/polybar)
