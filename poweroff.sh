#!/bin/bash
dt=$(date -Iseconds)
unison=$($HOME/scripts/unison_sync.sh)
rm "$HOME/.cache/cliphist/db"
echo "[$dt] INFO: navi, powering off" >> navi.log
poweroff
