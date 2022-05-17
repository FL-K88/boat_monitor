#!/usr/bin/python

import serial

ser = serial.Serial(‘dev/tty/ACM0’, 9600)

while True:

input = ser.read()

print (input.decode(“utf-8”))