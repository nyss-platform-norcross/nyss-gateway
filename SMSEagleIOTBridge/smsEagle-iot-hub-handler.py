import nyssIotBridge
import requests
import time
import logging
import os
import subprocess

# Python 3 needs to be installed on the SMSEagle to start this script, using "do-not-use_apt-get"
# do-not-use_apt-get update
# do-not-use_apt-get install python3
# do-not-use_apt-get install python3-pip
# pip3 install azure-iot-device

#The connection string can be found in azure iot hub 
conn_str = ""
login = ""
cred = ""

logging.basicConfig(
    filename='/var/log/iot-bridge-log.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

def send_sms(params):
    params["login"] = login
    params["pass"] = cred   
    return str(requests.get('https://localhost/index.php/http_api/send_sms', params=params, verify=False))

def ping_device(params):
    return str(time.time())

def reboot_device(params):
    os.system('reboot')
    return str("Rebooting in 1 minute.")

def get_local_ips(params):
    return str(subprocess.getoutput('hostname -I'))

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/iot-bridge-log.log', level=logging.DEBUG)
    nyssIotBridge.init(send_sms, ping_device, reboot_device, get_local_ips, conn_str)
    while True:
        time.sleep(1)

