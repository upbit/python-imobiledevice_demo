#!/usr/bin/env python

import plist
from imobiledevice import *

KEYCHAIN_2_PATH = "/private/var/Keychains/keychain-2.db"

def lockdown_get_service_client(service_class):
	ld = LockdownClient(iDevice())
	return ld.get_service_client(service_class)

def afc2_dump_keychain2():
	afc2 = lockdown_get_service_client(Afc2Client)

	# get keychain-2.db size
	keychain2 = afc2.open(KEYCHAIN_2_PATH, mode="r")
	keychain2.seek(0, 2)	# SEEK_END(2)
	file_size = keychain2.tell()

	# read keychain-2.db and write to local
	keychain2.seek(0, 0)	# SEEK_SET(0)
	local_file = open("keychain-2.db", "w+")
	local_file.write(keychain2.read(file_size))

	local_file.close()
	keychain2.close()

def main():
	afc2_dump_keychain2()
	print ">>> done"

if __name__ == '__main__':
	main()
