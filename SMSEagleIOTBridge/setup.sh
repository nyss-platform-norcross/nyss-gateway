#!/bin/bash

if [ ! -d "/home/pi" ]; then 
    mkdir /home/pi
fi

version=$(python3 -V 2>&1)
parser="${version/\Python /}"
parsedVersion=$(echo "${parser//./}")
short="${parsedVersion:0:2}"

if [[ "$short" -lt "40" && "$short" -gt "36" ]]
then 
    echo "Correct version of Python installed"
else
    echo "Installing correct version of Python..."
    read -r -p "Do you want to enable setup optimizations? This may take a significant amount of time (y/n) " yn
    do-not-use_apt-get update
    do-not-use_apt-get install libffi-dev libbz2-dev liblzma-dev libsqlite3-dev libncurses5-dev libgdbm-dev zlib1g-dev libreadline-dev libssl-dev tk-dev build-essential libncursesw5-dev libc6-dev openssl git
    wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz
    tar xf Python-3.6.5.tar.xz

case $yn in
      [nN] ) ./Python-3.6.5/configure ;;
      [yY] ) ./Python-3.6.5/configure --enable-optimizations ;;
      * ) echo invalid response;
exit 1;;
esac
    make -j -l 4
    make altinstall
    echo “alias python3=/usr/local/bin/python3.6” >> ~/.bashrc
    source ~/.bashrc
    python3 -m pip install --upgrade pip
    pip3 install azure-iot-device
    pip3 install six
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



echo "Starting the nyss service …"

systemctl daemon-reload
systemctl enable nyss-iot-bridge.service
systemctl start nyss-iot-bridge.service

echo "Setup finished, rebooting device …"

reboot
