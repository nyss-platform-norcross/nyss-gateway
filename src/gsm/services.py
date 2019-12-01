import threading
import time 
import datetime
import uuid


class DummySMSReader:

    def __init__(self, smsHandler):
        self.smsHandler = smsHandler
        self.dummyThread = threading.Thread(name="Dummy SMS Reader", target=self._run, daemon=True)
        self.start()


    def start(self):
        self.dummyThread.start()

    def _run(self):
        while True:
            self.smsHandler.handleNewSMS(datetime.datetime.now(), str(uuid.uuid4()), "0-000-000")
            time.sleep(1.)
    
