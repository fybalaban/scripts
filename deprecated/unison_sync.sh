#!/bin/bash
#
#       Ferit Yiğit BALABAN <fybalaban@fybx.dev>, 2023
#       & ChatGPT
#

LOCAL_DIR="$HOME/mounts/31_shoka"
REMOTE_DIR="ssh://fyb@192.168.0.3//mnt/shoka"
LOG_FILE="$HOME/navi.log"
UNISON="/usr/bin/unison"

# Run Unison to synchronize the directories
$UNISON $LOCAL_DIR $REMOTE_DIR -batch -auto -confirmbigdel > /dev/null 2>&1

# Check the exit code of Unison
if [ $? -eq 0 ]; then
  # Synchronization was successful, log the message and exit
  echo "$(date -Iseconds) INFO: unison, sync successful" >> $LOG_FILE
  exit 0
else
  # Synchronization failed, check if there were conflicts
  CONFLICTS=`grep "Conflicting file" /var/log/unison.log | wc -l`
  if [ $CONFLICTS -eq 0 ]; then
    # There were no conflicts, log the message and exit
    echo "$(date -Iseconds) INFO: unison, no diff" >> $LOG_FILE
    exit 0
  else
    # There were conflicts, log the message and exit with an error code
    echo "$(date -Iseconds) ERROR: unison, sync conflict" >> $LOG_FILE
    exit 1
  fi
fi
