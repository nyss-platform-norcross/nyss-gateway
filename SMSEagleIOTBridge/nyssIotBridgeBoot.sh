#!/bin/sh
echo "Updating IoT Hub handler script"

curl -s -o /home/pi/smsEagle-iot-hub-handler.py https://raw.githubusercontent.com/nyss-platform-norcross/nyss-sms-gateway/feature/update-handler-script/SMSEagleIOTBridge/smsEagle-iot-hub-handler.py
res=$?
if test "$res" != "0"
then
    echo "Failed to update IoT Hub handler script"
else
    chmod +x /home/pi/smsEagle-iot-hub-handler.py
    echo "Successfully updated IoT Hub handler script"
    # save script version as latest commit id
    curl -s https://api.github.com/repos/nyss-platform-norcross/nyss-sms-gateway/commits/feature/update-handler-script | python3 -c "import sys, json; print(json.load(sys.stdin)['sha'])" > /home/pi/iot-hub-handler-version.txt
fi

until ping -c1 azure.microsoft.com;
do sleep 5;
done;