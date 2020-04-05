from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QGridLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import pyqtgraph as pg
import numpy as np

class StatusTab(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()

        self.layout = QGridLayout(self)
        self.sms_received_chart = pg.PlotWidget(self)
        self.sms_received_chart1 = pg.PlotWidget(self)
        self.sms_received_chart2 = pg.PlotWidget(self)
        self.sms_received_chart3 = pg.PlotWidget(self)

        self.layout.addWidget(self.sms_received_chart, 0, 0)
        self.layout.addWidget(self.sms_received_chart1, 1, 0)
        self.layout.addWidget(self.sms_received_chart2, 0, 1)
        self.layout.addWidget(self.sms_received_chart3, 1, 1)

        self.x = np.arange(24)
        self.y = np.linspace(0, 100, 24)

        bars = pg.BarGraphItem(x=self.x, height=self.y, width=0.4)
        bars1 = pg.BarGraphItem(x=self.x, height=self.y, width=0.4)
        bars2 = pg.BarGraphItem(x=self.x, height=self.y, width=0.4)
        bars3 = pg.BarGraphItem(x=self.x, height=self.y, width=0.4)
        self.sms_received_chart.addItem(bars)
        self.sms_received_chart1.addItem(bars1)
        self.sms_received_chart2.addItem(bars2)
        self.sms_received_chart3.addItem(bars3)
        
        
