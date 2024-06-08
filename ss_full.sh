#!/usr/bin/bash
#
# 1. take the screenshot of all displays with cursor visible (-c)
# and print to stdout (-)
# 2. the data printed to stdout is piped to wl-copy and it's copied
# 3. the data is pasted to a file in folder $SS
SS="/media/yigid/share/shoka/photos/Screenshots"
TEMP_FILE="$HOME/temp_file"
ACTIVE_MON=$( hyprctl monitors -j | jq -r '.[] | select(.focused == true) | .name' )

grim -l 1 -o $ACTIVE_MON "$TEMP_FILE"

if [ $? -eq 0 ]; then
    wl-copy --type image/png < "$TEMP_FILE"
    wl-paste > "$SS"/$( date +'%Y-%m-%d-%H%M%S.png' )
    rm "$TEMP_FILE"
fi
