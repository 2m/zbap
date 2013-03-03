#!/bin/bash
CURRENT_PID=`pgrep -f "python Zbap.py"`
if [ -n "${CURRENT_PID}" ]; then
    kill -SIGINT $CURRENT_PID
else
    echo "Zbap is not running."
fi
