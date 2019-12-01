import logging
import datetime
from sqlalchemy.orm import Session, Query
from .models import SMS

class SmsPersistentService:
    

    def __init__(self, logger: logging.Logger, sessionFactory):
        self.log = logger
        self.sessionFactory = sessionFactory


    def handleNewSMS(self, date: datetime.date, text: str, number: str):
        self.log.debug('Handleing new SMS. Date: {} - Text: {}'.format(date, text))
        
        smsObj = SMS()
        smsObj.dateReceived = date
        smsObj.text = text
        session: Session = self.sessionFactory()
        session.add(smsObj)
        session.commit()
        session.close()

    def getAllUnhandledSMS(self) -> [SMS]:
        session: Session = self.sessionFactory()
        smss = session.query(SMS).filter(SMS.handled == False).all()
        session.close()

        return smss

    def markSMSHandled(self, sms: SMS):
        assert sms.handled == False
        session: Session = self.sessionFactory()
        sms.handled = True
        sms.dateHandled = datetime.datetime.now()
        session.add(sms)
        session.commit()
        session.close()
        