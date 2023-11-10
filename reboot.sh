#!/usr/bin/env bash
dt=$(date +'%d/%m/%y-%H.%M.%S')
rm "$HOME/.cache/cliphist/db"
python "$HOME/scripts/resync_vault.py"
echo "[$dt] navi restarting..." >> $HOME/navi.log
$HOME/scripts/modeset.py --shutdown
reboot
