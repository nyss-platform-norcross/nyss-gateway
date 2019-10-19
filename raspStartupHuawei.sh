#!/bin/bash


echo "Looking for Huawei Stick in Network Mode..."



checkForLteStick () {
    usbStr=$(lsusb)
    if [[ $usbStr == *"LTE/UMTS/GSM HiLink Modem/Networkcard"* ]]; then
        echo "Huawei LTE Stick found in correct mode"
        return 1
    else
        return 0
    fi
}

stickFound=0

until stickFound -eq 1; do
    checkForLteStick
    stickFound=$1
    sleep 1
    echo "Not Found..."
done

echo "Stick Found"

echo "Changing Resolve Configuration"

echo "8.8.8.8\n192.168.8.1" >> /etc/resolv.conf

echo "Resolve Config Changed"

echo "Changing metric of wlan0 and eth0 interface..."

sudo ifmetric wlan0 100
sudo ifmetric eth0 99

echo "Metric Changed...."

echo "Startup finished!"



