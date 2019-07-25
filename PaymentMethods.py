import pymysql

from GROCERYTECH_final import BuyerFunctionality
from GROCERYTECH_final import NewPaymentMethod
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class PaymentMethods(QWidget):

    def __init__(self, username):
        super(PaymentMethods, self).__init__()

        self.username = username

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password=None,
                                          db="grocerytech",
                                          charset="utf8mb4")

        self.initUI()

    def initUI(self):

        root = QVBoxLayout()
        bottom = QHBoxLayout()

        self.tableWidget = QTableWidget()

        self.numRows = self.getNumRows()

        self.tableWidget.setRowCount(self.numRows)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 120)
        self.tableWidget.setColumnWidth(4, 70)
        self.tableWidget.setMinimumHeight(200)
        self.tableWidget.setHorizontalHeaderLabels(["Select", "Payment Name", "Account Number", "Routing Number", "Default"])

        self.payments = self.getPayments()

        self.qButtonGroup = QButtonGroup()

        for i in range(self.numRows):
            radioBtn = QRadioButton()
            self.qButtonGroup.addButton(radioBtn, i)
            self.tableWidget.setCellWidget(i, 0, radioBtn)
            for j in range(4):

                if j == 0:
                    payment_name = QTableWidgetItem(self.payments[i][0])
                    payment_name.setTextAlignment(Qt.AlignCenter)
                    payment_name.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                    self.tableWidget.setItem(i, 1, payment_name)

                if j == 1:
                    account_number = QTableWidgetItem(str(self.payments[i][1]))
                    account_number.setTextAlignment(Qt.AlignCenter)
                    account_number.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                    self.tableWidget.setItem(i, 2, account_number)

                if j == 2:
                    routing_number = QTableWidgetItem(str(self.payments[i][2]))
                    routing_number.setTextAlignment(Qt.AlignCenter)
                    routing_number.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                    self.tableWidget.setItem(i, 3, routing_number)

                if j == 3:
                    if self.isDefaultPayment(self.payments[i][0]):
                        default = QTableWidgetItem("YES")
                    else:
                        default = QTableWidgetItem("NO")

                    default.setTextAlignment(Qt.AlignCenter)
                    default.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                    self.tableWidget.setItem(i, 4, default)



        root.addWidget(self.tableWidget)

        self.back = QPushButton("Back")
        self.delete = QPushButton("Delete Payment")
        self.add = QPushButton("Add Payment")

        self.back.setMaximumWidth(150)
        self.delete.setMaximumWidth(150)
        self.add.setMaximumWidth(150)

        self.back.clicked.connect(self.backClicked)
        self.delete.clicked.connect(self.deleteClicked)
        self.add.clicked.connect(self.addClicked)

        bottom.addWidget(self.back)
        bottom.addWidget(self.add)
        bottom.addWidget(self.delete)

        root.addLayout(bottom)

        self.setLayout(root)
        self.setWindowTitle("Payment Methods")
        self.setGeometry(400, 200, 550, 50)
        self.show()

    def backClicked(self):
        self.buyerFunct = BuyerFunctionality.BuyerFunctWindow(self.username)
        self.buyerFunct.show()
        self.close()

        self.connection.close()

    def deleteClicked(self):
        index = self.qButtonGroup.checkedId()
        payment_name = self.payments[index][0]

        if self.isDefaultPayment(payment_name):
            self.deleteError = DeleteDefaultError(self.username)
            self.deleteError.show()
            self.close()

            self.connection.close()

        else:
            self.confDelete = ConfirmDeletePayment(payment_name, self.username)
            self.confDelete.show()
            self.close()

    def addClicked(self):
        self.newPayment = NewPaymentMethod.NewPaymentMethod(self.username)
        self.newPayment.show()
        self.close()

        self.connection.close()

    def getNumRows(self):
        cursor = self.connection.cursor()

        select = ('SELECT COUNT(*) FROM PAYMENTS WHERE username="{}";'.format(self.username))
        cursor.execute(select)
        num_payments = cursor.fetchone()
        return num_payments[0]

    def getPayments(self):
        cursor = self.connection.cursor()

        select = ('SELECT payment_name, account_number, routing_number, default_payment FROM BUYER, PAYMENTS WHERE BUYER.username=PAYMENTS.username and BUYER.username="{}";'.format(self.username))
        cursor.execute(select)

        return cursor.fetchall()

    def isDefaultPayment(self, payment_name):
        cursor = self.connection.cursor()

        select = ('SELECT default_payment FROM BUYER WHERE username="{}";'.format(self.username))
        cursor.execute(select)
        default = cursor.fetchone()[0]

        if default == payment_name:
            return True

        return False


class DeleteDefaultError(QMessageBox):

    def __init__(self, username):
        super(DeleteDefaultError, self).__init__()

        self.username = username

        self.initUI()

    def initUI(self):
        self.setIcon(QMessageBox.Information)
        self.setText("There was an error")
        self.setInformativeText('You cannot delete the default payment.')
        self.setDetailedText('Add a new payment, set that payment as default, then delete this payment.')
        self.setStandardButtons(QMessageBox.Ok)
        self.buttonClicked.connect(self.btnClicked)

        self.show()

    def btnClicked(self):
        self.payMeths = PaymentMethods(self.username)
        self.payMeths.show()
        self.close()

class ConfirmDeletePayment(QWidget):

    def __init__(self, payment_name, username):
        super(ConfirmDeletePayment, self).__init__()

        self.payment_name = payment_name
        self.username = username

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password=None,
                                          db="grocerytech",
                                          charset="utf8mb4")

        self.initUI()

    def initUI(self):

        root = QVBoxLayout()
        msg = QHBoxLayout()
        btns = QGridLayout()

        self.message = QLabel("ARE YOU SURE YOU WANT TO DELETE THIS PAYMENT?\nPAYMENT NAME: {}".format(self.payment_name))
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
        self.setGeometry(400, 250, 100, 75)
        self.setWindowTitle("Confirm Log Out")
        self.show()

    def cancelClicked(self):
        self.backToPayments()

    def confClicked(self):
        cursor = self.connection.cursor()

        delete = ('DELETE FROM PAYMENTS WHERE payment_name="{}" and username="{}";'.format(self.payment_name, self.username))
        cursor.execute(delete)
        self.connection.commit()

        self.backToPayments()

    def backToPayments(self):
        self.payMeth = PaymentMethods(self.username)
        self.payMeth.show()
        self.close()

        self.connection.close()
