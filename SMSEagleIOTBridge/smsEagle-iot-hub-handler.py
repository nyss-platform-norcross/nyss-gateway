import nyssIotBridge
import requests
import time
import logging
import os
import subprocess
import sys
import threading

# Python 3 needs to be installed on the SMSEagle to start this script, using "do-not-use_apt-get"
# do-not-use_apt-get update
# do-not-use_apt-get install python3
# do-not-use_apt-get install python3-pip
# pip3 install azure-iot-device

logging.basicConfig(
    filename='/var/log/iot-bridge-log.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.WARNING,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("iot-hub-bridge")

def get_sys_arg(i):
    return sys.argv[i] if i < len(sys.argv) else None


def get_env_var(key):
    try:
        return os.environ[key]
    except Exception as e:
        logger.error("Environment variable " + key + " not found!")
        raise


# The connection string can be found in azure iot hub
IOT_HUB_CONNECTIONSTRING = get_sys_arg(1) or get_env_var("IOT_HUB_CONNECTIONSTRING")
SMSEAGLE_USERNAME = get_sys_arg(2) or get_env_var("SMSEAGLE_USERNAME")
SMSEAGLE_PWD = get_sys_arg(3) or get_env_var("SMSEAGLE_PWD")


def send_sms(params):
    params["login"] = SMSEAGLE_USERNAME
    params["pass"] = SMSEAGLE_PWD
    return str(requests.get('https://localhost/index.php/http_api/send_sms', params=params, verify=False, timeout=30))


def ping_device(params):
    return "I am alive!"

def handle_reboot():
    time.sleep(5)
    os.system('reboot')

def reboot_device(params):
    # handle reboot on a new thread in order to respond to azure before rebooting
    reboot_thread = threading.Thread(target=handle_reboot)
    reboot_thread.start()
    return str("Device is rebooting.")


def get_local_ips(params):
    return str(subprocess.getoutput('hostname -I'))

def get_iot_hub_handler_version(params):
    version = open('/home/pi/iot-hub-handler-version.txt', 'r')
    return str(version)


if __name__ == "__main__":
    methods = {
        'send_sms': send_sms,
        'ping_device': ping_device,
        'reboot_device': reboot_device,
        'get_local_ips': get_local_ips,
        'get_iot_hub_handler_version': get_iot_hub_handler_version
    }

    nyssIotBridge.init(IOT_HUB_CONNECTIONSTRING, methods)
    while True:
        time.sleep(1)
