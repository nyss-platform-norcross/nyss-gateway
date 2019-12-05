import datetime
import logging
import random
import threading
from time import sleep

from smshandling.models import SMS
from smshandling.smsService import SmsService


class ApiPublisher:
    def __init__(self, API_URL: str, API_ID: str, API_KEY: str, smsService: SmsService, logger):
        self.log: logging.Logger = logger
        self.smsService = smsService
        self.log.debug(
            'Creating APIPublisher... with API_URL="{}" -  API_ID="{}" - API_KEY="{}"'.format(API_URL, API_ID, API_KEY))

        self.publisherThread = threading.Thread(
            name="API Publisher Thread", daemon=True, target=self._publishLoop)
        self.publisherThread.start()

    def publish(self, id: int, date: datetime.datetime, text: str):
        self.log.debug(
            'Publishing SMS top API: ID:{} Date:{} Text:{}'.format(id, date, text))

    def _publishLoop(self):
        while True:
            self._trypublishUnhandledSMS()
            sleep(1.0)

    def _trypublishUnhandledSMS(self):
        toHandle = self.smsService.getAllUnhandledSMS()
        count = 0
        for sms in toHandle:
            sms: SMS
            self.log.debug('Trying to publish SMS to API: {}'.format(sms))
            try:
                self.publish(sms.id, sms.dateReceived, sms.text)
                self.smsService.markSMSHandled(sms)
            except:
                self.log.warn('Failed to publish SMS...', exc_info=True)
