#!/bin/bash

echo -n "Gmail password: "

stty -echo
read password
stty echo


sudo mount -t gmailfs /usr/local/bin/gmailfs.py /media/gmail -o username=wendellextras,password="$password",fsname=mygmail
# sudo rsync -avr /home/wendell/wendellc/ /media/gmail/
