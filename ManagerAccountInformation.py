

import pymysql

from GROCERYTECH_final import ManagerFunctionality
from GROCERYTECH_final import LoginRegister
from GROCERYTECH_final import UpdateManagerInformation

from PyQt5.QtWidgets import *

class ManagerAccountInformation(QWidget):

    def __init__(self, username):
        super(ManagerAccountInformation, self).__init__()

        self.username = username

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password=None,
                                          db="grocerytech",
                                          charset="utf8mb4")

        self.initUI()

    def initUI(self):

        root = QGridLayout()

        self.f_name = QLabel("First Name")
        self.l_name = QLabel("Last Name")
        self.usernameLabel = QLabel("Username")
        self.phone = QLabel("Phone")
        self.strMng = QLabel("Store Managed")
        self.strAddress = QLabel("Store Address")
        self.email = QLabel("Email")

        self.f_nameEdit = QLineEdit()
        self.l_nameEdit = QLineEdit()
        self.usernameEdit = QLineEdit()
        self.phoneEdit = QLineEdit()
        self.strMngEdit = QLineEdit()
        self.strAddressEdit = QLineEdit()
        self.emailEdit = QLineEdit()

        self.f_nameEdit.setReadOnly(True)
        self.l_nameEdit.setReadOnly(True)
        self.usernameEdit.setReadOnly(True)
        self.phoneEdit.setReadOnly(True)
        self.strMngEdit.setReadOnly(True)
        self.strAddressEdit.setReadOnly(True)
        self.emailEdit.setReadOnly(True)

        self.f_nameEdit.setText(self.getFirstName())
        self.l_nameEdit.setText(self.getLastName())
        self.usernameEdit.setText(self.username)
        self.phoneEdit.setText(self.getPhone())
        self.strMngEdit.setText(self.getStrMng())
        self.strAddressEdit.setText(self.getStrAddress())

        self.back = QPushButton("Back")
        self.delAct = QPushButton("Delete Account")
        self.update = QPushButton("Update")

        self.back.clicked.connect(self.backClicked)
        self.delAct.clicked.connect(self.delActClicked)
        self.update.clicked.connect(self.updateClicked)

        root.addWidget(self.f_name, 1, 1)
        root.addWidget(self.f_nameEdit, 1, 2)
        root.addWidget(self.l_name, 1, 3)
        root.addWidget(self.l_nameEdit, 1, 4)
        root.addWidget(self.usernameLabel, 2, 1)
        root.addWidget(self.usernameEdit, 2, 2)
        root.addWidget(self.phone, 2, 3)
        root.addWidget(self.phoneEdit, 2, 4)
        root.addWidget(self.strMng, 3, 1)
        root.addWidget(self.strMngEdit, 3, 2)
        root.addWidget(self.strAddress, 3, 3)
        root.addWidget(self.strAddressEdit, 3, 4)
        root.addWidget(self.back, 4, 1)
        root.addWidget(self.delAct, 4, 3)
        root.addWidget(self.update, 4, 4)

        self.setLayout(root)
        self.setWindowTitle("Manager Account Information")
        self.setGeometry(400, 120, 600, 200)

        self.show()

    def backClicked(self):
        self.managerFunct = ManagerFunctionality.ManagerFunctWindow(self.username)
        self.managerFunct.show()
        self.close()

        self.connection.close()

    def delActClicked(self):
        self.confDelete = ConfirmDeleteAccount(self.username)
        self.confDelete.show()
        self.close()

        self.connection.close()

    def updateClicked(self):
        self.updateInfo = UpdateManagerInformation.UpdateManagerInformation(self.username)
        self.updateInfo.show()
        self.close()

        self.connection.close()

    def getFirstName(self):
        cursor = self.connection.cursor()

        select = ('SELECT first_name FROM USERR WHERE username="{}";'.format(self.username))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getLastName(self):
        cursor = self.connection.cursor()

        select = ('SELECT last_name FROM USERR WHERE username="{}";'.format(self.username))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getPhone(self):
        store_id = self.getStoreID()
        cursor = self.connection.cursor()

        select = ('SELECT phone FROM GROCERYSTORE WHERE store_id={};'.format(store_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getStrMng(self):
        store_id = self.getStoreID()
        cursor = self.connection.cursor()

        select = ('SELECT store_name FROM GROCERYSTORE WHERE store_id={};'.format(store_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getStrAddress(self):
        address_id = self.getStrAddressID()
        cursor1 = self.connection.cursor()
        cursor2 = self.connection.cursor()

        select_house_num = ('SELECT house_number FROM ADDRESS WHERE id={};'.format(address_id))
        cursor1.execute(select_house_num)
        house_number = cursor1.fetchone()[0]

        select_street = ('SELECT street FROM ADDRESS WHERE id={};'.format(address_id))
        cursor2.execute(select_street)
        street = cursor2.fetchone()[0]

        return (str(house_number) + " " + street)


    def getStrAddressID(self):
        cursor = self.connection.cursor()

        select = ('SELECT store_address FROM MANAGES WHERE username="{}";'.format(self.username))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getStoreID(self):
        address_id = self.getStrAddressID()
        cursor = self.connection.cursor()

        select = ('SELECT store_id FROM GROCERYSTORE WHERE address_id={};'.format(address_id))
        cursor.execute(select)
        return cursor.fetchone()[0]


class RevenueReport(QWidget):

    def __init__(self, username):
        super(RevenueReport, self).__init__()

        self.username = username

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password=None,
                                          db="grocerytech",
                                          charset="utf8mb4")

        self.initUI()

    def initUI(self):

        root = QGridLayout()

        self.store_name = QLabel("Store Name")
        self.num_of_items = QLabel("Number of Items Sold")
        self.total_profit = QLabel("Total Profit")

        self.store_nameEdit = QLineEdit()
        self.num_of_itemsEdit = QLineEdit()
        self.total_profitEdit = QLineEdit()

        self.store_nameEdit.setReadOnly(True)
        self.num_of_itemsEdit.setReadOnly(True)
        self.total_profitEdit.setReadOnly(True)

        self.store_nameEdit.setText(self.getStoreName())
        self.num_of_itemsEdit.setText(self.getNumItems())
        self.total_profitEdit.setText(self.getTotalProfit())

        self.back = QPushButton("Back")

        self.back.clicked.connect(self.backClicked)

        root.addWidget(self.store_name, 1, 1)
        root.addWidget(self.store_nameEdit, 1, 2)
        root.addWidget(self.num_of_items, 2, 1)
        root.addWidget(self.num_of_itemsEdit, 2, 2)
        root.addWidget(self.total_profit, 3, 1)
        root.addWidget(self.total_profitEdit, 3, 2)
        root.addWidget(self.back, 4, 1)

        self.setLayout(root)
        self.setWindowTitle("Revenue Report")
        self.setGeometry(500, 200, 400, 300)

        self.show()

    def backClicked(self):
        self.manageInfo = ManagerFunctionality.ManagerFunctWindow(self.username)
        self.manageInfo.show()
        self.close()

        self.connection.close()

    def getStrAddressID(self):
        cursor = self.connection.cursor()

        select = ('SELECT store_address FROM MANAGES WHERE username="{}";'.format(self.username))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getStoreID(self):
        address_id = self.getStrAddressID()
        cursor = self.connection.cursor()

        select = ('SELECT store_id FROM GROCERYSTORE WHERE address_id={};'.format(address_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getStoreName(self):
        store_id = self.getStoreID()
        cursor = self.connection.cursor()

        select = ('SELECT store_name FROM GROCERYSTORE WHERE store_id={};'.format(store_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getNumItems(self):
        store_id = self.getStoreID()
        cursor = self.connection.cursor()

        select = ('SELECT SUM(SELECTITEM.quantity) FROM ORDERR, ITEM, SELECTITEM, ORDERFROM WHERE ORDERR.order_id=ORDERFROM.order_id and SELECTITEM.order_id=ORDERR.order_id and ITEM.item_id=SELECTITEM.item_id and ORDERFROM.store_address_id={};'.format(store_id))
        cursor.execute(select)

        num_items = cursor.fetchone()[0]

        if num_items is None:
            return "NO SALES"

        return str(num_items)

    def getTotalProfit(self):
        store_id = self.getStoreID()
        cursor = self.connection.cursor()

        select = ('SELECT SUM((SELECTITEM.quantity * (ITEM.listed_price - ITEM.wholesale_price))) from ORDERR, ITEM, SELECTITEM, ORDERFROM where ORDERR.order_id=ORDERFROM.order_id and SELECTITEM.order_id=ORDERR.order_id and ITEM.item_id=SELECTITEM.item_id and ORDERFROM.store_address_id={};'.format(store_id))
        cursor.execute(select)

        total_profit = cursor.fetchone()[0]

        if total_profit is None:
            return "NO SALES"

        return str(total_profit)


class ConfirmDeleteAccount(QWidget):

    def __init__(self, username):
        super(ConfirmDeleteAccount, self).__init__()

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

        self.message = QLabel("ARE YOU SURE YOU WANT TO DELETE YOUR ACCOUNT?")
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
        self.setGeometry(500, 250, 150, 150)
        self.setWindowTitle("Confirm Account Deletion")

        self.show()

    def cancelClicked(self):
        self.deliverInfo = ManagerAccountInformation(self.username)
        self.deliverInfo.show()
        self.close()

        self.connection.close()

    def confClicked(self):
        cursor = self.connection.cursor()

        delete = ('DELETE FROM USERR WHERE username="{}";'.format(self.username))
        cursor.execute(delete)
        self.connection.commit()

        self.loginRegister = LoginRegister.LoginWindow()
        self.loginRegister.show()
        self.close()

        self.connection.close()



