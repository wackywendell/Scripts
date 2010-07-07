#!/bin/bash

cmd="wget -N --retry-connrefused"
dir="/home/wendell/Dropbox/Us/Germany Documents/berlin transportation"
f1='http://www.s-bahn-berlin.de/fahrplanundnetz/pdf/MoFr_BGWD_Richtung_BWKR.pdf'
f2='http://www.s-bahn-berlin.de/fahrplanundnetz/pdf/MoFr_BGWD_Richtung_BNIS.pdf'
f3='http://www.s-bahn-berlin.de/fahrplanundnetz/pdf/SaSo_BGWD_Richtung_BWKR.pdf'
f4='http://www.s-bahn-berlin.de/fahrplanundnetz/pdf/SaSo_BGWD_Richtung_BNIS.pdf'
f5='http://www.s-bahn-berlin.de/pdf/VBB-Liniennetz.pdf'
f6='http://www.s-bahn-berlin.de/pdf/S+U-Liniennetz.pdf'
zf='http://www.vbbonline.de/software/WINKOMP526.ZIP'

cd "$dir"
logfile=S7.log
olddate=`ls -l "../vbb update/PLAN1.ZIP"`
cmd="wget -N --retry-connrefused -a$logfile"
cmd1="wget -N --retry-connrefused -o$logfile"
$cmd1 "$f1" "$f2" "$f3" "$f4" "$f5" "$f6" "$zf"
#$cmd1 'http://www.s-bahn-berlin.de/fahrplanundnetz/pdf/MoFr_BGWD_Richtung_BWKR.pdf'
#$cmd 'http://www.s-bahn-berlin.de/fahrplanundnetz/pdf/MoFr_BGWD_Richtung_BNIS.pdf'
#$cmd 'http://www.s-bahn-berlin.de/fahrplanundnetz/pdf/SaSo_BGWD_Richtung_BWKR.pdf'
#$cmd 'http://www.s-bahn-berlin.de/fahrplanundnetz/pdf/SaSo_BGWD_Richtung_BNIS.pdf'

if [[ $? ]]; then
    echo "$? Unzipping..." >> $logfile
    unzip -uo WINKOMP526.ZIP -d"../vbb update" 2>&1 >>$logfile
    newdate=`ls -l "../vbb update/PLAN1.ZIP"`
    if [[ "$olddate" != "$newdate" ]] || [[ $1 == 'force' ]] ; then
        echo "Running setup..." >> $logfile
        wine "../vbb update/SETUP.EXE"
    else
        echo "Setup not running" >> $logfile
    fi
else
    echo "Failure, not unzipping!" >> $logfile
fi
