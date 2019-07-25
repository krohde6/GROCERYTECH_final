from GROCERYTECH_final import LoginRegister
from GROCERYTECH_final import CheckRegistration
from GROCERYTECH_final import DelivererFunctionality
from PyQt5.QtWidgets import *
import pymysql


class DelivererRegistration(QWidget):

    def __init__(self):
        super(DelivererRegistration, self).__init__()

        self.initUI()

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password=None,
                                          db="grocerytech",
                                          charset="utf8mb4")

    def initUI(self):

        root = QGridLayout()

        self.f_name = QLabel("First Name")
        self.l_name = QLabel("Last Name")
        self.username = QLabel("Username")
        self.conf_code = QLabel("Confirmation Code")
        self.password = QLabel("Password")
        self.conf_password = QLabel("Confirm Password")
        self.email = QLabel("Email")
        self.phone = QLabel("Phone")

        self.f_nameEdit = QLineEdit()
        self.l_nameEdit = QLineEdit()
        self.usernameEdit = QLineEdit()
        self.conf_codeEdit = QLineEdit()
        self.passwordEdit = QLineEdit()
        self.conf_passwordEdit = QLineEdit()
        self.emailEdit = QLineEdit()
        self.phoneEdit = QLineEdit()

        self.conf_passwordEdit.setEchoMode(QLineEdit.Password)
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        self.back = QPushButton("Back")
        self.register = QPushButton("Register")
        self.register.setToolTip("Click here to confirm registration")
        self.back.clicked.connect(self.backClicked)
        self.register.clicked.connect(self.registerClicked)

        root.addWidget(self.f_name, 1, 1)
        root.addWidget(self.f_nameEdit, 1, 2)
        root.addWidget(self.l_name, 1, 3)
        root.addWidget(self.l_nameEdit, 1, 4)
        root.addWidget(self.username, 2, 1)
        root.addWidget(self.usernameEdit, 2, 2)
        root.addWidget(self.conf_code, 2, 3)
        root.addWidget(self.conf_codeEdit, 2, 4)
        root.addWidget(self.password, 3, 1)
        root.addWidget(self.passwordEdit, 3, 2)
        root.addWidget(self.conf_password, 3, 3)
        root.addWidget(self.conf_passwordEdit, 3, 4)
        root.addWidget(self.email, 4, 1)
        root.addWidget(self.emailEdit, 4, 2)
        root.addWidget(self.back, 5, 3)
        root.addWidget(self.register, 5, 4)

        self.setLayout(root)
        self.setWindowTitle("Register Deliverer")
        self.setGeometry(450, 150, 550, 250)
        self.show()

    def backClicked(self):
        self.registerWindow = LoginRegister.RegisterWindow()
        self.registerWindow.show()
        self.close()

        self.connection.close()

    # calls check methods to ensure entered critera for registration is correct
    # i.e. phone number is XXX-XXX-XXXX, email contains "@", etc.
    # if all values check, create account and proceed
    def registerClicked(self):
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        conf_password = self.conf_passwordEdit.text()
        email = self.emailEdit.text()
        conf_code = int(self.conf_codeEdit.text())

        userValid = CheckRegistration.validUser(username, password, conf_password, email)
        delivererValid = CheckRegistration.validDeliverer(conf_code)

        if not userValid:
            self.userError = CheckRegistration.UserErrorWindow()
            self.userError.show()
            self.close()

        elif not delivererValid:
            self.managerError = CheckRegistration.ManagerErrorWindow()
            self.managerError.show()
            self.close()

        else:
            user_type = "deliverer"
            first_name = self.f_nameEdit.text()
            last_name = self.l_nameEdit.text()

            cursor = self.connection.cursor()

            insertUser = ('INSERT INTO USERR VALUES ("{}", "{}", "{}", "{}", "{}", "{}");'.format(username, password, user_type, email, first_name, last_name))
            cursor.execute(insertUser)
            self.connection.commit()

            self.deliverFunct = DelivererFunctionality.DelivererFunctWindow(username)
            self.deliverFunct.show()
            self.close()

        self.connection.close()
