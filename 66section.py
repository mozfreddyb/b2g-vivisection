#!/usr/bin/env python
# encoding: utf-8
#
# Why is this called 66section.py?
# Because "vi" is the roman number 6 and 6 is shorter. I also hope it's a nice tongue twister

import os.path
from os import listdir
from subprocess import Popen

from adbhelper import ADB

if __name__ == "__main__":
    adb = ADB()
    # Walk through filesystem modifications
    def visitFsNode(_, dirname, fnames):
        for f in fnames:
            fullpath = os.path.join(dirname, f)
            if os.path.isdir(fullpath):
                continue
            else:
                remotepath = os.path.join("/", os.path.relpath(fullpath, 'filesystem-mods'))
                print "### Patching file:", remotepath
                adb.push(fullpath, remotepath)

    adb.remount()
    print "### Looking for filesystem patches..."
    os.path.walk('filesystem-mods', visitFsNode, None)

    cwd_abs = os.path.abspath(os.curdir)

    for appdir in listdir("app-mods"):
        appdir_abs = os.path.abspath(os.path.join("app-mods/", appdir))
        if not os.path.isdir(appdir_abs):
            print "### Not a directory. Skipping", appdir
            continue
        else:
            print "### Patching", appdir
            # e.g. app-mods/settings.gaiamobile.org"
            zipname = os.path.join(appdir_abs, "application.zip")#
            # XXX the remotepath may be wrong. there's also /data/local/webapps it seems.
            remotename = os.path.join("/system/b2g/webapps/", appdir, "application.zip")
            # Get the app
            print "### Fetching & Modifying..."
            if adb.pull(remotename, zipname) != 0:
                print "EEE App {} does not exist on device. Skipping".format(appdir)
                continue

            # Modify ZIP in-place
            #print "Changing to", appdir_abs
            os.chdir(appdir_abs)
            for fnode in listdir("."):
                if fnode == "application.zip":
                    continue
                #print "$", str(['zip', '-r', 'application.zip', fnode])
                p = Popen(['zip', '-r', 'application.zip', fnode], cwd=appdir_abs)
                p.wait()


            # Push it back
            print "### Pushing back to device"
            adb.push(zipname, remotename)
            p=Popen(["rm", "application.zip"], cwd=appdir_abs)
            p.wait()

            os.chdir(cwd_abs)
