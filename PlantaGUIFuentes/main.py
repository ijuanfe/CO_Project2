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
        self.CentralName = self.findChild(QLineEdit, "lineEdit_1")
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

        try:
            int(central.CaP)
            int(central.CoP)
        except:
            self.showErr('La capacidad y el costo deben ser números.')
            return

        self.centrals.append(central)
        self.centralList.addItem(
            self.CentralName.text() + " >> CaP" +
            self.CentralCaP.text() + " - CoP " +
            self.CentralCoP.text()
        )

    def addClient(self):
        days = int(self.days.text())
        cleanRequest = []
        clientRequest = self.clientRequest.text()
        request = clientRequest.split(',')
        if days <= 0:
            self.showErr('La cantidad de días debe ser mayor a 0.')
            return

        if request.__len__() == days:
            for req in request:
                try:
                    int(req)
                except:
                    self.showErr('El requerimiento debe ser numerico (Ej, 100, 200).')
                    return

                cleanRequest.append(req.strip())
            self.clients.append(cleanRequest)
            self.clientList.addItem(clientRequest)
        else:
            self.showErr('Los requerimientos ( cantidad actual=' + str(request.__len__()) + ' ) del cliente deben ser igual a la cantidad de días.')

    def runMinizinc(self):
        f = open("model/data.dzn", "w")
        f.write(self.witeInput())
        f.close()
        command = MINIZINC_EXECUTABLE_PATH + " --solver coinbc " + " model/model.mzn > out.log"
        os.system(command)
        f = open("out.log", "r")
        self.output.setPlainText(f.read())

    def witeInput(self):

        CaP = ""
        CoP = ""

        for central in self.centrals:
            CaP += central.CaP + ".0, "
            CoP += central.CoP + ".0, "

        data = "Nc = " + str(self.centrals.__len__()) + ";\n"
        data += "S = " + str(self.clients.__len__()) + ";\n"
        data += "n = " + str(self.days.text()) + ";\n"
        data += "CaP = [" + CaP + "];\n"
        data += "CoP = [" + CoP + "];\n"
        data += "d = array2d (1..S, 1..n,\n"
        data += "   [\n"
        data += self.buildClientArray() + "\n"
        data += "   ]);\n"

        return data

    def buildClientArray(self):
        clients = ""
        for client in self.clients:
            fullRequest = "     "
            for request in client:
                fullRequest += str(request) + ".0, "
            clients += fullRequest + "\n"
        return clients

    def showErr(self, msg):
        self.output.setHtml('<h3 style="color:#ff2e2e;">' + msg + '</h3>')

    def clearErr(self):
        self.output.setHtml('')


def show():

    print(MINIZINC_EXECUTABLE_PATH)
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()


show()
