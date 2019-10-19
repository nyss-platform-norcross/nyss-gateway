
import subprocess

def tryConnectToWiFi(ssid: str, password: str):
    subprocess.check_output(['ifdown', 'wlan0'])
    subprocess.check_output(['wpa_supplicant', '-d', '-c', ''])
    pass


