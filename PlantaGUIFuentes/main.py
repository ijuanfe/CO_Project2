import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QComboBox, QPushButton, QMainWindow


class Ui(QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/main.ui', self)
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle('GUI')
        self.show()


def show():
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()


show()
