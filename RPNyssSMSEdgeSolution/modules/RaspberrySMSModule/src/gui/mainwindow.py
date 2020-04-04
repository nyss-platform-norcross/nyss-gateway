import PyQt5.QtCore as Qt
import PyQt5.QtWidgets as qtWidgets
import sys

class MainWindow(qtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")
        self.resize(480, 320)

        self.widget = qtWidgets.QWidget()
        self.mainlayout = qtWidgets.QHBoxLayout()
        self.widget.setLayout(self.mainlayout)


        label = qtWidgets.QLabel("This is a PyQt5 window!")
        self.mainlayout.addItem(label)
        # The `Qt` namespace has a lot of attributes to customise
        # widgets. See: http://doc.qt.io/qt-5/qt.html

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(self.widget)


if __name__ == "__main__":
    app = qtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()