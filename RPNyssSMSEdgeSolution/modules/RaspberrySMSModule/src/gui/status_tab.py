from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QGridLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QTimer
import pyqtgraph as pg
import numpy as np
import datetime
import time
import math
import random


def timestamp():
    return int(time.mktime(datetime.datetime.now().timetuple()))


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time', units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        return [datetime.datetime.fromtimestamp(value).strftime("%H:%M") for value in values]

class StatusTab(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()

        self.layout = QGridLayout(self)
        self._create_net_info()
        self._create_received_chart()
        
        
    def _create_net_info(self):
        self._net_label = QLabel("IP: 192.168.178.1 | WiFi: DasHier | Id: 1650346", self)

        self.layout.addWidget(self._net_label, 0, 0)
        

    def _create_received_chart(self):
        self.sms_received_chart = pg.PlotWidget(self, axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.layout.addWidget(self.sms_received_chart, 1, 0)

        self.x = np.arange(24)
        self.y = np.linspace(0, 100, 24)

        # bars = pg.BarGraphItem(x=np.arange(24), height=np.zeros((24)), width=0.4)

        # self.sms_received_chart.addItem(bars)
        a = 0

        plottedItems = []

        def updater():
            nonlocal a
            a += 1
            smsSuccess = random.randint(10, 100)
            smsError = random.randint(0, 2)

            x = timestamp()
            x0 = x - 0.4
            x1 = x + 0.4
            success = pg.BarGraphItem(x0=[x0], x1=[x], height=[smsSuccess], brush="g")
            errors =  pg.BarGraphItem(x0=[x], x1=[x1], height=[smsError], brush="r")
            self.sms_received_chart.addItem(errors)
            self.sms_received_chart.addItem(success)
            plottedItems.append((success, errors))
            if (len(plottedItems) > 24):
                items = plottedItems.pop(0)
                self.sms_received_chart.removeItem(items[0])
                self.sms_received_chart.removeItem(items[1])

        for i in range(24):
            updater()
        timer = QTimer(self)
        timer.timeout.connect(updater)
        timer.start(1000)


