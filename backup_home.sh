#!/usr/bin/env bash
#
#       Ferit Yiğit BALABAN <f@fybx.dev>, 2022
#
echo "Hello, $( whoami )"
echo "w/o Downloads: $( du -sh --exclude='Downloads' "$HOME" )"
echo "wth Downloads: $( du -sh "$HOME" )"
doas tar --exclude="$HOME/Downloads" --exclude="$HOME/.local/share/JetBrains" --exclude="$HOME/.cache/pip" --exclude="$HOME/.cache/yay" --exclude="$HOME/.cache/JetBrains" --exclude="$HOME/.nuget" --create --verbose --preserve-permissions --gzip --file "/home/ferit-$( date +'%y%m%d' ).tar.gz" /home/ferit
