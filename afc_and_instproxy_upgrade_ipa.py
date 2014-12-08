#!/usr/bin/env python

import plist
from imobiledevice import *

def lockdown_get_service_client(service_class):
	ld = LockdownClient(iDevice())
	return ld.get_service_client(service_class)

def afc_upload_file(filename, local_stream, path="/"):
	afc = lockdown_get_service_client(AfcClient)

	try:
		afc.get_file_info(path)
	except AfcError, e:
		if (e.code != 8):	# AFC_E_OBJECT_NOT_FOUND
			raise e
		# just create path
		afc.make_directory(path)

	upload_file_path = "%s/%s" % (path, filename)

	testipa = afc.open(upload_file_path, mode="w+")
	testipa.write(local_stream.read())
	testipa.close()
	
	# show info and cleanup
	#print afc.read_directory(path)
	#print afc.get_file_info(upload_file_path)

def instproxy_install_file(filename):
	instproxy = lockdown_get_service_client(InstallationProxyClient)

	# upgrade if IPA exist
	instproxy.upgrade(filename, plist.Dict({}))

	# dump application info
	#client_options = plist.Dict({
	#	"ApplicationType": "User",		# Any, System, User
	#})
	#for app in instproxy.browse(client_options):
	#	print "[CFBundleIdentifier] %s" % app["CFBundleIdentifier"]
	#	print "[EnvironmentVariables] %s" % app["EnvironmentVariables"]

def cleanup(path):
	afc = lockdown_get_service_client(AfcClient)

	# IPA will delete after installed
	afc.remove_path(path)

def main():
	payload_stream = open("payload/pangunew.ipa")

	# uncommet following lines if install network IPA
	#print ">>> Download IPA..."
	#import urllib2
	#payload_stream = urllib2.urlopen("http://blog.imaou.com/RankingLog/RankingLog_v1.3.ipa")

	# Install start here
	WORK_PATH = "/IPATemp"		# /private/var/mobile/Media/IPATemp
	
	print ">>> Upload IPA..."
	afc_upload_file("tmp.ipa", payload_stream, path=WORK_PATH)

	print ">>> Install IPA..."
	instproxy_install_file("%s/tmp.ipa" % WORK_PATH)

	print ">>> Cleanup..."
	cleanup(WORK_PATH)

	print ">>> Done"

if __name__ == '__main__':
	main()
