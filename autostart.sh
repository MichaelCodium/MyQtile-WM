#!/bin/sh
xfsettingsd &
xfce4-power-manager &
nm-applet &

sleep 20

rclone mount gdrive: /home/xunlai/GoogleDrive/ --vfs-cache-mode writes --rc --daemon
