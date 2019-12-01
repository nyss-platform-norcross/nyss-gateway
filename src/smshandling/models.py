
from base import Base
from sqlalchemy import Column, Integer, DateTime, Float, String, Boolean

class SMS(Base):
    __tablename__ = 'sms'

    id = Column(Integer, primary_key = True)
    dateReceived = Column('Date_Received', DateTime)
    dateHandled = Column('Date_Handled', DateTime)
    text = Column('Text', String)
    handled = Column('Handled', Boolean, default = False)
    number = Column('Number', String)


    def __str__(self):
        return "[Id: {} - Date Received: {} - Text: {} - Handled: {}]".format(self.id, self.dateReceived, self.text, self.handled)

