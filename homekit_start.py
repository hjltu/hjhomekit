#!/usr/bin/env python3

import os, sys, inspect, csv
import csv_deploy
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from config.hjhome import MQTT_SERVER, HOMEKIT_NAME,
    SETUP_DIR, INSTANCE_DIR, MAC_FILE, HOMEKIT_ACCESSORY_FILE
from setup.rpi_serial import serial as SERIAL
from setup.rpi_serial import mac as SERIAL_MAC
from setup.rpi_serial import pin as PIN_CODE

FILE = INSTANCE_DIR + "/" + HOMEKIT_ACCESSORY_FILE

print("create accessories")
csv_deploy.main()
MAC_ADDR = os.system("cat " + INSTANCE_DIR + "/" + MAC_FILE)
echo MAC_ADDR

print("start homekit2mqtt")
os.system("homekit2mqtt -m " + $FILE + "-b " + HOMEKIT_NAME + " -a " + MAC_ADDR + " -c " PIN_CODE + " -u " + MQTT_SERVER)
