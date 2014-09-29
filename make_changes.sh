#!/bin/bash
echo "Waiting for device.." &&
adb wait-for-device &&
echo "Let's go." &&
adb remount &&
echo "Stopping B2G" &&
adb shell stop b2g &&
echo "Pushing hosts file" &&
adb push adb_hosts.txt /system/etc/hosts &&
echo "pulling settings app" &&
adb pull /system/b2g/webapps/settings.gaiamobile.org/application.zip &&
echo "Adding ddg as search provider" &&
zip --verbose -r application.zip resources/search/* &&
adb push application.zip /system/b2g/webapps/settings.gaiamobile.org/application.zip &&
rm application.zip &&
echo "Rebooting" &&
adb reboot
