
import subprocess
import os

def tryConnectToWiFi(ssid: str, password: str):

    with os.open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w+') as handle:
        handle.write('network={\n    ssid=\"' + ssid + '\"\n    psk=\"' + password + '\"\n}\n')
    subprocess.check_output(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'])



