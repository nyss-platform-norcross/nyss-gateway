import threading
import time
import datetime
import uuid

from .model import GSMStatus, RawSMS


class GSMAdapter:
    def __init__(self, *args, **kwargs):
        self._smsHandler = {}

    def addSMSHandler(self, callback) -> str:
        '''
            callback signature: (rawSMS: RawSMS)
            return : handlerId: str
                    Use this to unregister a sms handler
        '''
        handlerId = uuid.uuid4().hex
        self._smsHandler[handlerId] = callback

    def removeSMSHandler(self, handlerId: str):
        del self._smsHandler[handlerId]

    def isUnlocked(self) -> bool:
        raise NotImplementedError()

    def unlockWithPin(self, pin: str):
        raise NotImplementedError()

    def sendSMS(self, number: str, text: str, callback):
        raise NotImplementedError()

    def getStatus(self):
        raise NotImplementedError()


class DummyAdapter(GSMAdapter):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.dummyThread = threading.Thread(
            name="Dummy SMS Reader", target=self._run, daemon=True)
        self.dummyThread.start()

    def isUnlocked(self) -> bool:
        return True

    def unlockWithPin(self, pin: str):
        pass

    def sendSMS(self, number: str, text: str, callback):
        time.sleep(0.5)
        callback()

    def getStatus(self):
        return GSMStatus('1', 'DUMMY-Provider', True)

    def _run(self):
        while True:
            # text = str(uuid.uuid4())
            text = "1#1#1"
            sms = RawSMS("+0000000", datetime.datetime.utcnow(), text=text)
            for handler in self._smsHandler.keys():
                func = self._smsHandler[handler](sms)
            time.sleep(10.)
