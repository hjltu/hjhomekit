#!/usr/bin/env python3

import os, sys, inspect, csv
import csv_deploy
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from config.hjhome import MQTT_SERVER, HOMEKIT_NAME, \
    SETUP_DIR, INSTANCE_DIR, MAC_FILE, HOMEKIT_ACCESSORY_FILE
from setup.rpi_serial import serial as SERIAL
from setup.rpi_serial import mac as SERIAL_MAC
from setup.rpi_serial import pin as PIN_CODE

ACC_FILE = INSTANCE_DIR + "/" + HOMEKIT_ACCESSORY_FILE
MAC_FILE = INSTANCE_DIR + "/" + MAC_FILE

print("create accessories")
res = csv_deploy.main()
if res is not True:
    print('deploy ERR:', res)
    sys.exit(1)
with open(MAC_FILE, 'r') as file:
    MAC_ADDR = file.read().replace('\n', '')

print("start homekit2mqtt")
print("homekit2mqtt -m " + ACC_FILE + " -b " + HOMEKIT_NAME + " -a " + MAC_ADDR + " -c " + PIN_CODE + " -u mqtt://" + MQTT_SERVER)
os.system("homekit2mqtt -m " + ACC_FILE + " -b " + HOMEKIT_NAME + " -a " + MAC_ADDR + " -c " + PIN_CODE + " -u mqtt://" + MQTT_SERVER)
