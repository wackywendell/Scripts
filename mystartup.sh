#!/bin/bash

file='/home/wendell/.startup.log'

sleep 10
touch $file
echo "$0: `date`" > $file
echo "I am `whoami`" >> $file
setxkbmap -layout 'us,de' -option "grp:menu_toggle,ctrl:swapcaps" 2>&1 >> $file
#xmodmap -verbose /home/wendell/.xmodmaprc >> $file
echo "$0: `date`" >> $file