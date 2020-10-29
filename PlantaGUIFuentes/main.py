import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QSpinBox, QApplication, QLineEdit, QListWidget, QMainWindow, QPushButton


class Ui(QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/main.ui', self)

        self.clients = []
        self.clientIndex = []

        self.days = self.findChild(QSpinBox, 'spinBox')

        self.NCaP = self.findChild(QLineEdit, "lineEdit")
        self.HCaP = self.findChild(QLineEdit, "lineEdit_2")
        self.TCaP = self.findChild(QLineEdit, "lineEdit_3")
        self.NCoP = self.findChild(QLineEdit, "lineEdit_6")
        self.HCoP = self.findChild(QLineEdit, "lineEdit_5")
        self.TCoP = self.findChild(QLineEdit, "lineEdit_4")

        self.clientList = self.findChild(QListWidget, "listWidget")
        self.clientRequest = self.findChild(QLineEdit, "lineEdit_7")
        self.addClientBtn = self.findChild(QPushButton, 'pushButton')

        self.solveBtn = self.findChild(QPushButton, 'pushButton_2')

        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle('Planta de energía')


        self.addClientBtn.clicked.connect(lambda: self.addClient())
        self.show()

    def addClient(self):
        cleanRequest = []
        clientRequest = self.clientRequest.text()
        request = clientRequest.split(',')
        for req in request:
            cleanRequest.append(req.strip())
        self.clients.append(cleanRequest)
        self.clientList.addItem(clientRequest)

def show():
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()


show()
