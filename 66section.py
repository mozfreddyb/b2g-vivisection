#!/usr/bin/env python
# encoding: utf-8
#
# Why is this called 66section.py?
# Because "vi" is the roman number 6 and 6 is shorter. I also hope it's a nice tongue twister

import os.path

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

    def doAppMods(_, dirname, fnames):
        for subdir in fnames:
            apppath = os.path.join(dirname, subdir) # e.g. settings.gaiamobile.org
            if not os.path.isdir(apppath):
                continue
            else:
                if dirname == "app-mods": continue
                localname = dirname+"_application.zip"
                remotename = "/system/b2g/webapps/"+os.path.relpath(dirname,"app-mods")+"/application.zip"
                # Get the app
                adb.pull(remotename, localname)
                # Modify ZIP in-place
                def addToZip(zipname, dirname, fnames):
                    for f in fnames:
                        if os.path.isfile(f):
                            fullpath = os.path.join(dirname, f)
                            os.chdir("app-mods")
                            print "zip -r", zipname, f
                            # TODO FIXME XXX something in here is messed up. fix tomorrow.
                os.path.walk(apppath, addToZip, localname)

                # Push it back
                adb.push(localname, remotename)

    os.path.walk("app-mods", doAppMods, None)