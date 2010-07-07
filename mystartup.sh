#!/bin/bash

echo "$0: `date`" > ~/.Xmodmaptxt
echo "I am `whoami`" >> ~/.Xmodmaptxt
sleep 10 && xmodmap -verbose /home/wendell/.xmodmaprc >> ~/.Xmodmaptxt
echo "$0: `date`" >> ~/.Xmodmaptxt