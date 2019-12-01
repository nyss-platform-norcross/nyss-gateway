from smshandling.smsService import SmsService
import logging
import threading
import datetime
import uuid
import time

from .services import GSMAdapter, GSMStatus
class HuaweiAdapter(GSMAdapter):
    def __init__(self, smsService: SmsService, logger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.smsService = smsService
        self.log: logging.Logger = logger

        self.log.debug('Creating Huawei Reader')
        self.dummyThread = threading.Thread(
            name="Huawei SMS Reader", target=self._run, daemon=True)
        self.start()

    def start(self):
        self.dummyThread.start()

    def _run(self):
        while True:
            self.smsService.saveSMS(
                datetime.datetime.now(), str(uuid.uuid4()), "HUAWEI-0-000-000")
            time.sleep(1.)
