#!/bin/bash
dt=$(date +'%d/%m/%y-%H.%M.%S')
echo "[$dt] navi shutting down..." >> navi.log
$HOME/scripts/modeset.py --shutdown
shutdown -h now
