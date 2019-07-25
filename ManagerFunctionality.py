import pymysql

from GROCERYTECH_final import LoginRegister
from GROCERYTECH_final import ManagerAccountInformation
from GROCERYTECH_final import OutstandingOrders
from GROCERYTECH_final import Inventory

from PyQt5.QtWidgets import *

class ManagerFunctWindow(QWidget):

    def __init__(self, username):
        super(ManagerFunctWindow, self).__init__()

        self.username = username

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password=None,
                                          db="grocerytech",
                                          charset="utf8mb4")

        self.initUI()

    def initUI(self):

        root = QGridLayout()

        self.revReport = QPushButton("View Revenue Reports")
        self.actInfo = QPushButton("Account Information")
        self.viewOrders = QPushButton("View Orders")
        self.viewInventory = QPushButton("View Inventory")
        self.back = QPushButton("Back")

        self.revReport.clicked.connect(self.revReportClicked)
        self.actInfo.clicked.connect(self.actInfoClicked)
        self.viewOrders.clicked.connect(self.viewOrdersClicked)
        self.viewInventory.clicked.connect(self.viewInventoryClicked)
        self.back.clicked.connect(self.backClicked)

        root.addWidget(self.revReport, 1, 1)
        root.addWidget(self.actInfo, 1, 2)
        root.addWidget(self.viewOrders, 2, 1)
        root.addWidget(self.viewInventory, 2, 2)
        root.addWidget(self.back, 3, 2)

        self.setLayout(root)
        self.setWindowTitle("Manager Functionality")
        self.setGeometry(450, 150, 500, 200)


    def revReportClicked(self):
        self.revenueWindow = ManagerAccountInformation.RevenueReport(self.username)
        self.revenueWindow.show()
        self.close()

        self.connection.close()

    def actInfoClicked(self):
        self.actInfoWindow = ManagerAccountInformation.ManagerAccountInformation(self.username)
        self.actInfoWindow.show()
        self.close()

        self.connection.close()

    def viewOrdersClicked(self):
        self.outOrders = OutstandingOrders.OutstandingOrders(self.username, self.getStoreID())
        self.outOrders.show()
        self.close()

        self.connection.close()

    def viewInventoryClicked(self):
        self.viewInv = Inventory.Inventory(self.username, self.getStoreID())
        self.viewInv.show()
        self.close()

        self.connection.close()

    def backClicked(self):
        self.confBack = ConfirmBack(self.username)
        self.confBack.show()
        self.close()

    def getStoreID(self):
        cursor1 = self.connection.cursor()
        cursor2 = self.connection.cursor()

        select1 = ('SELECT store_address FROM USERR, MANAGES WHERE USERR.username=MANAGES.username and USERR.username="{}";'.format(self.username))
        cursor1.execute(select1)
        address_id = cursor1.fetchone()[0]

        select2 = ('SELECT store_id FROM GROCERYSTORE WHERE address_id={};'.format(address_id))
        cursor2.execute(select2)
        return cursor2.fetchone()[0]

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
        self.buyerFunct = ManagerFunctWindow(self.username)
        self.buyerFunct.show()
        self.close()

    def confClicked(self):
        self.loginWin = LoginRegister.LoginWindow()
        self.loginWin.show()
        self.close()
