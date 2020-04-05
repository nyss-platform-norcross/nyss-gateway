import datetime
from smshandling.models import SMS
from base import Base
from time import sleep
from gsm import SmsListener
from gui import runGui

def createDatabase(engine):
    print('creating database tables')
    Base.metadata.create_all(engine)
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config("alembic.ini")
    command.stamp(alembic_cfg, "head")


def main(gsm_adapter, save_service):
    print("Main started...")
    runGui(gsm_adapter)
    # sleep(10)
    # for sms in save_service.getAllUnhandledSMS():
    #     print("Unhandeld SMS: {}".format(sms))
    # publisher._trypublishUnhandledSMS()
