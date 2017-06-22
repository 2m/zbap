#!/bin/bash

CURRENT_PID=`pgrep -f "python Zbap.py"`
if [ -n "${CURRENT_PID}" ]; then
    echo "There is already ZBAP running with PID:$CURRENT_PID"
    exit
fi

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $CURRENT_DIR
python Zbap.py &
