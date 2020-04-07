#!/bin/sh

if [ -d $SETUP_DIR ]; then
    echo "setup dir"
else
    exit 1
fi
exit 0

INSTANCE_DIR = 'instance'
mkdir -p -- "$INSTANCE_DIR"
FILE="$INSTANCE_DIR/hjhome.json"

if [ ! -f file ]; then
    echo "accessory file doesn't exist"
    python3 csv_deploy.py
fi

echo "start homekit2mqtt"
homekit2mqtt
