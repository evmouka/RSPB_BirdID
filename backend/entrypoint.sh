#!/bin/bash
set -e

trap "kill -TERM $child" SIGTERM
trap "kill -INT $child" SIGINT

gunicorn -w 4 -b 0.0.0.0:5000 app:app &
child=$!

wait "$child"