#!/usr/bin/env python3

import serial
import time
import struct
import sys

ser = serial.Serial(sys.argv[1],9600)

def req(cmd):
    time.sleep(0.1)
    ser.write(cmd)
    time.sleep(0.1)
    return ser.read_all()

def parse_ds(data):
    measurements = {}
    for i in range(8,44,2):
        measurements[str(1270+(i-8)*10)] = struct.unpack('<h',data[i:i+2])[0]/100
    return {
        'memslot': data[7],
        'filename': data[72:88].decode('UTF-8').split('\0')[0],
        'measurements': measurements,
        'threshold': struct.unpack('<h',data[92:94])[0]/100
    }

def parse_si(data):
    return {
        'prodno': data[4:11].decode('UTF-8'),
        'serno': data[17:29].decode('UTF-8'),
        'hw_ver': str(data[34])+'.'+str(data[33])+'.'+str(data[32]),
        'fw_ver': str(data[38])+'.'+str(data[37])+'.'+str(data[36]),
        'caldate': data[40:48].decode('UTF-8')
    }


data = req(b'\x02\x11\x00\x05\x03\x00\x00')
print(parse_si(data))

for ds in range(255):
    data = req(b'\x02\x21\x00\x05\x00'+ds.to_bytes(1)+b'\x03\x00\x00')
    if(data):
        print(parse_ds(data))
    else:
        break
