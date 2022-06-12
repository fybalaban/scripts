#!/usr/bin/env bash
dt=$(date +'%d/%m/%y-%H.%M.%S')
echo "[$dt] navi restarting..." >> $HOME/navi.log
$HOME/scripts/modeset.py --shutdown
reboot
