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

