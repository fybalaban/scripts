#!/usr/bin/env bash
cp deskenv.service ~/.config/systemd/user/
cp deskenv.timer ~/.config/systemd/user/
systemctl --user enable deskenv.timer