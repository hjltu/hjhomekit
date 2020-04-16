#!/usr/bin/env python3
"""
csv_depliy.py
hjltu@ya.ru
27-jul-19 create
7-apr-20 hjhomekit
"""

import os, sys, inspect, csv
import csv2list
sys.path.append("/root")
from setup.rpi_serial import serial as SERIAL
from setup.rpi_serial import mac as SERIAL_MAC


CSV_FILE = SERIAL + '.csv'
#CSV_PATH = os.environ['HOME']+'/config'
CSV_PATH = parent_dir+'/config'


def check_csv_file_exist():
    files = os.listdir(CSV_PATH)
    if CSV_FILE in files:
        return True


def parse_csv_file(csvfile):
    """
    input: csv file
    output: list of dicts
    """
    return csv2list.main(csvfile)


def json_file_gen(acc):
    """
    exec filegen.sh to create
        json file homekit accessory
    """
    acc_prop=''
    for a in acc:
        acc_prop += a["type"]+' '+a["acc"]+' '+a["name"]+' '
    print('acc_prop len:', len(acc_prop), 'acc_prop:', acc_prop)
    return os.system("./filegen.sh " + acc_prop)

def hass_conf_file_gen(acc):
    """
    exec hass_filegen.sh to create
        config file homeassistant accessory
    """
    acc_prop=''
    for a in acc:
        acc_prop += a["type"]+' '+a["name"]+a['comm']+' '+a['stat']+' '
    print('acc_prop len:', len(acc_prop), 'acc_prop:', acc_prop)
    return os.system("./hass_filegen.sh " + acc_prop)

def main():
    """
    return True if everything is OK
        or error string
    system env variables:
        read:
            home = os.environ['HOME']
            sn = os.getenv('SERIAL', '1234abcd')
        write:
            os.environ['SERIAL'] = '1234abcd'
    """
    if check_csv_file_exist() is not True:
        return "file {} not found in {}".format(CSV_FILE, CSV_PATH)
    acc = parse_csv_file(CSV_PATH + '/' + CSV_FILE)
    if isinstance(acc, str):
        return acc
    res = json_file_gen(acc)
    print('csv deploy result:',res)
    if res != 0:
        return "filegen exit code is: " + str(res)
    res = hass_conf_gen(acc)
    return True


if __name__ == "__main__":
    main()
