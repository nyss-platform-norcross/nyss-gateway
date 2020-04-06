import pyqtgraph as pg
from PyQt5.QtCore import pyqtSlot
import datetime

from .chart_utils import timestamp, TimeAxisItem



class SmsReceivingChart(pg.PlotWidget):

    def __init__(self, parent=None, background='default', **kargs):
        super().__init__(parent=parent, background=background, axisItems={
            'bottom': TimeAxisItem(orientation='bottom')}, **kargs)

        self._lastHour = datetime.datetime.now().hour
        self._currentTimestmap = timestamp()
        self._plottedItems = []
        self._current_hour_values = (0, 0)


        self.setTitle("SMS Receiving")
        # self.setLabel('left', 'Count')
        self.getAxis('left').setWidth(30)
        self.getAxis('bottom').setHeight(25)

        self.setMouseEnabled(False, False)


    @pyqtSlot(int, int)
    def update(self, sms_success: int, sms_error: int):

        currentHour = lastHour = datetime.datetime.now().hour

        if (currentHour > lastHour):
            lastHour = currentHour
            self._currentTimestmap = timestamp()
            self._current_hour_values = (sms_success, sms_error)
        else:
            self._current_hour_values = (
                self._current_hour_values[0] + sms_success, self._current_hour_values[1] + sms_error)
            if (len(self._plottedItems) > 0):
                currentItem = self._plottedItems.pop()  # Remove current hour to update it
                self.removeItem(currentItem[0])
                self.removeItem(currentItem[1])

        x = self._currentTimestmap
        x0 = x - 0.4
        x1 = x + 0.4

        success = pg.BarGraphItem(x0=[x0], x1=[x], height=[
                                  self._current_hour_values[0]], brush="g")
        errors = pg.BarGraphItem(x0=[x], x1=[x1], height=[
                                 self._current_hour_values[1]], brush="r")
        self.addItem(errors)
        self.addItem(success)


        self._plottedItems.append((success, errors))
        if (len(self._plottedItems) > 24):
            items = self._plottedItems.pop(0)
            self.removeItem(items[0])
            self.removeItem(items[1])


