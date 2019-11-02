import threading
import huaweiSmsHandler  # TODO: needs to be changed to gsmadapter is ready
import sendToApiHandler
import time
import frontend
import gsmadapter
import logging

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
log = logging.getLogger('WebServer')
log.setLevel(logging.DEBUG)


def startSmsHandler():
    log.debug("Starting SMS Handler!")
    required = True
    count = 0
    log.debug("Entering SMS Handler loop")
    while gsmadapter.isPinRequired() and not gsmadapter.isDeviceReady():
        log.debug("SMS Handler waiting...")
    huaweiSmsHandler.runSMSHandler()


def startSmsToCbsPlatformHandler():
    log.debug("Starting SMS to CBS platform handler")
    sendToApiHandler.runSendToApiHandler()


smsHandlerThread = threading.Thread(target=startSmsHandler, daemon=True)
smsToCbsPlatformThread = threading.Thread(
    target=startSmsToCbsPlatformHandler, daemon=True)


def startFronted():
    while not gsmadapter.isDeviceReady():
        log.debug("Wating for Device...")
        time.sleep(5)

    log.debug("Checking if pin required")
    if gsmadapter.isPinRequired():
        log.debug("Pin required!")
        frontend.PinEnterWindow()
    log.debug("Starting Status Window")
    frontend.StatusWindow()


frontendThread = threading.Thread(target=startFronted, daemon=True)
smsHandlerThread = threading.Thread(target=startSmsHandler, daemon=True)

frontendThread.start()
smsHandlerThread.start()
smsToCbsPlatformThread.start()
while True:
    try:
        time.sleep(1.)
    except KeyboardInterrupt as err:
        raise err
