#!/bin/bash



progname=$1
echo "RUNNING $1 ONCE!"

progwithargs=$@

origwd=`pwd`

lfname="runonce-$progname.lock"
#echo lockfile-create -r0 "$lfname"

#lockfile-create -r0 "$lfname"
cd ~/.config
lockfile-create -lr0 "$lfname" 2>/dev/null
created=$?



if [[ $created == 0 ]] ; then
    #echo "lock file succeeded:" $created
    cd $origwd
    $progwithargs &
    cd ~/.config
    pid=$!
    echo $pid > $lfname
    wait $pid
    lockfile-remove -l "$lfname"
else
    #echo "lockfile failed!" $created
    pid=`cat $lfname`
    winid=`wmctrl -lp | awk '{if($3=='$pid') print $1}'`
    echo "raising window $winid of process $pid..."
    wmctrl -iR $winid
fi


cd $origwd