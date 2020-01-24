import subprocess
import json

def _parseIpStatus(iface):
    status = {}
    status['ifname'] = iface['ifname']
    if "addr_info" in iface:
        for addrinfo in iface['addr_info']:
            status[addrinfo['family']] = addrinfo['local']

    return status

def getInterfaceStatus():
    status = []
    result = subprocess.run(["ip", "-j", "addr", "show"], capture_output = True, text=True)
    resultStr = str(result.stdout)
    data = json.loads(resultStr)
    for iface in data:
        print(iface['ifname'])
        if iface['ifname'] == 'wlan0' or iface['ifname'] == 'eth0':
            status.append(_parseIpStatus(iface))
    print(status)

from wifihandler import addNewWifiSettings

if __name__ == "__main__":
    addNewWifiSettings("DasHier", "allesgrossgeschrieben")
    # getInterfaceStatus()