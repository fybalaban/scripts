#!/usr/bin/bash
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       Select an area with slurp, ss with grim 
#       and copy to clipboard.
SS="/media/fyb/share/shoka/swap/screenshots"
TEMP_FILE="$HOME/temporary_screenshot"

grim -c -g "$( slurp )" "$TEMP_FILE"

if [ $? -eq 0 ]; then
  wl-copy --type image/png < "$TEMP_FILE"
  wl-paste > "$SS/$( date +'%Y-%m-%d-%H%M%S.png' )" 
  rm "$TEMP_FILE"
fi

