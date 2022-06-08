#!/bin/bash

if [ ! -d "/home/pi" ]; then 
    mkdir /home/pi
fi

echo "Username of SMS Eagle IoT Hub user:"
read IOT_USERNAME

echo "Password of SMS Eagle IoT Hub user:"
read IOT_PASSWORD

echo "Nyss IoT Hub device connection string:"
read IOT_CONNECTIONSTRING

echo "Fetching Nyss scripts …"



curl -s -o /home/pi/smsEagle-iot-hub-handler.py https://raw.githubusercontent.com/nyss-platform-norcross/nyss-sms-gateway/feature/update-handler-script/SMSEagleIOTBridge/smsEagle-iot-hub-handler.py
res=$?
if test "$res" != "0"
then 
    echo "Failed to fetch smsEagle-iot-hub-handler.py"
    exit 0
else
    chmod +x /home/pi/smsEagle-iot-hub-handler.py
fi

curl -s -o /home/pi/nyssIotBridge.py https://raw.githubusercontent.com/nyss-platform-norcross/nyss-sms-gateway/feature/update-handler-script/SMSEagleIOTBridge/nyssIotBridge.py
res=$?
if test "$res" != "0"
then
    echo "Failed to fetch nyssIotBridge.py"
    exit 0
else
    chmod +x /home/pi/nyssIotBridge.py
fi

curl -s -o /home/pi/nyssIotBridgeBoot.sh https://raw.githubusercontent.com/nyss-platform-norcross/nyss-sms-gateway/feature/update-handler-script/SMSEagleIOTBridge/nyssIotBridgeBoot.sh
res=$?
if test "$res" != "0"
then
    echo "Failed to fetch nyssIotBridgeBoot.sh"
    exit 0
else
    chmod +x /home/pi/nyssIotBridgeBoot.sh
fi

curl -s -o /etc/systemd/system/nyss-iot-bridge.service https://raw.githubusercontent.com/nyss-platform-norcross/nyss-sms-gateway/feature/update-handler-script/SMSEagleIOTBridge/nyss-iot-bridge.service
res=$?
if test "$res" != "0"
then
    echo "Failed to fetch nyss-iot-bridge.service"
    exit 0
else
    chmod +644 /etc/systemd/system/nyss-iot-bridge.service
fi

echo "All scripts fetched, creating config file for the nyss service …"

mkdir -p /etc/systemd/system/nyss-iot-bridge.service.d
test -e /etc/systemd/system/nyss-iot-bridge.service.d/override.conf
res=$?
if test "$res" == "0"
then
    rm /etc/systemd/system/nyss-iot-bridge.service.d/override.conf
fi

touch /etc/systemd/system/nyss-iot-bridge.service.d/override.conf

echo "[Service]" >> /etc/systemd/system/nyss-iot-bridge.service.d/override.conf
echo "Environment=\"IOT_HUB_CONNECTIONSTRING=$IOT_CONNECTIONSTRING\"" >> /etc/systemd/system/nyss-iot-bridge.service.d/override.conf
echo "Environment=\"SMSEAGLE_USERNAME=$IOT_USERNAME\"" >> /etc/systemd/system/nyss-iot-bridge.service.d/override.conf
echo "Environment=\"SMSEAGLE_PWD=$IOT_PASSWORD\"" >> /etc/systemd/system/nyss-iot-bridge.service.d/override.conf

python3 -m pip install --upgrade pip
pip3 install azure-iot-device
pip3 install six

echo "Starting the nyss service …"

systemctl daemon-reload
systemctl enable nyss-iot-bridge.service
systemctl start nyss-iot-bridge.service

echo "Setup finished, rebooting device …"

reboot
