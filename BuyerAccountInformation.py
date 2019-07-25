import pymysql

from GROCERYTECH_final import BuyerFunctionality
from GROCERYTECH_final import LoginRegister
from GROCERYTECH_final import UpdateBuyerInformation

from PyQt5.QtWidgets import *


class BuyerAccountInformation(QWidget):

    def __init__(self, username):
        super(BuyerAccountInformation, self).__init__()

        self.username = username

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password="kwrohde",
                                          db="grocerytech",
                                          charset="utf8mb4")

        self.initUI()

    def initUI(self):

        root = QGridLayout()

        self.f_name = QLabel("First Name")
        self.usernameLabel = QLabel("Username")
        self.pref_store = QLabel("Preferred Store")
        self.store_address = QLabel("Store Address")
        self.email = QLabel("Email")
        self.pref_num = QLabel("Preferred Card Number")
        self.rout_num = QLabel("Routing Number")
        self.l_name = QLabel("Last Name")
        self.phone = QLabel("Phone")
        self.address = QLabel("Address")
        self.city = QLabel("City")
        self.state = QLabel("State")
        self.zip = QLabel("Zip Code")

        self.f_nameEdit = QLineEdit()
        self.usernameEdit = QLineEdit()
        self.pref_storeEdit = QLineEdit()
        self.store_addressEdit = QLineEdit()
        self.emailEdit = QLineEdit()
        self.pref_numEdit = QLineEdit()
        self.rout_numEdit = QLineEdit()
        self.l_nameEdit = QLineEdit()
        self.phoneEdit = QLineEdit()
        self.addressEdit = QLineEdit()
        self.cityEdit = QLineEdit()
        self.stateEdit = QLineEdit()
        self.zipEdit = QLineEdit()

        self.f_nameEdit.setReadOnly(True)
        self.usernameEdit.setReadOnly(True)
        self.pref_storeEdit.setReadOnly(True)
        self.store_addressEdit.setReadOnly(True)
        self.emailEdit.setReadOnly(True)
        self.pref_numEdit.setReadOnly(True)
        self.rout_numEdit.setReadOnly(True)
        self.l_nameEdit.setReadOnly(True)
        self.phoneEdit.setReadOnly(True)
        self.addressEdit.setReadOnly(True)
        self.cityEdit.setReadOnly(True)
        self.stateEdit.setReadOnly(True)
        self.zipEdit.setReadOnly(True)

        self.f_nameEdit.setText(self.getFirstName())
        self.usernameEdit.setText(self.username)
        self.pref_storeEdit.setText(self.getPrefStore())
        self.store_addressEdit.setText(self.getStoreAddress())
        self.emailEdit.setText(self.getEmail())
        self.pref_numEdit.setText(str(self.getPrefCard()))
        self.rout_numEdit.setText(str(self.getRoutNum()))
        self.l_nameEdit.setText(self.getLastName())
        self.phoneEdit.setText(str(self.getPhone()))
        self.addressEdit.setText(self.getAddress())
        self.cityEdit.setText(self.getCity())
        self.stateEdit.setText(self.getState())
        self.zipEdit.setText(str(self.getZip()))

        self.back = QPushButton("Back")
        self.del_acct = QPushButton("Delete Account")
        self.update = QPushButton("Update")

        self.back.clicked.connect(self.backClicked)
        self.del_acct.clicked.connect(self.deleteClicked)
        self.update.clicked.connect(self.updateClicked)

        root.addWidget(self.f_name, 1, 1)
        root.addWidget(self.f_nameEdit, 1, 2)
        root.addWidget(self.l_name, 1, 3)
        root.addWidget(self.l_nameEdit, 1, 4)
        root.addWidget(self.usernameLabel, 2, 1)
        root.addWidget(self.usernameEdit, 2, 2)
        root.addWidget(self.phone, 2, 3)
        root.addWidget(self.phoneEdit, 2, 4)
        root.addWidget(self.pref_store, 3, 1)
        root.addWidget(self.pref_storeEdit, 3, 2)
        root.addWidget(self.address, 3, 3)
        root.addWidget(self.addressEdit, 3, 4)
        root.addWidget(self.store_address, 4, 1)
        root.addWidget(self.store_addressEdit, 4, 2)
        root.addWidget(self.city, 4, 3)
        root.addWidget(self.cityEdit, 4, 4)
        root.addWidget(self.email, 5, 1)
        root.addWidget(self.emailEdit, 5, 2)
        root.addWidget(self.state, 5, 3)
        root.addWidget(self.stateEdit, 5, 4)
        root.addWidget(self.pref_num, 6, 1)
        root.addWidget(self.pref_numEdit, 6, 2)
        root.addWidget(self.zip, 6, 3)
        root.addWidget(self.zipEdit, 6, 4)
        root.addWidget(self.rout_num, 7, 1)
        root.addWidget(self.rout_numEdit, 7, 2)
        root.addWidget(self.back, 8, 2)
        root.addWidget(self.del_acct, 8, 3)
        root.addWidget(self.update, 8, 4)

        self.setLayout(root)
        self.setWindowTitle("Buyer Account Information")
        self.setGeometry(400, 120, 600, 270)
        self.show()


    def getFirstName(self):
        cursor = self.connection.cursor()

        select = ('SELECT first_name FROM USERR WHERE username="{}";'.format(self.username))
        cursor.execute(select)
        f_name = cursor.fetchone()
        return f_name[0]

    def getLastName(self):
        cursor = self.connection.cursor()

        select = ('SELECT last_name FROM USERR WHERE username="{}";'.format(self.username))
        cursor.execute(select)
        l_name = cursor.fetchone()
        return l_name[0]

    def getPhone(self):
        cursor = self.connection.cursor()

        select = ('SELECT phone FROM BUYER WHERE username="{}";'.format(self.username))
        cursor.execute(select)
        phone = cursor.fetchone()
        return phone[0]

    def getPrefStore(self):
        cursor = self.connection.cursor()

        select = ('SELECT store_name FROM GROCERYSTORE, BUYER WHERE GROCERYSTORE.store_id=BUYER.default_store_id and username="{}";'.format(self.username))
        exists = cursor.execute(select)

        if exists == 0:
            return "None"
        else:
            store_name = cursor.fetchone()
            return store_name[0]

    def getAddress(self):
        cursor1 = self.connection.cursor()
        cursor2 = self.connection.cursor()

        select1 = ('SELECT house_number FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and username="{}";'.format(self.username))
        cursor1.execute(select1)
        house_number = cursor1.fetchone()
        house_number = str(house_number[0])

        select2 = ('SELECT street FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and username="{}";'.format(self.username))
        cursor2.execute(select2)
        street = cursor2.fetchone()
        street = street[0]

        return (house_number + " " + street)

    def getStoreAddress(self):
        cursor1 = self.connection.cursor()
        cursor2 = self.connection.cursor()
        address_id = self.getStoreID()

        select1 = ('SELECT house_number FROM ADDRESS, GROCERYSTORE WHERE ADDRESS.id=GROCERYSTORE.address_id and ADDRESS.id = {};'.format(address_id))
        cursor1.execute(select1)
        house_number = cursor1.fetchone()
        house_number = str(house_number[0])

        select2 = ('SELECT street FROM ADDRESS, GROCERYSTORE WHERE ADDRESS.id=GROCERYSTORE.address_id and ADDRESS.id = {};'.format(address_id))
        cursor2.execute(select2)
        street = cursor2.fetchone()
        street = street[0]

        return (house_number + " " + street)

    def getCity(self):
        cursor = self.connection.cursor()

        select = ('SELECT city FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and BUYER.username="{}";'.format(self.username))
        cursor.execute(select)
        city = cursor.fetchone()
        return city[0]

    def getEmail(self):
        cursor = self.connection.cursor()

        select = ('SELECT email FROM USERR WHERE username="{}";'.format(self.username))
        cursor.execute(select)
        email = cursor.fetchone()
        return email[0]

    def getState(self):
        cursor = self.connection.cursor()

        select = ('SELECT state FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and BUYER.username="{}";'.format(self.username))
        cursor.execute(select)
        state = cursor.fetchone()
        return state[0]

    def getPrefCard(self):
        if self.hasNoPayMeth():
            return "NONE"

        if self.defaultIsCheck():
            return "Check"

        cursor = self.connection.cursor()

        select = ('SELECT account_number FROM BUYER, PAYMENTS WHERE BUYER.default_payment=PAYMENTS.payment_name and BUYER.username=PAYMENTS.username and BUYER.username="{}";'.format(self.username))
        cursor.execute(select)
        prefCard = cursor.fetchone()

        if type(prefCard) == tuple:
            return prefCard[0]

        else:
            return "No card on file"

    def getZip(self):
        cursor = self.connection.cursor()

        select = ('SELECT zip_code FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and BUYER.username="{}";'.format(self.username))
        cursor.execute(select)
        zipcode = cursor.fetchone()
        return zipcode[0]

    def getRoutNum(self):
        if self.hasNoPayMeth():
            return "NONE"

        if self.defaultIsCheck():
            return "Check"

        cursor = self.connection.cursor()

        select = ('SELECT routing_number FROM BUYER, PAYMENTS WHERE BUYER.default_payment=PAYMENTS.payment_name and BUYER.username=PAYMENTS.username and BUYER.username="{}";'.format(self.username))
        cursor.execute(select)
        routNum = cursor.fetchone()

        if type(routNum) == tuple:
            return routNum[0]

        else:
            return "No card on file"

    def getStoreID(self):
        cursor = self.connection.cursor()

        select = ('SELECT GROCERYSTORE.address_id FROM GROCERYSTORE, BUYER WHERE GROCERYSTORE.store_id=BUYER.default_store_id and BUYER.username="{}";'.format(self.username))
        cursor.execute(select)
        address_id = cursor.fetchone()
        return address_id[0]

    def defaultIsCheck(self):
        cursor = self.connection.cursor()

        select = ('SELECT COUNT(account_number) FROM BUYER, PAYMENTS WHERE BUYER.default_payment=PAYMENTS.payment_name and BUYER.username=PAYMENTS.username and BUYER.username="{}";'.format(self.username))
        cursor.execute(select)
        isFound = cursor.fetchone()
        isFound = isFound[0]
        if isFound == 0:
            return True
        else:
            return False

    def hasNoPayMeth(self):
        cursor = self.connection.cursor()
        select = ('SELECT default_payment FROM BUYER WHERE username="{}";'.format(self.username))
        cursor.execute(select)

        if cursor.fetchone()[0] == "NONE":
            return True

        return False

    def backClicked(self):
        self.buyerFunct = BuyerFunctionality.BuyerFunctWindow(self.username)
        self.buyerFunct.show()
        self.close()

        self.connection.close()

    def deleteClicked(self):
        self.confDelete = ConfirmDeleteAccount(self.username)
        self.confDelete.show()
        self.close()

        self.connection.close()

    def updateClicked(self):
        self.updateActInfo = UpdateBuyerInformation.UpdateBuyerInformation(self.username)
        self.updateActInfo.show()
        self.close()

        self.connection.close()



class ConfirmDeleteAccount(QWidget):

    def __init__(self, username):
        super(ConfirmDeleteAccount, self).__init__()

        self.username = username

        self.initUI()

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password=None,
                                          db="grocerytech",
                                          charset="utf8mb4")

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
        self.acctInfo = BuyerAccountInformation(self.username)
        self.acctInfo.show()
        self.close()

        self.connection.close()

    def confClicked(self):
        cursor = self.connection.cursor()

        payments = ('DELETE FROM PAYMENTS WHERE username="{}";'.format(self.username))
        user = ('DELETE FROM USERR WHERE username="{}";'.format(self.username))
        address = ('DELETE FROM ADDRESS WHERE id={};'.format(self.getAddressID()))

        cursor.execute(payments)
        cursor.execute(user)
        cursor.execute(address)
        self.connection.commit()

        self.loginRegister = LoginRegister.LoginWindow()
        self.loginRegister.show()
        self.close()

        self.connection.close()

    def getAddressID(self):
        cursor = self.connection.cursor()

        select = ('SELECT address_id FROM BUYER WHERE username="{}";'.format(self.username))
        cursor.execute(select)
        return cursor.fetchone()[0]



