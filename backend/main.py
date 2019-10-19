import threading
import time
import frontend
import gsmadapter

import logging


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
log = logging.getLogger('WebServer')
log.setLevel(logging.DEBUG)

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

# def startSmsHandler():
#     log.debug("Starting SMS Handler!")
#     required = True
#     count = 0
#     while huaweiaccess.isPinRequired() or required:
#     # while required:
#         time.sleep(1)
#         count = count + 1
#         if count == 5:
#             required = False
#     log.debug("Entering SMS Handler loop")
#     smsHandler.runSMSHandler()


# httpServer = threading.Thread(target=startHttpServer, daemon=True)
frontendThread = threading.Thread(target=startFronted, daemon=True)
# smsHandlerThread = threading.Thread(target=startSmsHandler, daemon=True)

# httpServer.start()
frontendThread.start()
# smsHandlerThread.start()
# httpServer.join()
while True:
    try:
        time.sleep(1.)
    except KeyboardInterrupt as err:
        raise err

# if __name__ == "__main__":
    # log.debug('Starting SMS Gateway backend application')
