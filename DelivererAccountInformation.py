import pymysql

from GROCERYTECH_final import DelivererFunctionality
from GROCERYTECH_final import LoginRegister
from GROCERYTECH_final import UpdateDelivererInformation

from PyQt5.QtWidgets import *

class DelivererAccountInformation(QWidget):

    def __init__(self, username):
        super(DelivererAccountInformation, self).__init__()

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
        self.email = QLabel("Email")
        self.email.setMaximumWidth(50)

        self.f_nameEdit = QLineEdit()
        self.l_nameEdit = QLineEdit()
        self.usernameEdit = QLineEdit()
        self.emailEdit = QLineEdit()
        self.emailEdit.setMaximumWidth(150)

        self.l_nameEdit.setMaximumWidth(100)

        self.f_nameEdit.setReadOnly(True)
        self.l_nameEdit.setReadOnly(True)
        self.usernameEdit.setReadOnly(True)
        self.emailEdit.setReadOnly(True)

        self.f_nameEdit.setText(self.getFirstName())
        self.l_nameEdit.setText(self.getLastName())
        self.usernameEdit.setText(self.username)
        self.emailEdit.setText(self.getEmail())

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
        root.addWidget(self.email, 2, 3)
        root.addWidget(self.emailEdit, 2, 4)
        root.addWidget(self.back, 3, 1)
        root.addWidget(self.delAct, 3, 3)
        root.addWidget(self.update, 3, 4)

        self.setLayout(root)
        self.setWindowTitle("Deliverer Account Information")
        self.setGeometry(400, 120, 600, 200)

        self.show()

    def backClicked(self):
        self.delFunct = DelivererFunctionality.DelivererFunctWindow(self.username)
        self.delFunct.show()
        self.close()

        self.connection.close()

    def delActClicked(self):
        self.confDelete = ConfirmDeleteAccount(self.username)
        self.confDelete.show()
        self.close()

        self.connection.close()

    def updateClicked(self):
        self.updateDeliver = UpdateDelivererInformation.UpdateDelivererInformation(self.username)
        self.updateDeliver.show()
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

    def getEmail(self):
        cursor = self.connection.cursor()

        select = ('SELECT email FROM USERR WHERE username="{}";'.format(self.username))
        cursor.execute(select)
        return cursor.fetchone()[0]



class ConfirmDeleteAccount(QWidget):

    def __init__(self, username):
        super(ConfirmDeleteAccount, self).__init__()

        self.username = username

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
        self.deliverInfo = DelivererAccountInformation(self.username)
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


