import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from .status_tab import StatusTab


class MainWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.setObjectName("main")
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.status = StatusTab()
        self.umts = QWidget()
        # self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.status, "Status")
        self.tabs.addTab(self.umts, "SIM")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(),
                  currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 480
        self.height = 320
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MainWidget(self)
        self.setCentralWidget(self.table_widget)
        self.setObjectName("main")

        self.show()


def runGui():
    app = QApplication(sys.argv)

    with open("styles.qss", 'r') as hd:
        styles = hd.read()
        app.setStyleSheet(styles)

    window = MainWindow()

    app.exec_()

if __name__ == "__main__":
    runGui()