import threading
import time 
import datetime
import uuid

from .huaweireader import HuaweiReader

class DummySMSReader:

    def __init__(self, smsService, *args, **kwargs):
        self.smsService = smsService
        self.dummyThread = threading.Thread(name="Dummy SMS Reader", target=self._run, daemon=True)
        self.start()


    def start(self):
        self.dummyThread.start()

    def _run(self):
        while True:
            self.smsService.saveSMS(datetime.datetime.now(), str(uuid.uuid4()), "DUMMY-0-000-000")
            time.sleep(1.)
    


def create_reader(reader_type: str, *args, **kwargs):
    if reader_type == 'DUMMY':
        return DummySMSReader(*args, **kwargs)
    elif reader_type == 'HUAWEI':
        return HuaweiReader(**kwargs)