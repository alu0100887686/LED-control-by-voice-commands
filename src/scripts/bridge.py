#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import serial, sys, re, binascii
import serial.tools.list_ports

def getSerialPort():
    r = ""
    if sys.platform.startswith('linux2'): # Linux serial port
        r = re.compile("/dev/tty[A-Za-z]*")
    elif sys.platform.startswith('win32'): # Windows serial port
        r = re.compile("COM[A-Za-z0-9]*")
    elif sys.platform.startswith('darwin'): # Mac Osx serial port
        r = re.compile("/dev/cu.usbmodem[A-Za-z0-9]*")
    list = serial.tools.list_ports.comports()
    enable = []
    usable = []
    for i in list:
        enable.append(i.device)
    for i in filter(r.match, enable):
        usable.append(i)
    return usable[0]

print (getSerialPort())
arduino = serial.Serial(getSerialPort(), 9600)
option = "1"
while(option != "0" ):
    option = str(input('Enter your input: '))
    arduino.write(option.encode())
arduino.close()
