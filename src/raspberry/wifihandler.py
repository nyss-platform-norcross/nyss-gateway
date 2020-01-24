# from gsm import SmsListener, RawSMS
import os
import logging
import subprocess

_log = logging.getLogger("WIFI-Handler")


def _write_to_wpa_suuplicant(ssid: str, password: str):
    wifiConfig = '\nnetwork={{\n    ssid="{}"\n    psk="{}"\n}}\n'.format(
        ssid, password)

    with open("/etc/wpa_supplicant/wpa_supplicant.conf", 'a+') as wpa:
        wpa.write(wifiConfig)
    subprocess.run(["wpa_cli", "-i", "wlan0", "reconfigure"])


def addNewWifiSettings(ssid: str, password: str):
    _log.debug("Trying to add wifi configuration: {}:{}".format(ssid, password))

    if ssid.find('"') != -1:
        raise ValueError(
            "SSID may not contain quotation marks for security reasons")
    if password.find('"') != -1:
        raise ValueError(
            "WiFi passsword may not contain quotation marks for security reasons")

    _write_to_wpa_suuplicant(ssid, password)

    _log.debug("Wifi Settings added")


# @SmsListener
# def handleWifiSMS(sms: RawSMS):
#     if sms.text.startswith('WIFI:'):
#         parts = sms.text.split(':')
#         ssid = parts[1]
#         password = parts[2]
#         addNewWifiSettings(ssid, password)
#     else:
#         return
