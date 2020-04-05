import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from .status_tab import StatusTab
import re


class MainWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.setObjectName("main")
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.status = StatusTab()
        self.umts = QWidget()

        self.footer_label = QLabel("NYSS-Redcross SMS-Gateway. Version: 0.0.1-SNAPSHOT")
        self.footer_label.setObjectName("footer")
        # self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.status, "Status")
        self.tabs.addTab(self.umts, "SIM")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.layout.addWidget(self.footer_label)
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

def loadStylesSheet() -> str:
    with open("gui/styles.qss", 'r') as hd:
        lines = hd.readlines()

        styleWithoutVariables = []

        variables = []
        for line in lines:
            groups = re.findall(r'^(\$[a-zA-Z-]+):\s+(.*);$', line)
            if (len(groups) == 1) and len(groups[0]) == 2:
                variables.append((groups[0][0].replace('$', '\$'), groups[0][1]))
            else:
                styleWithoutVariables.append(line)

        finalLines = []
        for line in styleWithoutVariables:
            for variable in variables:
                line = re.sub(variable[0], variable[1], line)
            finalLines.append(line)
    return "\n".join(finalLines)


def runGui():
    app = QApplication(sys.argv)

    app.setStyleSheet(loadStylesSheet())

    window = MainWindow()

    app.exec_()


if __name__ == "__main__":
    runGui()
