#!/usr/bin/env python

import os
import sys
import time
import plist
from imobiledevice import *

"""
### key for ReturnAttributes:

	ApplicationDSID
	ApplicationType
	BuildMachineOSBuild
	CFBundleDevelopmentRegion
	CFBundleDisplayName
	CFBundleDocumentTypes
	CFBundleExecutable
	CFBundleIcons
	CFBundleIdentifier
	CFBundleInfoDictionaryVersion
	CFBundleName
	CFBundleNumericVersion
	CFBundlePackageType
	CFBundleShortVersionString
	CFBundleSignature
	CFBundleSupportedPlatforms
	CFBundleURLTypes
	CFBundleVersion
	Container
	DTCompiler
	DTPlatformBuild
	DTPlatformName
	DTPlatformVersion
	DTSDKBuild
	DTSDKName
	DTXcode
	DTXcodeBuild
	Entitlements
	EnvironmentVariables
	Fabric
	IsUpgradeable
	LSRequiresIPhoneOS
	MinimumOSVersion
	NSPhotoLibraryUsageDescription
	Path
	SequenceNumber
	SignerIdentity
	UIDeviceFamily
	UILaunchImages
	UIMainStoryboardFile
	UIPrerenderedIcon
	UIStatusBarHidden
	UIStatusBarStyle
	UIStatusBarTintParameters
	UISupportedInterfaceOrientations
	UTExportedTypeDeclarations
	UTImportedTypeDeclarations
"""

def lockdown_get_service_client(service_class):
	ld = LockdownClient(iDevice())
	return ld.get_service_client(service_class)

def list_installed_app(app_type="Any"):
	instproxy = lockdown_get_service_client(InstallationProxyClient)

	client_options = plist.Dict({
		"ApplicationType": app_type,
		"ReturnAttributes": plist.Array([
			"CFBundleIdentifier",
			"CFBundleName",
			"CFBundleVersion",
		]),
	})

	return instproxy.browse(client_options)

def printf_app_bundles(app_list):
	for app in app_list:
		app_name = app["CFBundleName"].get_value().encode("utf8")
		print "%s - %s %s" % (app["CFBundleIdentifier"], app_name, app["CFBundleVersion"])

def main():
	#app_list = list_installed_app("System")
	app_list = list_installed_app("User")
	printf_app_bundles(app_list)
	
if __name__ == '__main__':
	main()
