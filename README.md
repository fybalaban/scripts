## scripts

This repository contains Python and shell scripts that I actively develop and utilize on my GNU/Linux [(or as I've recently taken to calling it, GNU plus Linux)](https://balaban.software/tribute.html) machine.

### launch_searx.sh

starts a docker container for searx. use a cron job to execute this script on reboot.
> @reboot sh $HOME/scripts/launch_searx.sh

dependencies:
 - docker installation (do not use snap to install)

### pi & piw

ssh into my dear raspberry pi, static ip addresses change according to connection medium (lan vs wlan)

### volumeup.sh

used in i3wm to set maximum volume level. calling this script increases current volume level by 5%
change the number in condition part of script ($current -lt 200) to set the upper limit

used by:
 - i3wm configuration

dependencies:
 - pactl
 - pulseaudio (?)

### update_repos.py

updates repositories kept in $HOME/sources by calling 'git pull' using subprocess

dependencies:
 - [termcolor](https://pypi.org/project/termcolor)

### launch_polybar.sh

used by i3wm to launch polybar on occasions. ripped it off from arch wiki ;)

used by:
 - i3wm configuration
 - [source_polybar.py](https://github.com/fybalaban/scripts#source_polybarpy)

dependencies:
 - [polybar](https://github.com/polybar/polybar)

### source_polybar.py

generates and deploys my polybar configuration with color parameters. significantly reduces the time it takes to change colors.

dependencies:
 - [launch_polybar.sh](https://github.com/fybalaban/scripts#launch_polybarsh)
 - [polybar](https://github.com/polybar/polybar) (I mean how can you use this config without polybar?)

### launch_compton.sh

restarting i3 using $mod+shift+r causes multiple instances of compton to be created :) i noticed that when the CPU temperature hit 85 degrees :) never doing that again :)

dependencies:
 - [compton](https://github.com/chjj/compton)
