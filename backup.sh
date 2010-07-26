#!/bin/bash

excludefile=/home/wendell/scripts/rdiffbackuplist.txt

sudo rdiff-backup --check-destination-dir --print-statistics -v5 --exclude-globbing-filelist "$excludefile" $@ / /media/backup/rdbackup
