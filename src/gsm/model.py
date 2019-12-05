import datetime



class GSMStatus:
    def __init__(self, signalStrength, providerName, available):
        self.signalStrength = signalStrength
        self.available = available
        self.providerName = providerName


class RawSMS:

    def __init__(self, phone: str, date: datetime.datetime, text: str):
        self.phone: str = phone
        self.date: datetime.datetime = date
        self.text: str = text
