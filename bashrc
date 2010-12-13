# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

export PYTHONSTARTUP=~/.pythonrc
export PYTHONDOCS=/usr/share/doc/python/html/
set -o vi
# show job status changes immediately
set -b

# The bash history file should save last 10000 commands. Default is 500.
export HISTFILESIZE=10000
# The number of commands to remember in the in-memory command history, as
# reported by the 'history' built-in. Default is 500.
export HISTSIZE=1000
# Don't put duplicate lines in the history. See bash(1) for more options
export HISTCONTROL=ignoreboth

# Don't lose command history when multiple shells run in parallel.
shopt -s histappend
PROMPT_COMMAND="history -a; $PROMPT_COMMAND"
# Don't log these commands to history file.
export HISTIGNORE="ls:cd:[bf]g:exit:..:...:ll:l:la"

# set path to include scripts
[[ "$PATH" =~ "/home/wendell/scripts:" ]] || export PATH=/home/wendell/scripts:$PATH
[[ "$PATH" =~ "/home/wendell/bin" ]] || export PATH=/home/wendell/bin:$PATH

function addpythonpath() {
  [[ "$PYTHONPATH" =~ "$1" ]] || export PYTHONPATH="$PYTHONPATH:$1"
}
addpythonpath /usr/local/lib
addpythonpath /home/wendell/scripts
addpythonpath /home/wendell/scripts/lib
addpythonpath /home/wendell/lib
addpythonpath /home/wendell/lib/python
addpythonpath /home/wendell/lib/python2.6/site-packages
export LD_LIBRARY_PATH='/home/wendell/lib'

#  [[ "$PYTHONPATH" =~ "/home/wendell/scripts" ]] || export PYTHONPATH=/home/wendell/scripts:$PYTHONPATH
# [[  "$PYTHONPATH" =~ "/home/wendell/scripts/lib" ]] || export PYTHONPATH=/home/wendell/scripts/lib:$PYTHONPATH
# [[ "$PYTHONPATH" =~ "/usr/local/lib" ]] || export PYTHONPATH=$PYTHONPATH:/usr/local/lib
export BROWSER=firefox
#export EDITOR=vim
export EDITOR="gvim -f"
export PAGER="less -R"
# export COLORTERM=terminator # what is this?

# for GO
export GOROOT=$HOME/go
export GOARCH=386
export GOOS=linux

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines in the history. See bash(1) for more options
export HISTCONTROL=ignoredups
# ... and ignore same sucessive entries.
export HISTCONTROL=ignoreboth

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize
# use '**' for recursive directory searching
shopt -s globstar
# use '?(...)', '*(...)', '+(...)', '@(...)', '!(...)' to match
#      1 or zero, 0 or more, 1/more, exactly 1, or not the ... expression
shopt -s extglob

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
#if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
#    debian_chroot=$(cat /etc/debian_chroot)
#fi

# FORCES ALL XTERMS TO TAKE 256 COLORS
# THIS MAY BE BAD
if [[ "$TERM" =~ "xterm" ]]; then
    if [ -e /usr/share/terminfo/x/xterm-256color ]; then
        export TERM='xterm-256color'
    else
        export TERM='xterm-color'
    fi
fi

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] || [ -x /bin/tput ] && tput setaf 1 >&/dev/null; then
    # We have color support; assume it's compliant with Ecma-48
    # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
    # a case would tend to support setf rather than setaf.)
    color_prompt=yes
    else
    color_prompt=
    fi
fi


# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
    xterm-256color) color_prompt=yes;;
    screen) color_prompt=yes;;
esac

if [ "$color_prompt" = yes ]; then
    PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME}: ${PWD/$HOME/~}\007"'
    ;;
*)
    ;;
esac

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

#if [ -f ~/.bash_aliases ]; then
#    . ~/.bash_aliases
#fi

# enable color support of ls and also add handy aliases
if [ "$TERM" != "dumb" ] && [ -x /usr/bin/dircolors ]; then
    eval "`dircolors -b`"
    alias ls='ls --color=auto'
    #alias dir='ls --color=auto --format=vertical'
    #alias vdir='ls --color=auto --format=long'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
    alias rgrep='rgrep --color=auto'
fi

