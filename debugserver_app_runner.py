#!/usr/bin/env python

import os
import sys
import time
import plist
from imobiledevice import *

# mount /Developer image before test
# ideviceimagemounter /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/DeviceSupport/8.0/DeveloperDiskImage.dmg{,.signature}

APP_BUNDLE_ID = "com.malcolmhall.WiFiPasswords"

def lockdown_get_service_client(service_class):
	ld = LockdownClient(iDevice())
	return ld.get_service_client(service_class)

def debugserver_run_app(app_bin_path):
	app_root = os.path.dirname(app_bin_path)

	#dev = iDevice()
	#ld = LockdownClient(dev, label="app-runner")
	#svrport = ld.start_service(DebugServerClient)
	#debugserver = DebugServerClient(dev, svrport)
	debugserver = lockdown_get_service_client(DebugServerClient)

	with DebugServerCommand("QSetLogging:bitmask=LOG_ALL|LOG_RNB_REMOTE|LOG_RNB_PACKETS") as cmd:
		print "Setting logging bitmask: %s" % debugserver.send_command(cmd)
	with DebugServerCommand("QSetMaxPacketSize:", 1, ["1024"]) as cmd:
		print "Setting maximum packet size: %s" % debugserver.send_command(cmd)
	with DebugServerCommand("QSetWorkingDir:", 1, [app_root]) as cmd:
		print "Setting working directory: %s" % debugserver.send_command(cmd)

	response = debugserver.set_argv(1, [app_bin_path])
	print "Setting argv: %s" % response

	with DebugServerCommand("qLaunchSuccess") as cmd:
		print "Checking if launch succeeded: %s" % debugserver.send_command(cmd)

	with DebugServerCommand("Hc0") as cmd:
		print "Setting thread: %s" % debugserver.send_command(cmd)

	cmd_continue = DebugServerCommand("c")
	loop_response = debugserver.send_command(cmd_continue)

	# waiting Ctrl+C to exit
	while True:
		try:
			if (loop_response == None):
				break
			result, loop_response = debugserver.handle_response(loop_response, reply=True)
			if result:
				sys.stdout.write(result)

			time.sleep(100/1000.0)

		except (KeyboardInterrupt, SystemExit):
			print "Exiting..."
			break

	with DebugServerCommand("k") as cmd:
		response = debugserver.send_command(cmd)
		print "Killing process: %s" % debugserver.handle_response(response)

def main():
	instproxy = lockdown_get_service_client(InstallationProxyClient)
	bin_path = instproxy.get_path_for_bundle_identifier(APP_BUNDLE_ID)
	debugserver_run_app(bin_path)

if __name__ == '__main__':
	main()
