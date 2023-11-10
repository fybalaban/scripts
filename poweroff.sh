#!/bin/bash
dt=$(date -Iseconds)
# unison=$($HOME/scripts/unison_sync.sh)
rm "$HOME/.cache/cliphist/db"
python "$HOME/scripts/resync_vault.py"
echo "[$dt] INFO: navi, powering off" >> navi.log
poweroff
