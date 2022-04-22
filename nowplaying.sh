#!/bin/bash
status=$( playerctl status )
if [ $? -eq 0 ]; then
    echo $( playerctl -f '{{trunc(xesam:artist, 20)}} - {{trunc(xesam:title, 30)}}' metadata )
else
    echo ""
fi
exit 0