# some more ls aliases
alias ll='ls -lh'
alias la='ls -A'
alias l='ls -CF'
alias lf='ls -alh'
alias pac='sudo pacman-color'
complete -o filenames -F _pacman pac

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
# it also takes forever
if [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
fi

##########################################
# added by wendell
##########################################

# for colored man pages!
#export LESS_TERMCAP_mb=$(printf "\e[1;37m")
#export LESS_TERMCAP_md=$(printf "\e[1;37m")
#export LESS_TERMCAP_me=$(printf "\e[0m")
#export LESS_TERMCAP_se=$(printf "\e[0m")
#export LESS_TERMCAP_so=$(printf "\e[1;47;30m")
#export LESS_TERMCAP_ue=$(printf "\e[0m")
#export LESS_TERMCAP_us=$(printf "\e[0;36m")


# uses xd to actually switch directories
function xd() {
             cd `/usr/bin/xd $*`
}

function rtt(){
    rm $1
    touch $1
    tail -f $1
}

# make isomount a command
alias isomount='sudo mount -o loop'
#alias isomount='sudo mount -o loop -t iso9660'

# mount an ipod
export IPOD='/dev/disk/by-id/usb-Apple_iPod_00000098DCFB-0:0-part1'
export BACKUPDEV='/dev/disk/by-id/usb-WD_2500BMV_External_57442D575845583038414638363538-0:0-part1'
#alias ipodmount='sudo mount -t vfat "$IPOD" /media/NIGEL -o"uid=1001,gid=1001,shortname=mixed"'
#alias backupmount='sudo mount -t ext4 "$BACKUPDEV" /media/backup'
alias cammount='sudo mtpfs -o allow_other -o uid=1001 -o gid=1000 /media/camera'

alias ipodumount='sudo umount "$IPOD"'
alias ipodeject='sudo eject "$IPOD"'

# alias for  html manual
alias manh='man -H'
complete -o filenames -F _man manh

alias ipy=ipython
alias apt='sudo aptitude'
complete -o filenames -F _aptitude apt

alias pacupdate='sudo pacman-color -Syu && sudo pacman-optimize'
alias pacorphans='sudo pacman -Qdt | cut -d" " -f1 | xargs -pr sudo pacman --noconfirm -R'

# watch easily
alias wch='watch -d -n1'

# alias for 'college' folder
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'

# make disk usage more readable
alias df='df -TBM'
alias du='du -BM'
alias dud='du -s'
alias dudd='du --max-depth=1 | sort -n'

# alias for 'college' folder
alias cdcl='cd /data/wendell/college/'

# search for a process
alias psgrep='ps -ef | grep'

#edit in a separate process
function ged() { command gedit "$@" 2>/dev/null & }
function sged() { command sudo -b gedit "$@" 2>/dev/null ; }

#edit in geany a separate process
function gn() { command geany 2>/dev/null 1>/dev/null "$@" & }
function sgn() { command sudo -b geany 1>/dev/null 2>/dev/null "$@" ; }

function kwrite() { command kwrite "$@" 2>/dev/null ; }
function kw() { command kwrite "$@" 2>/dev/null & }
function skw() { command sudo -b kwrite "$@" 2>/dev/null ; }


# Find a file with a pattern in name:
function ff() { find . -type f -iname '*'$*'*' ; }
function ffl() { find . -type f -iname '*'$*'*' -printf '%G\t%u\t%M\t%kk\t%P\n' | less -e; }
function fd() { find . -type d -iname '*'$*'*' ; }
function fdl() { find . -type d -iname '*'$*'*' -printf '%G\t%u\t%M\t%kk\t%P\n' ; }

function fo() { pyfindopen . $1 ; }


# find in the 'wendell' folder
function fw() { find /data/wendell -type f -iname '*'$*'*' ; }
function fwo() { pyfindopen /data/wendell $1 ; }
function fwc() { find /data/wendell/college -type f -iname '*'$*'*' ; }
function fwco() { pyfindopen /data/wendell/college $1 ; }

function extract()      # Handy Extract Program.
{
     if [ -f $1 ] ; then
         case $1 in
             *.tar.bz2)   tar xvjf $1     ;;
             *.tar.gz)    tar xvzf $1     ;;
             *.bz2)       bunzip2 $1      ;;
             *.rar)       unrar x $1      ;;
             *.gz)        gunzip $1       ;;
             *.tar)       tar xvf $1      ;;
             *.tbz2)      tar xvjf $1     ;;
             *.tgz)       tar xvzf $1     ;;
             *.zip)       unzip $1        ;;
             *.Z)         uncompress $1   ;;
             *.7z)        7z x $1         ;;
             *)           echo "'$1' cannot be extracted via >extract<" ;;
         esac
     else
         echo "'$1' is not a valid file"
     fi
}

# pip bash completion start
_pip_completion()
{
    COMPREPLY=( $( COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   PIP_AUTO_COMPLETE=1 $1 ) )
}
complete -o default -F _pip_completion pip
# pip bash completion end

ipu=/home/wendell/pkgs/ipython/IPython/frontend/urwid
alias ipu="cd $ipu"
alias ikernel='~/pkgs/ipython/IPython/zmq/pykernel.py --xrep 5575 --pub 5576'
alias iterm='~/pkgs/ipython/IPython/zmq/frontend.py'

function urmeld() {
   meld ~/pkgs/urwid{3,,-py3k}/$1 &
}

function urtest() {
    python ~/pkgs/urwid/test_urwid.py
}

function urtest3() {
    23dir
    python3 ~/pkgs/urwid3/test_urwid.py
}

function mdav() {
	stty -echo
	read -p "Password for wws8:"; echo
	stty echo
	mkdir -p /media/dir
}

function tcumt() {
    echo "Unmounting /media/crypt"
    sudo truecrypt -t -d /home/wendell/Dropbox/crypt
    }

function tcmt() {
	sudo mkdir -p /media/crypt
	sudo truecrypt -t --protect-hidden=no -k "" --fs-options=users,uid=$(id -u),gid=$(id -g),fmask=0113,dmask=0002 --mount /home/wendell/Dropbox/crypt /media/crypt
	sleep 20m && tcumt &
}
