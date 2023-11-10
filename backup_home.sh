#!/usr/bin/env bash
#
#       Ferit Yiğit BALABAN <fybalaban@fybx.dev>, 2023
#
EXCLUDE_FILE="$HOME/.backupexclude"

echo "Hello, $( whoami )"
echo "with excluded folders: $( du -sh --exclude-from="$EXCLUDE_FILE" "$HOME" )"
echo "with everything      : $( du -sh "$HOME" )"

sudo tar --exclude-from="$EXCLUDE_FILE" --create --verbose --preserve-permissions --gzip --file "$HOME-$( date +'%y%m%d' ).tar.gz" "$HOME"
