from .smsPersistentService import SmsPersistentService
from threading import Thread
from time import sleep
import logging
from .models import SMS


class SmsPublisherService:
    def __init__(self, smsPersistentService: SmsPersistentService, publisher, logger):
        self.storage = smsPersistentService
        self.publisher = publisher
        self.log: logging.Logger = logger

        self.checkThread = Thread(
            name="SMSPublisher", target=self._publisherLoop, daemon=True)
        self.smsPersistentService = smsPersistentService
        self.start()

    def start(self):
        self.checkThread.start()

    def _publisherLoop(self):
        while True:
            self._trypublishUnhandledSMS()
            sleep(1.0)

    def _trypublishUnhandledSMS(self):
        toHandle = self.storage.getAllUnhandledSMS()

        for sms in toHandle:
            sms: SMS
            self.log.debug('Trying to publish SMS to API: {}'.format(sms))
            try:
                self.publisher.publish(sms.id, sms.dateReceived, sms.text)
                self.smsPersistentService.markSMSHandled(sms)
            except:
                self.log.warn('Failed to publish SMS...', exc_info=True)
