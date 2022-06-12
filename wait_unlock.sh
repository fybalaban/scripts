#!/usr/bin/env bash
#
#       Ferit Yiğit BALABAN <f@fybx.dev>, 2022
#
sleep 5
while : ; do
    if pgrep -x "i3lock" > /dev/null
    then
        sleep 5
    else
        python $HOME/scripts/modeset2.py --unlock
        break
    fi
done
