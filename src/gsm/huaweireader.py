from smshandling.smsPersistentService import SmsPersistentService
import logging


class HuaweiReader:
    def __init__(self, smsHandler: SmsPersistentService, logger):
        self.smsHandler = smsHandler
        self.log: logging.Logger = logger

        self.log.debug('Creating Huawei Reader')
