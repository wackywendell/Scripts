#!/bin/sh
# picasa-hook-email.sh
# Edit the next line
PATH_TO_TBIRD=thunderbird
emailstr=$(echo “$1″|sed ‘s/mailto:?/to=,/’|\
sed ‘s/&cc=/,cc=/’|sed ‘s/&bcc=/,bcc=/’|sed “s/&body=/,body=\’/”|\
sed “s/&attach=/\’,attachment=\’file:\/\//”|sed ‘s/&attach=/,file:\/\//g’)”‘”
$PATH_TO_TBIRD -compose “$emailstr”
#End of picasa-hook-email.sh