#!/bin/sh

# PROVIDE: bruteforceblocker
# REQUIRE: LOGIN
# BEFORE: mail
# KEYWORD: FreeBSD shutdown

#
# Add the following lines to /etc/rc.conf to enable bruteforceblocker:
#
# bruteforceblocker_enable="YES"
#

. /etc/rc.subr

name="bruteforceblocker"
rcvar=`set_rcvar`
load_rc_config $name

command="/data/sysop/scripts/bruteforceblocker.pl"
pidfile="/var/run/bruteforceblocker.pid"
procname="/usr/bin/perl"

stop_postcmd=stop_postcmd

stop_postcmd()
{
  rm -f $pidfile
}

# set defaults
bruteforceblocker_enable=${bruteforceblocker_enable:-"NO"}

run_rc_command "$1"
