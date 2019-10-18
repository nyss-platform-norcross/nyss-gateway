#!/bin/bash


echo '### Configuration SCRIPT for NYSS SMS Gateway'

echo 'Checking Internet connection...'

echo -e "GET http://google.com HTTP/1.0\n\n" | nc google.com 80 > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Connected!"
else
    echo "No internet connection... pinging google.com did not work. Internet connection obligatory!"
fi

echo 'Installing usb-modeswitch for Huawei LTE Sticks'
apt install usb-modeswitch
echo 'Done.'



