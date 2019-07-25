from GROCERYTECH_final import LoginRegister
from GROCERYTECH_final import BuyerAccountInformation
from GROCERYTECH_final import PaymentMethods
from GROCERYTECH_final import StoreList
from GROCERYTECH_final import OrderHistory
from PyQt5.QtWidgets import *

class BuyerFunctWindow(QWidget):

    def __init__(self, username):
        super(BuyerFunctWindow, self).__init__()

        self.username = username

        self.initUI()

    def initUI(self):

        root = QGridLayout()

        self.newOrderBtn = QPushButton("New Order")
        self.orderHistBtn = QPushButton("Order History")
        self.actInfoBtn = QPushButton("Account Information")
        self.payMethBtn = QPushButton("Payment Methods")
        self.backBtn = QPushButton("Back")

        self.newOrderBtn.clicked.connect(self.newOrderClicked)
        self.orderHistBtn.clicked.connect(self.orderHistClicked)
        self.actInfoBtn.clicked.connect(self.actInfoClicked)
        self.payMethBtn.clicked.connect(self.payMethClicked)
        self.backBtn.clicked.connect(self.backClicked)

        root.addWidget(self.newOrderBtn, 1, 1)
        root.addWidget(self.orderHistBtn, 2, 1)
        root.addWidget(self.actInfoBtn, 1, 2)
        root.addWidget(self.payMethBtn, 2, 2)
        root.addWidget(self.backBtn, 3, 2)

        self.setLayout(root)
        self.setWindowTitle("Buyer Functionality")
        self.setGeometry(450, 150, 500, 200)
        self.show()

    def newOrderClicked(self):
        self.storeList = StoreList.StoreList(self.username)
        self.storeList.show()
        self.close()

    # direct to order history of this buyer window
    def orderHistClicked(self):
        self.orderHistory = OrderHistory.OrderHistory(self.username)
        self.orderHistory.show()
        self.close()

    def actInfoClicked(self):
        self.accountInfo = BuyerAccountInformation.BuyerAccountInformation(self.username)
        self.accountInfo.show()
        self.close()

    def payMethClicked(self):
        self.payMeth = PaymentMethods.PaymentMethods(self.username)
        self.payMeth.show()
        self.close()


    # direct back to login window
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
        self.buyerFunct = BuyerFunctWindow(self.username)
        self.buyerFunct.show()
        self.close()

    def confClicked(self):
        self.loginWin = LoginRegister.LoginWindow()
        self.loginWin.show()
        self.close()