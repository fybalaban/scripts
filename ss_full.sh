#!/usr/bin/bash
#
# 1. take the screenshot of all displays with cursor visible (-c)
# and print to stdout (-)
# 2. the data printed to stdout is piped to wl-copy and it's copied
# 3. the data is pasted to a file in folder $SS
SS="/media/fyb/share/shoka/swap/screenshots"
grim -c - | wl-copy --type image/png && wl-paste > "$SS"/$( date +'%Y-%m-%d-%H%M%S.png' )
