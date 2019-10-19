#!/usr/bin/env python

"""\
Demo: handle incoming SMS messages by replying to them

Simple demo app that listens for incoming SMS messages, displays the sender's number
and the messages, then replies to the SMS by saying "thank you"
"""

from __future__ import print_function

import logging
import time
import Queue

from gsmmodem.modem import GsmModem

PORT = '/dev/ttyS0'
BAUDRATE = 115200
PIN = None # SIM card PIN (if any)
q = Queue.Queue()
index = 0

# checks if Pin is required at all
def isPinRequired(): 
    pass

# pin wird eingegeben und pin abfrage deaktivierts
def unlockWithPin(pin): 
    pass

def handleSms(sms):
    print(u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(sms.number, sms.time, sms.text))
    print('Replying to SMS...')
    sms.reply(u'SMS received: "{0}{1}"'.format(sms.text[:20], '...' if len(sms.text) > 20 else ''))
    message = {
        "index": index,
        "content": sms.text,
        "phone": sms.number
    }
    q.put(message)
    index += 1
    print('SMS sent.\n')

def getUnreadMessageCount():
    return q.qsize()

def getFirstUnreadMessage():
    return q.get()

def deleteMessage(): # not necessary here, because messages taken of the queue are deleted automatically
    pass 

def sendMessage(apiData): #TODO
    pass

def initializeModem():
    print('Initializing modem...')
    # Uncomment the following line to see what the modem is doing:
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    modem.smsTextMode = False
    modem.connect(PIN)
    print('Waiting for SMS message...')
    while True:
        time.sleep(3)  
        modem.rxThread.join(2**31) # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal
    modem.close()