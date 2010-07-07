#!/bin/bash

while true; do
    if [ "`date`" != "$d" ]; then
        echo `date`
        d=`date`
    fi
    sleep .05
done
