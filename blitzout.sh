#!/bin/bash

tmp=/tmp/emails.txt

function sendblitz {
    ssmtp $1 < $2
    echo $1 >> $tmp
}

function countlines {
    wc -l $1 | awk '{print $1}'
}

touch $tmp
rm $tmp
touch $tmp
total=0

tmplen=`countlines $tmp`
emlen=`countlines $1`
started=-300

for n in `cat $1`; do
    while [ $tmplen -lt $started ]; do
        sleep 1
        tmplen=`countlines $tmp`
        echo "started: $started tmplen: $tmplen"
    done
    sendblitz $n $2 &
    ((started++))
    tmplen=`countlines $tmp`
    echo "started: $started tmplen: $tmplen"
done

echo "$tmplen, $emlen"

while [ $tmplen -lt $emlen ]; do
    sleep 1
    tmplen=`countlines $tmp`
    echo "tmplen: $tmplen, emlen: $emlen"
done
