#!/bin/sh
# This will grab twistd's PID and kill that server

PID="`pwd`/twistd.pid"

kill -9 $(cat $PID)
rm "`pwd`/twistd.pid"
