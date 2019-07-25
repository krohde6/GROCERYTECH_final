import pymysql

from PyQt5.QtWidgets import *
from GROCERYTECH_final import PaymentMethods

class NewPaymentMethod(QWidget):

    def __init__(self, username):
        super(NewPaymentMethod, self).__init__()

        self.username = username

        self.connection = pymysql.connect(host="localhost",
                                         user="root",
                                         password=None,
                                         db="grocerytech",
                                         charset="utf8mb4")

        self.initUI()

    def initUI(self):

        root = QGridLayout()

        self.pay_name = QLabel("Payment Name")
        self.pay_nameEdit = QLineEdit()
        self.act_num = QLabel("Account Number")
        self.act_numEdit = QLineEdit()
        self.rout_num = QLabel("Routing Number")
        self.rout_numEdit = QLineEdit()
        self.default = QLabel("Default Payment")

        self.defaultCB = QComboBox()
        self.defaultCB.addItem("NO")
        self.defaultCB.addItem("YES")

        self.back = QPushButton("Back")
        self.add = QPushButton("Add")

        self.back.clicked.connect(self.backClicked)
        self.add.clicked.connect(self.addClicked)

        root.addWidget(self.pay_name, 1, 1)
        root.addWidget(self.pay_nameEdit, 1, 2)
        root.addWidget(self.act_num, 2, 1)
        root.addWidget(self.act_numEdit, 2, 2)
        root.addWidget(self.rout_num, 3, 1)
        root.addWidget(self.rout_numEdit, 3, 2)
        root.addWidget(self.default, 4, 1)
        root.addWidget(self.defaultCB, 4, 2)
        root.addWidget(self.back, 5, 1)
        root.addWidget(self.add, 5, 2)

        self.setLayout(root)
        self.setWindowTitle("New Payment")
        self.setGeometry(350, 200, 300, 250)
        self.show()

    def backClicked(self):
        self.payMeth = PaymentMethods.PaymentMethods(self.username)
        self.payMeth.show()
        self.close()

        self.connection.close()

    def addClicked(self):
        payment_name = self.pay_nameEdit.text()
        account_number = self.act_numEdit.text()
        routing_number = self.rout_numEdit.text()

        validRout = self.validRoutNum(routing_number)
        validAct = self.validCardNum(account_number)

        if validRout and validAct:
            self.addPayment(payment_name, account_number, routing_number)

            self.connection.close()
            self.showPaymentMethods()

        else:
            self.payError = NewPaymentErrorWindow(self.username)
            self.payError.show()
            self.close()

            self.connection.close()

    def addPayment(self, payment_name, account_number, routing_number):
        cursor = self.connection.cursor()

        add = ('INSERT INTO PAYMENTS VALUES ("{}", "{}", {}, {});'.format(self.username, payment_name, account_number, routing_number))
        cursor.execute(add)
        self.connection.commit()

        if (self.defaultCB.currentText() == "YES"):
            payment_name = self.pay_nameEdit.text()

            self.setDefaultPayment(payment_name)

    def setDefaultPayment(self, payment_name):
        cursor = self.connection.cursor()

        update = ('UPDATE BUYER SET default_payment="{}" WHERE username="{}";'.format(payment_name, self.username))
        cursor.execute(update)
        self.connection.commit()

    def validRoutNum(self, rout_num=None):
        if not self.validCardNum(rout_num):
            return False

        cursor = self.connection.cursor()

        select = ('SELECT routing_number FROM PAYMENTS WHERE routing_number={}'.format(rout_num))
        cursor.execute(select)
        rout = cursor.fetchone()

        if rout == None:
            return True

        return False

    def validCardNum(self, card):
        if (card == None):
            return False

        if len(card) != 9:
            return False

        return True

    def showPaymentMethods(self):
        self.paymentMethods = PaymentMethods.PaymentMethods(self.username)
        self.paymentMethods.show()
        self.close()

class NewPaymentErrorWindow(QMessageBox):

    def __init__(self, username):
        super(NewPaymentErrorWindow, self).__init__()

        self.username = username

        self.initUI()

    def initUI(self):
        self.setIcon(QMessageBox.Information)
        self.setText("There was an error")
        self.setInformativeText('Please click "Show Details..." below')
        self.setDetailedText('Routing Number and Account Number should be exactly 9 digits.')
        self.setStandardButtons(QMessageBox.Ok)
        self.buttonClicked.connect(self.btnClicked)

        self.show()

    def btnClicked(self):
        self.newPayment = NewPaymentMethod(self.username)
        self.newPayment.show()
        self.close()

