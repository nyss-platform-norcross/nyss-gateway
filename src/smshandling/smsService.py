

import datetime
import logging

from .models import SMS


class SmsService:

    def __init__(self, logger: logging.Logger, sessionFactory):
        self.log = logger
        self.session = sessionFactory

    def saveSMS(self, date: datetime.date, text: str, number: str):
        self.log.debug(
            'Handleing new SMS. Date: {} - Text: {}'.format(date, text))
        smsObj = SMS()
        smsObj.dateReceived = date
        smsObj.text = text
        smsObj.number = number
        session: Session = self.session()
        session.add(smsObj)
        session.commit()
        session.close()

    def getAllUnhandledSMS(self):
        session: Session = self.session()
        smss = session.query(SMS).filter(SMS.handled == False).all()
        session.close()

        return smss

    def markSMSHandled(self, sms: SMS):
        if sms.handled == True:
            self.log.warn('SMS already marked handled!!!{}'.format(sms))
        session: Session = self.session()
        sms.handled = True
        sms.dateHandled = datetime.datetime.now()
        session.add(sms)
        session.commit()
        session.close()
