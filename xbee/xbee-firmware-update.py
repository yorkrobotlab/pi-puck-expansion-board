#!/usr/bin/env python3

import argparse
import sys
from digi.xbee.devices import XBeeDevice
from digi.xbee.firmware import update_local_firmware
from digi.xbee.exception import FirmwareUpdateException, OperationNotSupportedException, XBeeException


def main():
	parser = argparse.ArgumentParser(description="XBee firmware update.")
	parser.add_argument("xml_firmware_file", type=str, help="XML firmware file")
	parser.add_argument("xbee_firmware_file", type=str, nargs='?', default=None, help="XBee firmware file")
	parser.add_argument("bootloader_firmware_file", type=str, nargs='?', default=None, help="bootloader firmware file")
	parser.add_argument("-p", "--port", type=str, default="/dev/ttyUSB0", help="serial port (default /dev/ttyUSB0)")
	parser.add_argument("-b", "--baud", type=int, default=9600, help="serial baud rate (default 9600)")
	parser.add_argument("-t", "--timeout", type=int, default=None, help="communication timeout (optional)")
	parser.add_argument("-s", "--serial", action="store_true", help="use raw serial mode instead of API mode")
	args = parser.parse_args()

	xml_firmware_file = args.xml_firmware_file
	xbee_firmware_file = args.xbee_firmware_file
	bootloader_firmware_file = args.bootloader_firmware_file
	port = args.port
	baud = args.baud
	timeout = args.timeout
	serial = args.serial

	if serial:
		device = None
	else:
		device = XBeeDevice(port, baud)

	try:
		print("Starting firmware update ...")
		if serial:
			update_local_firmware(port, xml_firmware_file,
			                      xbee_firmware_file=xbee_firmware_file,
			                      bootloader_firmware_file=bootloader_firmware_file,
			                      timeout=timeout,
			                      progress_callback=progress_callback)
		else:
			device.open()
			device.update_firmware(xml_firmware_file,
			                       xbee_firmware_file=xbee_firmware_file,
			                       bootloader_firmware_file=bootloader_firmware_file,
			                       timeout=timeout,
			                       progress_callback=progress_callback)
		print("Firmware update successful!")
	except (XBeeException, FirmwareUpdateException, OperationNotSupportedException) as e:
		print("Error: %s" % str(e))
		sys.exit(1)
	finally:
		if device is not None and device.is_open():
			device.close()


def progress_callback(task, percent):
	print("%s: %d%%" % (task, percent))


if __name__ == "__main__":
	main()
