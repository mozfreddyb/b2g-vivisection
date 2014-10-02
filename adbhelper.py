#!/usr/bin/env python
# encoding: utf-8

from subprocess import Popen

class ADB():
    def __init__(self):
        print "Waiting for device..."
        self._run_adb(['wait-for-device'])

    ### Should I add a __del__ that reboots the device if self.shouldReboot is true?
    def __del__(self, *args, **kwargs):
        if self.shouldReboot:
            print "### Device has been modified. Reboot enforced."
            self.reboot()

    def _run_adb(self, args):
        #def call(*args):
        #    print '$ adb ', args
        #print "$", str(['adb'] + args)
        p = Popen((['adb'] + args))
        return p.wait()

    def push(self, localpath, remotepath):
        return self._run_adb(['push', localpath, remotepath])

    def pull(self, remotepath, localpath="."):
        return self._run_adb(['pull', remotepath, localpath])

    def remount(self):
        self.shouldReboot = True
        return self._run_adb(['remount'])

    def reboot(self):
        return self._run_adb(['reboot'])

    def stopB2G(self):
        self.shouldReboot = True
        return self._run_adb(['shell', 'stop', 'b2g'])

    def startB2G(self):
        print "### You are restarting B2G. "\
              "But depending on the modifications you have made, you might want to reboot the device instead?"
        return self._run_adb(['shell', 'start', 'b2g'])

