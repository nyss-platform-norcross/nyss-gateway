from gsm import SmsListener, RawSMS

def _addNewWifiSettings(ssid: str, password: str):
    print("Adding new Wifi. SSID={} - Password={}".format(ssid, password))


@SmsListener
def handleWifiSMS(sms: RawSMS):
    if sms.text.startswith('WIFI:'):
        parts = sms.text.split(':')
        ssid = parts[1]
        password = parts[2]
        _addNewWifiSettings(ssid, password)
    else:
        return



