from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QGridLayout, QLabel, QHBoxLayout, QFormLayout, QDialog, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QTimer, QDirIterator
from PyQt5.QtCore import Qt
import functools
from .view_controller import ViewController
from .signal_strength_chart import LinearTimeValueChart
from gsm import GSMStatus


class SimTab(QWidget):
    def __init__(self, view_controller: ViewController, parent=None):
        super().__init__(parent=parent)
        self.layout = QGridLayout(self)

        self._gsm_status: GSMStatus

        self._createGSMStatus()

        chart = LinearTimeValueChart(self)
        self.layout.addWidget(chart)
        self._create_sim_unlock()

        view_controller.gsmstatus.connect(self.gsm_status)
        self.view_controller = view_controller

    def _createGSMStatus(self):
        gsmStatusWidget = QWidget(self)
        layout = QFormLayout()
        gsmStatusWidget.setLayout(layout)
        gsmStatusWidget.setObjectName("gsmstatus")
        self.layout.addWidget(gsmStatusWidget, 0, 0)

        self._available_label = QLabel("Unknown")
        self._available_label.setObjectName("status")
        self._provider_name_label = QLabel("Unknown")
        self._provider_name_label.setObjectName("status")
        self._signal_strength_label = QLabel("Unknown")
        self._signal_strength_label.setObjectName("status")

        layout.addRow(QLabel("Available"), self._available_label)
        layout.addRow(QLabel("Provider"), self._provider_name_label)
        layout.addRow(QLabel("Signal Strength"), self._signal_strength_label)

    @pyqtSlot(GSMStatus)
    def gsm_status(self, status: GSMStatus):
        self._available_label.setText(status.available)
        self._provider_name_label.setText(status.providerName)
        self._signal_strength_label.setText(status.signalStrength)
        if status.available == 'Pin Required':
            self._unlock_button.setEnabled(True)
        else:
            self._unlock_button.setEnabled(False)

    def _create_sim_unlock(self):
        self._unlock_button = QPushButton(self)
        self._unlock_button.setText("Enter SIM Pin")
        self._unlock_button.setObjectName("primary")
        self._unlock_button.clicked.connect(self._on_sim_unlock)
        self._unlock_button.setEnabled(False)
        self.layout.addWidget(self._unlock_button)

    def _on_sim_unlock(self):
        dlg = QDialog(self)
        dlg.setWindowFlag(Qt.FramelessWindowHint)

        layout = QVBoxLayout()
        dlg.setLayout(layout)

        lineEdit = QLineEdit()
        lineEdit.setReadOnly(True)
        layout.addWidget(lineEdit, stretch=1)

        numberWidget = QWidget()
        number = QGridLayout()
        numberWidget.setLayout(number)

        def click(value):
            nonlocal i, j, lineEdit
            lineEdit.setText("{}{}".format(lineEdit.text(), value))

        def delete():
            lineEdit.setText(lineEdit.text()[:-1])
        for i in range(4):
            for j in range(3):
                value = i * 3 + j
                if value < 9:
                    btn = QPushButton("{}".format(i * 3 + j))
                    number.addWidget(btn, i, j)

                    btn.clicked.connect(functools.partial(click, i * 3 + j))
                    btn.setObjectName("number")
                if value == 11:
                    btn = QPushButton("DEL")
                    number.addWidget(btn, i, j)
                    btn.clicked.connect(delete)
                    btn.setObjectName("number")
                if value == 10:
                    btn = QPushButton("{}".format(9))
                    number.addWidget(btn, i, j)

                    btn.clicked.connect(functools.partial(click, 9))
                    btn.setObjectName("number")

        layout.addWidget(numberWidget)

        actionsWidget = QWidget()
        actions = QHBoxLayout()
        actionsWidget.setLayout(actions)
        layout.addWidget(actionsWidget)

        cancel_button = QPushButton(dlg)
        cancel_button.setText("Cancel")
        actions.addWidget(cancel_button)

        ok_button = QPushButton(dlg)
        ok_button.setObjectName("primary")
        ok_button.setText("Accept")
        actions.addWidget(ok_button)

        def ok_click():
            self.view_controller.submit_pin(lineEdit.text())
            dlg.close()

        def cancel_click():
            dlg.close()

        ok_button.clicked.connect(ok_click)
        cancel_button.clicked.connect(cancel_click)

        dlg.exec_()
