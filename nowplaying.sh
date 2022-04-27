#!/bin/bash
s=$( playerctl -f '{{trunc(xesam:artist, 20)}} - {{trunc(xesam:title, 30)}}' metadata )
if [ $? -eq 0 ]; then
    echo "$s"
else
    echo ""
fi
exit 0
