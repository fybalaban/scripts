#!/usr/bin/env bash
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       Select an area with slurp, ss with grim 
#       and copy to clipboard.
SS="$HOME/shoka/swap/screenshots"
grim -g "$( slurp )" - | wl-copy --type image/png && wl-paste > "$SS"/$( date +'%Y-%m-%d-%H%M%S.png' )
