#!/usr/bin/env python3

import subprocess
from digi.xbee.devices import XBeeDevice

hostname = subprocess.check_output("hostname", shell=True).decode("utf-8").strip()

print("Setting XBee node ID to", hostname)

device = XBeeDevice("/dev/ttyUSB0", 9600)
device.open()
device.set_node_id(hostname)
device.apply_changes()
device.write_changes()
device.close()
