import nyssIotBridge
import requests
import time
import logging

# Python 3 needs to be installed on the SMSEagle to start this script, using "do-not-use_apt-get"

#The connection string can be found in azure iot hub 
conn_str = ""

def send_sms(params):
    return str(requests.get('https://localhost/index.php/http_api/send_sms', params=params, verify=False))

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/iot-bridge-log.log', level=logging.DEBUG)
    nyssIotBridge.init(send_sms, "")
    while True:
        time.sleep(1)

