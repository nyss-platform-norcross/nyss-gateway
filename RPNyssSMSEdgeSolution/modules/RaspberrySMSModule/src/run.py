import logging
import sys
import os
from iocContainer import initialize

DATABASE_FILE_NAME = os.getenv('DATABASE', 'smsstore.db')

GSM_HANDLER_DUMMY = 'DUMMY'
GSM_HANDLER_HUAWEI = 'HUAWEI'

CONFIGURATION = {
    'database': {
        # 'url': 'sqlite://',
        'url': 'sqlite:///{}'.format(DATABASE_FILE_NAME),
        'file': DATABASE_FILE_NAME
    },
    'api': {
        'key': os.getenv('NYSS_API_KEY', 'dummykey'),
        'id': os.getenv('NYSS_API_ID', '1'),
        'url': os.getenv('NYSS_API_URL', 'http://localhost'),
    },
    'gsm': {
        'handler': GSM_HANDLER_HUAWEI,
        # 'handler': GSM_HANDLER_DUMMY,
    }
}

if __name__ == "__main__":
    initialize(CONFIGURATION)
