#!/bin/bash

d="Null"

(
find -L /data/wendell/ -iwholename '*.lyx' -print;
#~ find -L /data/wendell/ -iwholename '*PHYS*.lyx' -print;
#~ find -L /data/wendell/ -iwholename '*GEOG*.lyx' -print;
) | while read i
do
    p=${i/%.lyx}.pdf
    if [ "`dirname \"$p\"`" != "$d" ]; then
        d=`dirname "$p"`;
        echo "---$d";
    fi
    if test "$i" -nt "$p"; then
        #~ echo $i -nt $p
        #~ echo "running lyx";
        echo lyx -e pdf2 "$i";
        lyx -e pdf2 "$i";
        touch "$p";
    #~ else
        #~ echo "$i NOT NEW"
    fi
done

if [ "$1" = "-s" ]; then
    echo "Done converting"
else
    # Wait 10 seconds or a key is pressed
    read  -n1 -s -t10 -p "Press any key to close (or wait 10 seconds)..."
    echo ""
fi
