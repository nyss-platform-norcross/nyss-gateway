import logging
import datetime
import random


class ApiPublisher:
    def __init__(self, API_URL: str, API_ID: str, API_KEY: str, logger):
        self.log: logging.Logger = logger
        self.log.debug(
            'Creating APIPublisher... with API_URL="{}" -  API_ID="{}" - API_KEY="{}"'.format(API_URL, API_ID, API_KEY))

    def publish(self, id: int, date: datetime.datetime, text: str):
        if random.randint(0, 1) > 0:
            self.log.debug(
                'Publishing SMS top API: ID:{} Date:{} Text:{}'.format(id, date, text))
        else:
            raise IOError('Failed to connect tu API')
