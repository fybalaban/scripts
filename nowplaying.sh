#!/bin/bash
stat=$( playerctl status )
msg=$( playerctl -f '{{trunc(xesam:artist, 15)}} - {{trunc(xesam:title, 30)}}' metadata )
if [ "$stat" = "Playing" ]; then
    if [ "$msg" = " - " ]; then
        echo "No metadata"
    else
        echo "$msg"
    fi
else
    if [ "$stat" = "Paused" ]; then
        echo "Paused"
    else
        echo ""
    fi
fi
exit 0
