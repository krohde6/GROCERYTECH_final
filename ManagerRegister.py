from GROCERYTECH_final import LoginRegister
from GROCERYTECH_final import CheckRegistration
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pymysql



class ManagerRegistration(QWidget):

    def __init__(self):
        super(ManagerRegistration, self).__init__()

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
        self.usernameLabel = QLabel("Username")
        self.conf_code = QLabel("Confirmation Code")
        self.password = QLabel("Password")
        self.conf_password = QLabel("Confirm Password")
        self.email = QLabel("Email")
        self.asgn_store = QLabel("Assign Store")

        self.f_nameEdit = QLineEdit()
        self.l_nameEdit = QLineEdit()
        self.usernameEdit = QLineEdit()
        self.conf_codeEdit = QLineEdit()
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.conf_passwordEdit = QLineEdit()
        self.conf_passwordEdit.setEchoMode(QLineEdit.Password)
        self.emailEdit = QLineEdit()
        self.asgn_storeCB = QComboBox()
        self.asgn_storeCB.addItem("Select Store")
        self.asgn_storeCB.addItem("33 - Publix: 7971 Anglesey Drift")
        self.asgn_storeCB.addItem("34 - Publix: 7912 Crown Terrace")
        self.asgn_storeCB.addItem("35 - Publix: 6491 Valley Corner")
        self.asgn_storeCB.addItem("36 - Publix: 5728 Southgate Royd")
        self.asgn_storeCB.addItem("37 - Publix: 2445 Garnlwyd Close")
        self.asgn_storeCB.addItem("38 - Publix: 1758 Hyde Grove")
        self.asgn_storeCB.addItem("39 - Publix: 8754 Brewery Oval")
        self.asgn_storeCB.addItem("40 - Kroger: 6745 Archer Laurels")
        self.asgn_storeCB.addItem("41 - Kroger: 6158 West View Village")
        self.asgn_storeCB.addItem("42 - Kroger: 3758 Barley Brae")
        self.asgn_storeCB.addItem("43 - Kroger: 6161 Belvedere Cottages")
        self.asgn_storeCB.addItem("44 - Kroger: 1105 Lark Leas")
        self.asgn_storeCB.addItem("45 - Kroger: 5165 Belton Hey")
        self.asgn_storeCB.addItem("46 - Whole Foods: 1554 Adam Corner")
        self.asgn_storeCB.addItem("47 - Whole Foods: 9097 Fisher Brook")
        self.asgn_storeCB.addItem("48 - Sprouts: 384 Andover Hollies")
        self.asgn_storeCB.addItem("49 - Sprouts: 378 Grant Brow")
        self.asgn_storeCB.addItem("50 - Piggly Wiggly: 4716 Warrington Newydd")
        self.asgn_storeCB.addItem("51 - Walmart: 2618 Silverdale Wharf")
        self.asgn_storeCB.addItem("52 - Walmart: 3424 Backsands Lane")
        self.asgn_storeCB.addItem("53 - Target: 8505 Netherfield Dene")
        self.asgn_storeCB.addItem("54 - Target: 7158 Windings Road")
        self.asgn_storeCB.addItem("55 - Aldi: 1338 Byker Street")
        self.asgn_storeCB.addItem("56 - Aldi: 8134 Anglesey Ride")
        self.asgn_storeCB.addItem("57 - Aldi: 4769 Moorlands Leaze")
        self.asgn_storeCB.addItem("58 - Winndixie: 782 Gipton Gate East")
        self.asgn_storeCB.addItem("59 - Sams: 6953 Marina Paddocks")
        self.asgn_storeCB.addItem("60 - Sams: 9923 Brackley Drove")
        self.asgn_storeCB.addItem("61 - Sams: 4933 Godbold Road")
        self.asgn_storeCB.addItem("62 - Sams: 1203 Frogmire Close")
        self.asgn_storeCB.addItem("63 - Costco: 742 Vaughan Pines")
        self.asgn_storeCB.addItem("64 - Costco: 8261 Parkside East")
        self.asgn_storeCB.addItem("65 - Costco: 8328 Montpelier Newydd")
        self.asgn_storeCB.addItem("66 - Trader Joes: 8897 Bell Weir Close")
        self.asgn_storeCB.addItem("67 - Trader Joes: 4490 Fourth Field")
        self.asgn_storeCB.setMaximumWidth(150)
        self.asgn_storeCB.setGeometry(QRect(40, 40, 491, 31))

        self.back = QPushButton("Back")
        self.register = QPushButton("Register")

        self.back.clicked.connect(self.backClicked)
        self.register.clicked.connect(self.registerClicked)

        root.addWidget(self.f_name, 1, 1)
        root.addWidget(self.f_nameEdit, 1, 2)
        root.addWidget(self.l_name, 1, 3)
        root.addWidget(self.l_nameEdit, 1, 4)
        root.addWidget(self.usernameLabel, 2, 1)
        root.addWidget(self.usernameEdit, 2, 2)
        root.addWidget(self.conf_code, 2, 3)
        root.addWidget(self.conf_codeEdit, 2, 4)
        root.addWidget(self.password, 3, 1)
        root.addWidget(self.passwordEdit, 3, 2)
        root.addWidget(self.conf_password, 3, 3)
        root.addWidget(self.conf_passwordEdit, 3, 4)
        root.addWidget(self.email, 4, 1)
        root.addWidget(self.emailEdit, 4, 2)
        root.addWidget(self.asgn_store, 4, 3)
        root.addWidget(self.asgn_storeCB, 4, 4)
        root.addWidget(self.back, 6, 1)
        root.addWidget(self.register, 6, 2)

        self.setLayout(root)
        self.setWindowTitle("Register Manager")
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
        managerValid = CheckRegistration.validManager(conf_code)

        if not userValid:
            self.userError = CheckRegistration.UserErrorWindow()
            self.userError.show()
            self.close()

        elif not managerValid:
            self.managerError = CheckRegistration.ManagerErrorWindow()
            self.managerError.show()
            self.close()

        else:
            cursor = self.connection.cursor()

            user_type = "manager"
            first_name = self.f_nameEdit.text()
            last_name = self.l_nameEdit.text()
            store_address = self.getStoreAddress()

            insertUser = ('INSERT INTO USERR VALUES ("{}", "{}", "{}", "{}", "{}", "{}");'.format(username, password, user_type, email, first_name, last_name))
            cursor.execute(insertUser)
            self.connection.commit()

            updateManages = ('UPDATE MANAGES SET username="{}" WHERE store_address={}'.format(username, store_address))
            cursor.execute(updateManages)
            self.connection.commit()

        self.connection.close()

    def getStoreAddress(self):
        store_address = self.asgn_storeCB.currentText()
        return int(store_address[:store_address.index(" ")])
