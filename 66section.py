#!/usr/bin/env python
# encoding: utf-8
#
# Why is this called 66section.py?
# Because "vi" is the roman number 6 and 6 is shorter. I also hope it's a nice tongue twister

import os.path
from os import listdir

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
                adb.push(fullpath, remotepath)

    os.path.walk('filesystem-mods', visitFsNode, None)

    for appdir in listdir("app-mods"):
        if not os.path.isdir(os.path.join("app-mods/", appdir)):
            print "Not a directory. Skipping", appdir
            continue
        else:
            # e.g. app-mods/settings.gaiamobile.org_application.zip
            localname = os.path.join('app-mods/', appdir + "_application.zip")
            remotename = os.path.join("/system/b2g/webapps/", appdir, "/application.zip")
            # Get the app
            adb.pull(remotename, localname)
            # Modify ZIP in-place
            def addToZip(zipname, dirname, fnames):
                zipname = os.path.relpath(zipname, "app-mods")
                for f in fnames:
                    fullpath = os.path.join(dirname, f)
                    if os.path.isfile(fullpath):
                        os.chdir("app-mods") # if paths aren't relative to the ZIP, it won't work.
                        print "$ zip -r", zipname, os.path.relpath(fullpath, "app-mods")
                        os.chdir("..")
                        # TODO FIXME XXX something in here is messed up. fix tomorrow.

            os.path.walk(os.path.join("app-mods/", appdir), addToZip, localname)
            # Push it back
            adb.push(localname, remotename)
