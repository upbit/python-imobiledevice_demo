python-imobiledevice demo
=========================

libimobiledevice demos for Python

### afc_and_instproxy_upgrade_ipa.py
AfcClient and InstallationProxyClient example, install local/network IPA in background.

~~~sh
$ python afc_and_instproxy_upgrade_ipa.py
>>> Upload IPA...
>>> Install IPA...
>>> Cleanup...
>>> Done
~~~

### afc2_dump_keychain-2.py
Afc2Client example, access root file system and dump keychain-2.db.

~~~sh
$ python afc2_dump_keychain-2.py
>>> write keychain-2.db to local, done
~~~

### debugserver_app_runner.py
DebugServerClient and InstallationProxyClient example, a Python version of `idevicedebug run <bundle_id>`

~~~sh
$ ideviceimagemounter /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/DeviceSupport/8.0/DeveloperDiskImage.dmg{,.signature}

# sometime debugserver crash target
$ python debugserver_app_runner.py
Setting logging bitmask: OK
Setting maximum packet size: OK
Setting working directory: OK
Setting argv: OK
Checking if launch succeeded: None
Setting thread: OK
Traceback (most recent call last):
File "debugserver_app_runner.py", line 98, in <module>
main()
File "debugserver_app_runner.py", line 95, in main
debugserver_run_app(bin_path)
File "debugserver_app_runner.py", line 89, in debugserver_run_app
response = debugserver.send_command(cmd)
File "debugserver.pxi", line 116, in imobiledevice.DebugServerClient.send_command (imobiledevice.c:44176)
File "debugserver.pxi", line 129, in imobiledevice.DebugServerClient.send_command (imobiledevice.c:44051)
File "debugserver.pxi", line 122, in imobiledevice.DebugServerClient.send_command (imobiledevice.c:43964)
File "imobiledevice.pyx", line 30, in imobiledevice.Base.handle_error (imobiledevice.c:4814)
imobiledevice.DebugServerError: Unknown error (-256)

# just run script again...
$ python debugserver_app_runner.py
Setting logging bitmask: OK
Setting maximum packet size: OK
Setting working directory: OK
Setting argv: OK
Checking if launch succeeded: OK
Setting thread: OK
~~~

### afc_shell.py
AfcClient/Afc2Client example, Apple File Conduit shell like `ifuse`.

~~~sh
$ python afc_shell.py
afc:/ # cd /Developer/usr/bin
afc:/Developer/usr/bin # ls
debugserver
DTDeviceArbitration
iprofiler
ScreenShotr
XcodeDeviceMonitor
xctest
afc:/Developer/usr/bin # help sz
sz <remote> <local>

afc:/Developer/usr/bin # sz debugserver debugserver
Write 13801968 bytes to debugserver.
afc:/Developer/usr/bin # help

Documented commands (type help <topic>):
========================================
cat  help  mkdir  pwd  rename  rm  rn  rz  sz

Undocumented commands:
======================
cd  exit  ls  q  quit
~~~

### instproxy_browse_installed_app.py
InstallationProxyClient example, a Python version of `ideviceinstaller -l`

~~~sh
$ python instproxy_browse_installed_app.py
net.pxv.iphone - pixiv 5.3.1.2
com.tencent.mttlite - QQ浏览器 5.5.0.1075
com.sogou.sogouinput - 搜狗输入法 62493
com.jonathanlanis.boost - Boost 2 2.4
com.duokan.reader - 多看阅读 2014102901
com.zzz.RankingLog - RankingLog 1
~~~
