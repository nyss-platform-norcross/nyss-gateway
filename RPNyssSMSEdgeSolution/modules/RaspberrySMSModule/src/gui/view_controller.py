from PyQt5.QtCore import pyqtSlot, pyqtSignal, QTimer, QThread
from PyQt5.QtWidgets import QWidget
from gsm import GSMAdapter, GSMStatus
import time

class GSMStatusUpdater(QThread):

    status = pyqtSignal(GSMStatus)

    def __init__(self, gsm: GSMAdapter):
        super().__init__()
        self.gsm = gsm

    def run(self):
        while True:
            self.status.emit(self.gsm.getStatus())
            time.sleep(1.5)


class ViewController(QWidget):

    gsmstatus = pyqtSignal(GSMStatus)

    def __init__(self, gsmAdpter: GSMAdapter):
        super().__init__()
        self._gsmadapter = gsmAdpter

        self.status_thread = GSMStatusUpdater(gsmAdpter)
        self.status_thread.status.connect(self.gsmstatus)
        self.status_thread.start()

    def submit_pin(self, pin):
        self._gsmadapter.unlockWithPin(pin)


