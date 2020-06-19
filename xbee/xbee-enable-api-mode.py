#!/usr/bin/env python3

import serial
import sys
import time

print("Enabling API mode on XBee...")

ser = serial.Serial('/dev/ttyUSB0')

print()
time.sleep(1)
print("+++")
ser.write(b"+++")
time.sleep(1)
response = ser.read_until(b"\r")
print(response)
if response != b"OK\r":
    print("Error entering AT mode")
    sys.exit(1)

print()
print("ATAP 1<CR>")
ser.write(b"ATAP 1\r")
response = ser.read_until(b"\r")
print(response)
if response != b"OK\r":
    print("Error setting API mode")
    sys.exit(1)

print()
print("ATWR<CR>")
ser.write(b"ATWR\r")
response = ser.read_until(b"\r")
print(response)
if response != b"OK\r":
    print("Error writing data")
    sys.exit(1)

print()
print("ATCN<CR>")
ser.write(b"ATCN\r")
response = ser.read_until(b"\r")
print(response)
if response != b"OK\r":
    print("Error exiting command mode")
    sys.exit(1)
