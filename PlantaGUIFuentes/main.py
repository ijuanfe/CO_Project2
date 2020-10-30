import os
import sys
from PyQt5 import uic
from shutil import copyfile
from config import MINIZINC_EXECUTABLE_PATH
from PyQt5.QtWidgets import QSpinBox, QApplication, QLineEdit, QListWidget, QMainWindow, QPushButton, \
    QPlainTextEdit, QTextEdit

class Central:

    def __init__(self, CaP, CoP):
        self.CaP = CaP
        self.CoP = CoP


class Ui(QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/main.ui', self)

        self.centrals = []
        self.clients = []

        self.days = self.findChild(QSpinBox, 'spinBox')

        self.centralList = self.findChild(QListWidget, "listWidget_2")
        self.CentralCaP = self.findChild(QLineEdit, "lineEdit")
        self.CentralCoP = self.findChild(QLineEdit, "lineEdit_2")
        self.CentralName = self.findChild(QLineEdit, "lineEdit_3")
        self.addCentralBtn = self.findChild(QPushButton, 'pushButton_3')

        self.clientList = self.findChild(QListWidget, "listWidget")
        self.clientRequest = self.findChild(QLineEdit, "lineEdit_7")
        self.addClientBtn = self.findChild(QPushButton, 'pushButton')

        self.solveBtn = self.findChild(QPushButton, 'pushButton_2')
        self.output = self.findChild(QTextEdit, "textEdit")

        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle('Planta de energía')

        self.addCentralBtn.clicked.connect(lambda: self.addCentral())
        self.addClientBtn.clicked.connect(lambda: self.addClient())
        self.solveBtn.clicked.connect(lambda: self.runMinizinc())
        self.show()

    def addCentral(self):
        central = Central(
            CaP=self.CentralCaP.text(),
            CoP=self.CentralCoP.text(),
        )
        self.centrals.append(central)
        self.centralList.addItem(
            self.CentralName.text() + " >> " + str(self.CentralCaP.text()) + " - CoP " + str(self.CentralCoP.text())
        )

    def addClient(self):
        cleanRequest = []
        clientRequest = self.clientRequest.text()
        request = clientRequest.split(',')
        for req in request:
            cleanRequest.append(req.strip())
        self.clients.append(cleanRequest)
        self.clientList.addItem(clientRequest)

    def runMinizinc(self):
        f = open("model/data.dzn", "r")
        f.write(self.witeInput())
        command = MINIZINC_EXECUTABLE_PATH + " --solver coinbc " + " ../PlantaEnergia/PlantaEnergia.mzn > out.log"
        os.system(command)
        f = open("out.log", "r")
        self.output.setPlainText(f.read())

    def witeInput(self):

        CaP = str(self.NCaP.text()) + ".0, " +  str(self.HCaP.text()) + ".0, " +  str(self.TCaP.text()) + ".0 "
        CoP = str(self.NCoP.text()) + ".0, " + str(self.HCoP.text()) + ".0, " + str(self.TCoP.text()) + ".0 "

        return """
            Nc = 3;
            S = """ + str(self.clients.__len__()) + """;
            n = """ + str(self.days.text()) + """;
            CaP = [""" + CaP + """];
            CoP = [""" + CoP + """];
            d = array2d (1..S, 1..n,
                 [
                  """ + self.buildClientArray() + """
                 ]
                );
            """

    def buildClientArray(self):
        clients = ""
        for client in self.clients:
            fullRequest = ""
            for request in client:
                fullRequest += str(request) + ".0, "
            clients += fullRequest + "\n"
        return clients


def show():

    print(MINIZINC_EXECUTABLE_PATH)
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()


show()
