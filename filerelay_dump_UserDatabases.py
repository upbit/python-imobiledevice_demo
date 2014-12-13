#!/usr/bin/env python

import os
import sys
import time
import plist
from imobiledevice import *

##
## modify from https://github.com/libimobiledevice/libimobiledevice/blob/master/dev/filerelaytest.c
##
# !! THIS DEMO ONLY WORKS ON iOS<=7.x
# on iOS8 com.apple.mobile.file_relay is no longer available: http://www.zdziarski.com/blog/?p=3820

def lockdown_get_service_client(service_class):
	ld = LockdownClient(iDevice())
	return ld.get_service_client(service_class)

def file_relay_get_UserDatabases():
	filerelay = lockdown_get_service_client(FileRelayClient)
	filerelay_sources = [
		#"AppleSupport",
		#"Network",
		#"VPN",
		#"WiFi",
		"UserDatabases",
		#"CrashReporter",
		#"tmp",
		#"SystemConfiguration"
	]

	conn = filerelay.request_sources(filerelay_sources)

	sys.stdout.write("Dump to filerelay_dump.cpio.gz:\n")
	with open("filerelay_dump.cpio.gz", "wb+") as dumpfile:
		while (1):
			try:
				#data = conn.receive(4096)
				data = conn.receive_timeout(4096, 10)
				dumpfile.write(data)

				sys.stdout.write(".")
			except Exception, e:
				if (e.code == -2):		# no more data
					break
				# FileRelayError: Permission denied (-6) on iOS 8.x
				raise e

	print "Done"

def main():
	file_relay_get_UserDatabases()

if __name__ == '__main__':
	main()
