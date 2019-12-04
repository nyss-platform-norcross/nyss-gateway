from iocContainer import IocContainer
import logging
import sys
import os
from dependency_injector import providers

DATABASE_FILE_NAME = 'smsstore.db'

GSM_HANDLER_DUMMY = 'DUMMY'
GSM_HANDLER_HUAWEI = 'HUAWEI'

CONFIGURATION = {
    'database': {
        # 'url': 'sqlite://',
        'url': 'sqlite:///{}'.format(DATABASE_FILE_NAME),
    },
    'api': {
        'key': '409g43',
        'id': 'grwog230',
        'url': 'localhost',
    },
    'gsm': {
        'handler': GSM_HANDLER_HUAWEI,
    }
}

if __name__ == "__main__":
    needToCreateDatabase = False
    if os.path.exists(DATABASE_FILE_NAME) is False:
        needToCreateDatabase = True

    container = IocContainer(
        config=CONFIGURATION
    )
    container.logger().addHandler(logging.StreamHandler(sys.stdout))
    if needToCreateDatabase:
        container.createDatabase()
    container.gsm_adapter()
    container.api_publisher()
    container.main(*sys.argv[1:])
