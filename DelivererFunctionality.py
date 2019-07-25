from GROCERYTECH_final import LoginRegister
from GROCERYTECH_final import DelivererAccountInformation
from GROCERYTECH_final import Assignments

from PyQt5.QtWidgets import *

class DelivererFunctWindow(QWidget):

    def __init__(self, username):
        super(DelivererFunctWindow, self).__init__()

        self.username = username

        self.initUI()

    def initUI(self):

        root = QGridLayout()

        self.assignments = QPushButton("Assignments")
        self.actInfo = QPushButton("Account Information")
        self.back = QPushButton("Back")

        self.assignments.clicked.connect(self.assignmentsClicked)
        self.actInfo.clicked.connect(self.actInfoClicked)
        self.back.clicked.connect(self.backClicked)

        root.addWidget(self.assignments, 1, 1)
        root.addWidget(self.actInfo, 1, 2)
        root.addWidget(self.back, 2, 1)

        self.setLayout(root)
        self.setWindowTitle("Deliverer Functionality")
        self.setGeometry(450, 150, 500, 200)


    def assignmentsClicked(self):
        self.assign = Assignments.Assignments(self.username)
        self.assign.show()
        self.close()

    def actInfoClicked(self):
        self.actInfoWindow = DelivererAccountInformation.DelivererAccountInformation(self.username)
        self.actInfoWindow.show()
        self.close()

    def backClicked(self):
        self.confBack = ConfirmBack(self.username)
        self.confBack.show()
        self.close()

class ConfirmBack(QWidget):

    def __init__(self, username):
        super(ConfirmBack, self).__init__()

        self.username = username

        self.initUI()

    def initUI(self):

        root = QVBoxLayout()
        msg = QHBoxLayout()
        btns = QGridLayout()

        self.message = QLabel("ARE YOU SURE YOU WANT TO GO BACK?\nGOING BACK WILL LOG YOU OUT & YOU WILL BE REQUIRED TO LOG IN AGAIN.")
        self.message.setStyleSheet("color: red")
        msg.addWidget(self.message)

        self.cancelBtn = QPushButton("Cancel")
        self.confBtn = QPushButton("Confirm")
        self.cancelBtn.clicked.connect(self.cancelClicked)
        self.confBtn.clicked.connect(self.confClicked)

        btns.addWidget(self.cancelBtn, 1, 3)
        btns.addWidget(self.confBtn, 1, 4)

        root.addLayout(msg)
        root.addLayout(btns)
        self.setLayout(root)
        self.setGeometry(400, 250, 150, 150)
        self.setWindowTitle("Confirm Log Out")
        self.show()

    def cancelClicked(self):
        self.buyerFunct = DelivererFunctWindow(self.username)
        self.buyerFunct.show()
        self.close()

    def confClicked(self):
        self.loginWin = LoginRegister.LoginWindow()
        self.loginWin.show()
        self.close()
