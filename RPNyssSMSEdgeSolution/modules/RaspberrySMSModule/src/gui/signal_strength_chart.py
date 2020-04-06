import pyqtgraph as pg
from PyQt5.QtCore import pyqtSlot, QTimer
import datetime
import time
from .chart_utils import TimeAxisItem, timestamp
import random


class LinearTimeValueChart(pg.PlotWidget):

    def __init__(self, parent=None, background='default', **kargs):
        super().__init__(parent=parent, background=background,  axisItems={
            'bottom': TimeAxisItem(orientation='bottom')}, **kargs)

        timer = QTimer(self)

            
        timer.timeout.connect(self.test)
        timer.start(500)

    def test(self):
        self.add_data_point(float(random.randint(0, 4)))

    def add_data_point(self, value: float):
        item = pg.ScatterPlotItem(x=[timestamp()], y=[value], pen='g')
        self.addItem(item)
