#!/bin/bash

# Replace these three settings.
PROJDIR="/home/reddit/git/wowcaretaker/app"
PIDFILE="$PROJDIR/wowcaretaker.pid"
SOCKET="$PROJDIR/wowcaretaker.sock"
#SETTINGS="$PROJDIR/wowcaretaker/settings_live"
HOST="127.0.0.1"
PORT="3995"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

exec /usr/bin/env - \
  PYTHONPATH="../python:.." \
  ./manage.py runfcgi host=$HOST port=$PORT pidfile=$PIDFILE --settings=wowcaretaker.settings method=threaded maxspare=2

# --settings=wowcaretaker.settings_live
