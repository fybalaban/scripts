## scripts

This repository contains Python and shell scripts that I actively develop and utilize on my GNU/Linux [(or as I've recently taken to calling it, GNU plus Linux)](https://fybx.dev/tribute.html) machine.

|          | Shell scripts | Python scripts |
| -------- | ------------- | -------------- |
| Obsolete | [launch_searx][searx], [pi & piw][pipiw], [launch_compton.sh][lc] | [update_repos.py][updrp] |
| Active   | [volumeup.sh][vup], [launch_picom.sh][lp], [launch_polybar][lp] | [source_polybar.py][sp], [compare.py][compy], [drun_cleaner.py][drunc], [dotman.py][dotman], [fetchpy][fetchpy] |

[searx]: https://github.com/fybx/scripts#launch_searxsh
[pipiw]: https://github.com/fybx/scripts#pi--piw
[vup]: https://github.com/fybx/scripts#volumeupsh
[updrp]: https://github.com/fybx/scripts#update_repospy
[lp]: https://github.com/fybx/scripts#launch_polybar
[sp]: https://github.com/fybx/scripts#source_polybar
[lc]: https://github.com/fybx/scripts#launch_comptonsh
[lp]: https://github.com/fybx/scripts#launch_picomsh
[fetchpy]: https://github.com/fybx/scripts#fetchpy
[dotman]: https://github.com/fybx/scripts#dotmanpy
[drunc]: https://github.com/fybx/scripts#drun_cleanerpy
[compy]: https://github.com/fybx/scripts#comparepy

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
 - pulseaudio

### update_repos.py

updates repositories kept in $HOME/sources by calling 'git pull' using subprocess

dependencies:
 - [termcolor](https://pypi.org/project/termcolor)

### launch_polybar

used by i3wm (or me) to launch polybar on occasions. this script first checks for polybar instances, and exits if there is any; however if no instances exist, a new polybar will pop up, *quietly*!

used by:
 - i3wm configuration
 - [source_polybar.py](https://github.com/fybalaban/scripts#source_polybarpy)

dependencies:
 - [fish](https://github.com/fish-shell/fish-shell) installation
 - [polybar](https://github.com/polybar/polybar)

### source_polybar.py

generates and deploys my polybar configuration with color parameters. significantly reduces the time it takes to change colors.

dependencies:
 - [launch_polybar.sh](https://github.com/fybalaban/scripts#launch_polybarsh)
 - [polybar](https://github.com/polybar/polybar) (I mean how can you use this config without polybar?)

### launch_compton.sh

restarting i3 using $mod+shift+r causes multiple instances of compton to be created :) I noticed that when the CPU temperature hit 85 degrees :) never doing that again :)

dependencies:
 - [compton](https://github.com/chjj/compton)

### launch_picom.sh

if there isn't any instance of picom running, creates one.

dependencies:
 - [picom](https://github.com/yshui/picom)

## fetchpy

fetchpy is an alternative to neofetch. I was tinkering around with my neofetch config file, and at some point I got frustrated enough to create a full-blown fetch script.

This took me approximately ~6 hours to complete, and I'm proud of it! (I drank too much mineral soda with extra citric acid, acid reflux is really getting wild lol)

Switched to rich from termcolor: fetchpy now features a damn crazy color palette and pride flags on Arch logo!

dependencies:
 - [rich](https://github.com/Textualize/rich)

## dotman.py

dotman is (yet) another DOTfiles MANager that ***I've*** made for ***my*** machine. 
 - Will it work on yours? Probably.
 - Do you really need it? Probably not.

### features of dotman

 - [x] Backup to any given local and remote repository
 - [x] Use whitelist to select folders
 - [x] Deploy to $HOME/.config
 - [x] Interactive mode
 - [x] Automatable mode 
 - [x] Verbose output
 - [ ] Logging capability

dependencies:
 - python installation lol
 - aw, hell nah. [termcolor](https://pypi.org/project/termcolor) again

## drun_cleaner.py

drun_cleaner is a necessary tool to make selected desktop entries hidden. it uses a hardcoded list to get which files you want to be hidden, then searchs for those files in certain locations like "/usr/share/applications" and "$HOME/.local/share/applications". a file, when found, will get appended with 'NoDisplay=true' which removes that entry from run, drun, or any app launcher's menu.

## compare.py

this tiny script reads two csv files to two lists, then compares the lists. what's so special about it? it takes phantombuster's Instagram follower and followee lists as inputs. :D.
