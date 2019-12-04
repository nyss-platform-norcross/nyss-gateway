import threading
import time 
import datetime
import uuid

class GSMStatus:
    def __init__(self, signalStrength, providerName, available):
        self.signalStrength = signalStrength
        self.available = available
        self.providerName = providerName

class GSMAdapter:
    def __init__(self):
        super().__init__()
    
    def addSMSHandler(self, callback) -> str:
        '''
            callback signature: (phoneNumber: str, text: str, timestamp: datetime.datetime)
            return : handlerId: str
                    Use this to unregister a sms handler
        '''
        raise NotImplementedError('This is a Metaclass')

    def removeSMSHandler(self, id: str):
        raise NotImplementedError()

    def isUnlocked(self) -> bool:
        raise NotImplementedError()

    def unlockWithPin(self, pin: str):
        raise NotImplementedError()

    def sendSMS(self, number: str, text: str, callback):
        raise NotImplementedError()

    def getStatus(self):
        raise NotImplementedError()


class DummyAdapter(GSMAdapter):

    def __init__(self, smsService, *args, **kwargs):
        super().__init__()
        self.smsService = smsService
        self.dummyThread = threading.Thread(name="Dummy SMS Reader", target=self._run, daemon=True)
        self.dummyThread.start()


    def isUnlocked(self):
        return True

    def unlockWithPin(self, pin):
        return True

    def sendSMS(self, callback):
        callback()
    
    def _run(self):
        while True:
            self.smsService.saveSMS(datetime.datetime.now(), str(uuid.uuid4()), "DUMMY-0-000-000")
            time.sleep(1.)
    


