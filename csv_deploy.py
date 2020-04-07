#!/usr/bin/env python3
"""
csv_depliy.py
hjltu@ya.ru
27-jul-19 create
7-apr-20 hjhomekit
"""

import os, sys, inspect, csv
import csv2list
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from setup.rpi_serial import serial as SERIAL
from setup.rpi_serial import mac as SERIAL_MAC

CSV_FILE = SERIAL + '.csv'
CSV_PATH = os.environ['HOME']+'/config'


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
    print('acc_prop:', acc_prop)
    return os.system("./filegen.sh " + acc_prop)


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
    if type(acc) is 'str':
        return acc
    res = json_file_gen(acc)
    print('csv deploy result:',res)
    if res != 0:
        return "ERR filegen"
    return True


if __name__ == "__main__":
    main()
