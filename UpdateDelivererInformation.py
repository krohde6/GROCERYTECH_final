import pymysql

from GROCERYTECH_final import DelivererAccountInformation
from GROCERYTECH_final import CheckRegistration
from GROCERYTECH_final import UpdateDelivererErrors

from PyQt5.QtWidgets import *

class UpdateDelivererInformation(QWidget):

    def __init__(self, username):
        super(UpdateDelivererInformation, self).__init__()

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
        self.l_name = QLabel("Last Name")
        self.usernameLabel = QLabel("Username")
        self.password = QLabel("Password")
        self.conf_password = QLabel("Confirm Password")
        self.email = QLabel("Email")

        self.f_nameEdit = QLineEdit()
        self.l_nameEdit = QLineEdit()
        self.usernameEdit = QLineEdit()
        self.passwordEdit = QLineEdit()
        self.conf_passwordEdit = QLineEdit()
        self.emailEdit = QLineEdit()

        self.f_nameEdit.setText(self.getFirstName())
        self.l_nameEdit.setText(self.getLastName())
        self.usernameEdit.setText(self.username)
        self.passwordEdit.setText(self.getPassword())
        self.conf_passwordEdit.setText(self.getPassword())
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
        bottom.addWidget(self.email, 2, 3)
        bottom.addWidget(self.emailEdit, 2, 4)
        bottom.addWidget(self.password, 3, 1)
        bottom.addWidget(self.passwordEdit, 3, 2)
        bottom.addWidget(self.conf_password, 3, 3)
        bottom.addWidget(self.conf_passwordEdit, 3, 4)
        bottom.addWidget(self.back, 4, 3)
        bottom.addWidget(self.confirm, 4, 4)

        root.addLayout(bottom)
        self.setLayout(root)
        self.setWindowTitle("Update Information")
        self.setGeometry(400, 250, 150, 150)

        self.show()

    def backClicked(self):
        self.delivererInfo = DelivererAccountInformation.DelivererAccountInformation(self.username)
        self.delivererInfo.show()
        self.close()

        self.connection.close()

    def confirmClicked(self):
        self.updateFirstName(self.f_nameEdit.text())
        self.updateLastName(self.l_nameEdit.text())
        self.updateEmail(self.emailEdit.text())
        self.updatePassword(self.passwordEdit.text(), self.conf_passwordEdit.text())
        self.updateUsername(self.usernameEdit.text())

        if self.f_nameEdit.text() != "":
            f_nameValid = True
        else:
            f_nameValid = False

        if self.l_nameEdit.text() != "":
            l_nameValid = True
        else:
            l_nameValid = False

        validEmail = CheckRegistration.validEmail(self.emailEdit.text())
        validPassword = CheckRegistration.validPassword(self.passwordEdit.text(), self.conf_passwordEdit.text())
        validUsername = CheckRegistration.validEmail(self.emailEdit.text())

        if f_nameValid and l_nameValid and validEmail and validEmail and validUsername:
            self.updateSuccessful = UpdateSuccessful(self.getUsername())
            self.updateSuccessful.show()

        self.connection.close()
        self.close()


    def getUsername(self):
        return self.username

    def setUsername(self, n_username):
        self.username = n_username
        print("new username" + n_username)

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

    def getPassword(self):
        cursor = self.connection.cursor()

        select = ('SELECT password FROM USERR WHERE username="{}";'.format(self.getUsername()))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getEmail(self):
        cursor = self.connection.cursor()

        select = ('SELECT email FROM USERR WHERE username="{}";'.format(self.getUsername()))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getPhone(self):
        store_id = self.getStoreID()
        cursor = self.connection.cursor()

        select = ('SELECT phone FROM GROCERYSTORE WHERE store_id={};'.format(store_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def updateFirstName(self, new_f_name):

        if new_f_name != "":
            cursor = self.connection.cursor()

            update = ('UPDATE USERR SET first_name="{}" WHERE username="{}";'.format(new_f_name, self.getUsername()))
            cursor.execute(update)
            self.connection.commit()

        else:
            self.nameError = UpdateDelivererErrors.NameErrorWindow(self.getUsername())
            self.nameError.show()
            self.close()


    def updateLastName(self, new_l_name):

        if new_l_name != "":
            cursor = self.connection.cursor()

            update = ('UPDATE USERR SET last_name="{}" WHERE username="{}";'.format(new_l_name, self.getUsername()))
            cursor.execute(update)
            self.connection.commit()

        else:
            nameError = UpdateDelivererErrors.NameErrorWindow(self.getUsername())
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
            userError = UpdateDelivererErrors.UsernameErrorWindow(self.getUsername())
            userError.show()
            self.close()

    def updatePassword(self, n_password, n_conf_password):

        if CheckRegistration.validPassword(n_password, n_conf_password):
            cursor = self.connection.cursor()

            update = ('UPDATE USERR SET password="{}" WHERE username="{}";'.format(n_password, self.getUsername()))
            cursor.execute(update)
            self.connection.commit()

        else:
            passError = UpdateDelivererErrors.PasswordErrorWindow(self.getUsername())
            passError.show()
            self.close()

    def updateEmail(self, n_email):

        if CheckRegistration.validEmail(n_email):
            cursor = self.connection.cursor()

            update = ('UPDATE USERR SET email="{}" WHERE username="{}";'.format(n_email, self.getUsername()))
            cursor.execute(update)
            self.connection.commit()

        else:
            emailError = UpdateDelivererErrors.EmailErrorWindow(self.getUsername())
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
        self.acctInfo = DelivererAccountInformation.DelivererAccountInformation(self.username)
        self.acctInfo.show()
        self.close()