#!/bin/bash

k=`ps -e | grep rainlendar | awk '{print $1}'`
if [ -n "$k" ]; then
	kill -15 $k
	echo "killed rainlendar"
else
	echo "no rainlendar found"
fi

rainlendar2 &