import pymysql

from GROCERYTECH_final import BuyerAccountInformation
from GROCERYTECH_final import CheckRegistration
from GROCERYTECH_final import UpdateBuyerErrors

from PyQt5.QtWidgets import *


class UpdateBuyerInformation(QWidget):

    def __init__(self, username):
        super(UpdateBuyerInformation, self).__init__()

        self.username = username

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password=None,
                                          db="grocerytech",
                                          charset="utf8mb4")

        self.initUI()

    def initUI(self):
        root = QVBoxLayout()
        bottom = QGridLayout()

        self.instructions = QLabel("Make changes to any information you'd like to change. Click 'Submit Changes' when you're finished to confirm changes.")
        root.addWidget(self.instructions)

        self.f_name = QLabel("First Name")
        self.usernameLabel = QLabel("Username")
        self.password = QLabel("Password")
        self.house_number = QLabel("House Number")
        self.street = QLabel("Street")
        self.city = QLabel("City")
        self.email = QLabel("Email")

        self.f_nameEdit = QLineEdit()
        self.usernameEdit = QLineEdit()
        self.passwordEdit = QLineEdit()
        self.emailEdit = QLineEdit()
        self.house_numberEdit = QLineEdit()
        self.streetEdit = QLineEdit()
        self.cityEdit = QLineEdit()

        self.l_name = QLabel("Last Name")
        self.phone = QLabel("Phone")
        self.conf_password = QLabel("Confirm Password")
        self.state = QLabel("State")
        self.zip = QLabel("Zip Code")

        self.l_nameEdit = QLineEdit()
        self.phoneEdit = QLineEdit()
        self.conf_passwordEdit = QLineEdit()
        self.stateEdit = QLineEdit()
        self.zipEdit = QLineEdit()

        self.f_nameEdit.setText(self.getFirstName())
        self.l_nameEdit.setText(self.getLastName())
        self.usernameEdit.setText(self.username)
        self.phoneEdit.setText(self.getPhone())
        self.passwordEdit.setText(self.getPassword())
        self.conf_passwordEdit.setText(self.getPassword())
        self.house_numberEdit.setText(self.getHouseNum())
        self.streetEdit.setText(self.getStreet())
        self.cityEdit.setText(self.getCity())
        self.stateEdit.setText(self.getState())
        self.zipEdit.setText(self.getZip())
        self.emailEdit.setText(self.getEmail())

        self.back = QPushButton("Back")
        self.confirm = QPushButton("Confirm Changes")
        self.back.clicked.connect(self.backClicked)
        self.confirm.clicked.connect(self.confirmClicked)

        bottom.addWidget(self.f_name, 1, 1)
        bottom.addWidget(self.f_nameEdit, 1, 2)
        bottom.addWidget(self.l_name, 1, 3)
        bottom.addWidget(self.l_nameEdit, 1, 4)
        bottom.addWidget(self.usernameLabel, 2, 1)
        bottom.addWidget(self.usernameEdit, 2, 2)
        bottom.addWidget(self.phone, 2, 3)
        bottom.addWidget(self.phoneEdit, 2, 4)
        bottom.addWidget(self.password, 3, 1)
        bottom.addWidget(self.passwordEdit, 3, 2)
        bottom.addWidget(self.conf_password, 3, 3)
        bottom.addWidget(self.conf_passwordEdit, 3, 4)
        bottom.addWidget(self.house_number, 4, 1)
        bottom.addWidget(self.house_numberEdit, 4, 2)
        bottom.addWidget(self.street, 4, 3)
        bottom.addWidget(self.streetEdit, 4, 4)
        bottom.addWidget(self.city, 5, 1)
        bottom.addWidget(self.cityEdit, 5, 2)
        bottom.addWidget(self.state, 5, 3)
        bottom.addWidget(self.stateEdit, 5, 4)
        bottom.addWidget(self.zip, 6, 1)
        bottom.addWidget(self.zipEdit, 6, 2)
        bottom.addWidget(self.email, 6, 3)
        bottom.addWidget(self.emailEdit, 6, 4)
        bottom.addWidget(self.back, 8, 3)
        bottom.addWidget(self.confirm, 8, 4)

        root.addLayout(bottom)
        self.setLayout(root)
        self.setWindowTitle("Update Information")
        self.setGeometry(450, 150, 500, 200)
        self.show()

    def backClicked(self):
        self.buyerActInfo = BuyerAccountInformation.BuyerAccountInformation(self.getUsername())
        self.buyerActInfo.show()
        self.close()

        self.connection.close()

    def confirmClicked(self):
        self.updateFirstName(self.f_nameEdit.text())
        self.updateLastName(self.l_nameEdit.text())
        self.updatePassword(self.passwordEdit.text(), self.conf_passwordEdit.text())
        self.updateHouseNum(self.house_numberEdit.text())
        self.updateStreet(self.streetEdit.text())
        self.updateCity(self.cityEdit.text())
        self.updateState(self.stateEdit.text())
        self.updateZip((self.zipEdit.text()))
        self.updateEmail(self.emailEdit.text())
        self.updateUsername(self.usernameEdit.text())

        if self.f_nameEdit.text() != "":
            f_nameValid = True
        else:
            f_nameValid = False

        if self.l_nameEdit.text() != "":
            l_nameValid = True
        else:
            l_nameValid = False

        validPassword = CheckRegistration.validPassword(self.passwordEdit.text(), self.conf_passwordEdit.text())
        validAddress = CheckRegistration.validAddress(self.house_numberEdit.text(), self.zipEdit.text())
        validEmail = CheckRegistration.validEmail(self.emailEdit.text())
        validUsername = CheckRegistration.validUsername(self.usernameEdit.text())

        if f_nameValid and l_nameValid and validPassword and validAddress and validEmail and validUsername:
            self.updateSuccessful = UpdateSuccessful(self.getUsername())
            self.updateSuccessful.show()

        self.connection.close()
        self.close()

    def setUsername(self, n_username):
        self.username = n_username

    def getUsername(self):
        return self.username

    def getAddressID(self):
        cursor = self.connection.cursor()

        select_id = ('SELECT address_id FROM BUYER WHERE username="{}";'.format(self.getUsername()))
        cursor.execute(select_id)
        return cursor.fetchone()[0]

    def getFirstName(self):
        cursor = self.connection.cursor()

        select = ('SELECT first_name FROM USERR WHERE username="{}";'.format(self.getUsername()))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getLastName(self):
        cursor = self.connection.cursor()

        select = ('SELECT last_name FROM USERR WHERE username="{}";'.format(self.getUsername()))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getPhone(self):
        cursor = self.connection.cursor()

        select = ('SELECT phone FROM BUYER WHERE username="{}";'.format(self.getUsername()))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getPassword(self):
        cursor = self.connection.cursor()

        select = ('SELECT password FROM USERR WHERE username="{}";'.format(self.getUsername()))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getHouseNum(self):
        cursor = self.connection.cursor()

        select = ('SELECT house_number FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and username="{}";'.format(self.getUsername()))
        cursor.execute(select)
        return str(cursor.fetchone()[0])

    def getStreet(self):
        cursor = self.connection.cursor()

        select = ('SELECT street FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and username="{}";'.format(self.getUsername()))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getCity(self):
        cursor = self.connection.cursor()

        select = ('SELECT city FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and username="{}";'.format(self.getUsername()))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getState(self):
        cursor = self.connection.cursor()

        select = ('SELECT state FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and username="{}";'.format(self.getUsername()))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getZip(self):
        cursor = self.connection.cursor()

        select = ('SELECT zip_code FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and username="{}";'.format(self.getUsername()))
        cursor.execute(select)
        return str(cursor.fetchone()[0])

    def getEmail(self):
        cursor = self.connection.cursor()

        select = ('SELECT email FROM USERR WHERE username="{}";'.format(self.getUsername()))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def updateFirstName(self, new_f_name):
        if new_f_name != "":
            cursor = self.connection.cursor()

            update = ('UPDATE USERR SET first_name="{}" WHERE username="{}";'.format(new_f_name, self.getUsername()))
            cursor.execute(update)
            self.connection.commit()

        else:
            self.nameError = UpdateBuyerErrors.NameErrorWindow(self.getUsername())
            self.nameError.show()
            self.close()

    def updateLastName(self, new_l_name):
        if new_l_name != "":
            cursor = self.connection.cursor()

            update = ('UPDATE USERR SET last_name="{}" WHERE username="{}";'.format(new_l_name, self.getUsername()))
            cursor.execute(update)
            self.connection.commit()

        else:
            nameError = UpdateBuyerErrors.NameErrorWindow(self.getUsername())
            nameError.show()
            self.close()

    def updateUsername(self, n_username):
        if CheckRegistration.validUsername(n_username):
            cursor = self.connection.cursor()

            update = ('UPDATE USERR SET username="{}" WHERE username="{}";'.format(n_username, self.getUsername()))
            cursor.execute(update)
            self.connection.commit()

            self.setUsername(n_username)

        else:
            userError = UpdateBuyerErrors.UsernameErrorWindow(self.getUsername())
            userError.show()
            self.close()

    def updatePassword(self, n_password, n_conf_password):
        if CheckRegistration.validPassword(n_password, n_conf_password):
            cursor = self.connection.cursor()

            update = ('UPDATE USERR SET password="{}" WHERE username="{}";'.format(n_password, self.getUsername()))
            cursor.execute(update)
            self.connection.commit()

        else:
            passError = UpdateBuyerErrors.PasswordErrorWindow(self.getUsername())
            passError.show()
            self.close()

    def updateHouseNum(self, n_house_number):
        if CheckRegistration.validHouseNum(n_house_number):
            address_id = self.getAddressID()

            cursor = self.connection.cursor()
            update =('UPDATE ADDRESS SET house_number={} WHERE id={};'.format(int(n_house_number), address_id))
            cursor.execute(update)
            self.connection.commit()

        else:
            houseError = UpdateBuyerErrors.HouseNumErrorWindow(self.getUsername())
            houseError.show()
            self.close()

    def updateStreet(self, n_street):
        if len(n_street) <= 64:
            address_id = self.getAddressID()

            cursor = self.connection.cursor()
            update = ('UPDATE ADDRESS SET street="{}" WHERE id={};'.format(n_street, address_id))
            cursor.execute(update)
            self.connection.commit()

    def updateCity(self, n_city):
        address_id = self.getAddressID()

        cursor = self.connection.cursor()
        update = ('UPDATE ADDRESS SET city="{}" WHERE id={};'.format(n_city, address_id))
        cursor.execute(update)
        self.connection.commit()

    def updateState(self, n_state):
        address_id = self.getAddressID()

        cursor = self.connection.cursor()
        update = ('UPDATE ADDRESS SET state="{}" WHERE id={};'.format(n_state, address_id))
        cursor.execute(update)
        self.connection.commit()

    def updateZip(self, n_zip):
        if ((len(n_zip) == 5) and n_zip.isdigit()):
            address_id = self.getAddressID()

            cursor = self.connection.cursor()
            update = ('UPDATE ADDRESS SET zip_code={} WHERE id={};'.format(int(n_zip), address_id))
            cursor.execute(update)
            self.connection.commit()

        else:
            zipError = UpdateBuyerErrors.ZipCodeErrorWindow(self.getUsername())
            zipError.show()
            self.close()

    def updateEmail(self, n_email):
        if CheckRegistration.validEmail(n_email):
            cursor = self.connection.cursor()

            update = ('UPDATE USERR SET email="{}" WHERE username="{}";'.format(n_email, self.getUsername()))
            cursor.execute(update)
            self.connection.commit()

        else:
            emailError = UpdateBuyerErrors.EmailErrorWindow(self.getUsername())
            emailError.show()
            self.close()

class UpdateSuccessful(QWidget):

    def __init__(self, username):
        super(UpdateSuccessful, self).__init__()

        self.username = username

        self.initUI()

    def initUI(self):

        root = QVBoxLayout()
        msg = QHBoxLayout()
        btns = QGridLayout()

        self.message = QLabel("YOUR ACCOUNT INFORMATION HAS BEEN UPDATED")
        msg.addWidget(self.message)

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.okClicked)

        btns.addWidget(self.okBtn, 1, 4)

        root.addLayout(msg)
        root.addLayout(btns)
        self.setLayout(root)
        self.setGeometry(500, 250, 150, 150)
        self.setWindowTitle("Account Updated")
        self.show()

    def okClicked(self):
        self.acctInfo = BuyerAccountInformation.BuyerAccountInformation(self.username)
        self.acctInfo.show()
        self.close()









