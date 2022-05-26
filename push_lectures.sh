#!/usr/bin/env bash
#
#       Ferit Yiğit BALABAN <f@fybx.dev>, 2022
#
#       Description
#       This script is used to push all changes in lecture notes folder to GitHub

steps=6
notes="$HOME/notes/001_Education"
attch="$HOME/notes/009_Attachments"
atinn="$HOME/notes/001_Education/009_Attachments"
cmssg="$( date +"%d/%m/%y-%H.%M.%S" )"
echo "[1/$steps] Copy attachments to notes Git repository"
cp -r $attch $notes
echo "[2/$steps] Switch directory to $notes"
cd $notes
echo "[3/$steps] Add all changes to staging"
git add --all .
echo "[4/$steps] Commit changes"
git commit -m $cmssg
echo "[5/$steps] Push changes to remote"
git push origin main
echo "[6/$steps] Remove attachments from notes Git repository"
rm -r $atinn
