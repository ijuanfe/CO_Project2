import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QSpinBox, QApplication, QLineEdit, QPushButton, QMainWindow


class Ui(QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/main.ui', self)

        self.days = self.findChild(QSpinBox, 'spinBox')

        self.NCaP = self.findChild(QLineEdit, "lineEdit")
        self.HCaP = self.findChild(QLineEdit, "lineEdit_2")
        self.TCaP = self.findChild(QLineEdit, "lineEdit_3")
        self.NCoP = self.findChild(QLineEdit, "lineEdit_6")
        self.HCoP = self.findChild(QLineEdit, "lineEdit_5")
        self.TCoP = self.findChild(QLineEdit, "lineEdit_4")

        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle('GUI')
        self.show()


def show():
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()


show()
