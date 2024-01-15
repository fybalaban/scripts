#!/usr/bin/bash
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       Select an area with slurp, ss with grim 
#       and copy to clipboard.
SS="/media/fyb/share/shoka/swap/screenshots"
grim -c -g "$( slurp )" - | wl-copy --type image/png && wl-paste > "$SS"/$( date +'%Y-%m-%d-%H%M%S.png' )
