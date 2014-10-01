#!/usr/bin/env python
# encoding: utf-8

from subprocess import call

class ADB():
    def __init__(self):
        print "Waiting for device..."
        self._run_adb(['wait-for-device'])

    ### Should I add a __del__ that reboots the device if self.shouldReboot is true?

    def _run_adb(self, args):
        def call(*args):
            print '$ adb ', args
        return call((['adb'] + args))

    def push(self, localpath, remotepath):
        self._run_adb(['push', localpath, remotepath])

    def pull(self, remotepath, localpath="."):
        self._run_adb(['pull', remotepath, localpath])

    def remount(self):
        self.shouldReboot = True
        self._run_adb(['remount'])

    def reboot(self):
        self._run_adb(['reboot'])

    def stopB2G(self):
        self.shouldReboot = True
        self._run_adb(['shell', 'stop', 'b2g'])

    def startB2G(self):
        print "You are restarting B2G. "\
              "But depending on the modifications you have made, you might want to reboot the device instead?"
        self._run_adb(['shell', 'start', 'b2g'])

