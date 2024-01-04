#!/usr/bin/env bash
#
#       Ferit Yiğit BALABAN <fybalaban@fybx.dev>, 2023
#
EXCLUDE_FILE="$HOME/.backupexclude"
FILE="$HOME-$( date +'%y%m%d' ).tar.gz"
USER="$( whoami )"

echo "Hello, $USER"
echo "with excluded folders: $( du -sh --exclude-from="$EXCLUDE_FILE" "$HOME" )"
echo "with everything      : $( du -sh "$HOME" )"
echo "file will be saved as $FILE"

sudo tar --exclude-from="$EXCLUDE_FILE" \
  --create --verbose --preserve-permissions \
  --gzip --file "$FILE" "$HOME"

sudo chown "$USER":"$USER" "$FILE"

