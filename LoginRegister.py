import sys
import pymysql

from GROCERYTECH_final import BuyerRegister
from GROCERYTECH_final import DelivererRegister
from GROCERYTECH_final import ManagerRegister
from GROCERYTECH_final import BuyerFunctionality
from GROCERYTECH_final import DelivererFunctionality
from GROCERYTECH_final import ManagerFunctionality
from PyQt5.QtWidgets import *

class LoginWindow(QWidget):

    def __init__(self):
        super(LoginWindow, self).__init__()

        self.initUI()

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password=None,
                                          db="grocerytech",
                                          charset="utf8mb4")

    def initUI(self):

        root = QVBoxLayout()
        layout_form = QFormLayout()
        layout_hbox = QHBoxLayout()

        self.username = QLabel("Username")
        self.password = QLabel("Password")
        self.usernameEdit = QLineEdit()
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.login = QPushButton("Login")
        self.register = QPushButton("Register")
        self.register.setToolTip("If you do not have an account, click here.")

        self.login.clicked.connect(self.loginClicked)
        self.register.clicked.connect(self.registerClicked)

        layout_form.addRow(self.username, self.usernameEdit)
        layout_form.addRow(self.password, self.passwordEdit)
        layout_hbox.addWidget(self.login)
        layout_hbox.addWidget(self.register)

        root.addLayout(layout_form)
        root.addLayout(layout_hbox)

        self.setLayout(root)
        self.setGeometry(500, 200, 300, 150)
        self.setWindowTitle("User Login")
        self.show()

    # check if username/password matches existing account
    # display error window if user DNE
    def loginClicked(self):

        if self.validLogin(self.usernameEdit.text(), self.passwordEdit.text()):
            username = self.usernameEdit.text()
            user_type = self.getUserType(username)

            # open buyer logged in window
            if user_type == "buyer":
                self.buyerFuncWindow = BuyerFunctionality.BuyerFunctWindow(username)
                self.buyerFuncWindow.show()
                self.close()

            # open manager logged in window
            elif user_type == "manager":
                self.managerFuncWindow = ManagerFunctionality.ManagerFunctWindow(username)
                self.managerFuncWindow.show()
                self.close()

            # open deliverer logged in window
            else:
                self.deliverFuncWindow = DelivererFunctionality.DelivererFunctWindow(username)
                self.deliverFuncWindow.show()
                self.close()

        else:
            self.errorWindow = LoginErrorWindow()
            self.errorWindow.show()
            self.close()

        self.connection.close()

    # redirect to register window
    def registerClicked(self):
        self.register = RegisterWindow()
        self.register.show()
        self.close()

        self.connection.close()

    def validLogin(self, username=None, password=None):

        if (username == None or password == None):
            return False

        cursor1 = self.connection.cursor()
        cursor2 = self.connection.cursor()

        loadName = ('SELECT username FROM USERR WHERE username="{}" and password="{}";'.format(username, password))
        loadPass = ('SELECT password FROM USERR WHERE username="{}" and password="{}";'.format(username, password))

        cursor1.execute(loadName)
        nameCheck = cursor1.fetchone()

        cursor2.execute(loadPass)
        passCheck = cursor2.fetchone()

        if (nameCheck == None or passCheck == None):
            return False

        if (username == nameCheck[0] and password == passCheck[0]):
            return True

        return False

    def getUserType(self, username):

        cursor = self.connection.cursor()
        select = ('SELECT user_type FROM USERR WHERE username="{}";'.format(username))
        cursor.execute(select)

        user_type = cursor.fetchone()

        return user_type[0]

class LoginErrorWindow(QMessageBox):

    def __init__(self):
        super(LoginErrorWindow, self).__init__()

        self.initUI()

    def initUI(self):
        self.setIcon(QMessageBox.Information)
        self.setText("There was an error while trying to log you in")
        self.setInformativeText('Please click "Show Details..." below')
        self.setDetailedText('Your username + password does not match an account we have on file'
                             '\nEither try again or click "Register" at the login window '
                             'to create a new account')
        self.setStandardButtons(QMessageBox.Ok)
        self.buttonClicked.connect(self.btnClicked)

        self.show()

    def btnClicked(self):
        self.loginWindow = LoginWindow()
        self.loginWindow.show()
        self.close()

class RegisterWindow(QWidget):

    def __init__(self):
        super(RegisterWindow, self).__init__()

        self.initUI()

    def initUI(self):

        root = QVBoxLayout()

        self.buyer = QPushButton("Buyer")
        self.deliverer = QPushButton("Deliverer")
        self.manager = QPushButton("Manager")
        self.back = QPushButton("Back")

        self.buyer.setToolTip("Click here to register as a Buyer.")
        self.deliverer.setToolTip("Click here to register as a Deliverer.")
        self.manager.setToolTip("Click here to register as a Manager.")
        self.back.setToolTip("Click here to return to the login screen.")

        self.buyer.clicked.connect(self.buyerClicked)
        self.deliverer.clicked.connect(self.delivererClicked)
        self.manager.clicked.connect(self.managerClicked)
        self.back.clicked.connect(self.backClicked)

        root.addWidget(self.buyer)
        root.addWidget(self.deliverer)
        root.addWidget(self.manager)
        root.addWidget(self.back)

        self.setLayout(root)
        self.setWindowTitle("Register Navigation")
        self.setGeometry(520, 210, 250, 200)
        self.show()

    # direct to the buyer login screen
    def buyerClicked(self):
        self.buyerRegistration = BuyerRegister.BuyerRegistration()
        self.buyerRegistration.show()
        self.close()

    # direct to the deliverer login screen
    def delivererClicked(self):
        self.delivererRegistration = DelivererRegister.DelivererRegistration()
        self.delivererRegistration.show()
        self.close()

    # direct to the manager login screen
    def managerClicked(self):
        self.managerRegistration = ManagerRegister.ManagerRegistration()
        self.managerRegistration.show()
        self.close()

    # direct back to login window
    def backClicked(self):
        self.login = LoginWindow()
        self.login.show()
        self.close()

def main():
    app = QApplication(sys.argv)
    ex = LoginWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()