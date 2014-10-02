PROJECT STATUS
===================
b2g-vivisection might not work for production builds.
It expects apps that you want modified to live in `/system/b2g/webapps/`

-----------------------------------------------------------------------

b2g-vivisection
===============

This script allows you to modify a rooted Firefox OS device when running.
It requires the phone to be rooted.

**WARNING**:
 - This script does neither check for compatibility nor support!
 - If you overwrite stuff that you have no backup off, it will be lost!
 - It is recommended to apply changes with b2g-vivisection after
flashing/updating a device and before restoring user-data from a
known-good backup.


What this script does
=====================

Filesystem Modifications
========================
The script will go look into the directory `filesystem-mods` and
considers this as a copy of the path `/` on device.
This means that every file in `filesystem-mods` will be copied to the
same path on device.

Example: `filesystem-mods/etc/hosts` will be copied to `/etc/hosts`
This would allow blocking access to certain domains, effectively
installing an ad blocker.


App Modifications
=================
This works similarly to the filesystem modifications, except apps are
present on device as a ZIP file. This script will download the app as
application.zip and modify files *within the ZIP* by replacing selective
files according to the tree in `app-mods`.

Example:
`app-mods/settings.gaiamobile.org/resources/search/providers.json` will
lead to `/system/b2g/webapps/settings.gaiamobile.org/application.zip`
being loaded from the device to a local folder (through `adb pull`),
updated and copied back to the device.
This would change the list of available search engines.
