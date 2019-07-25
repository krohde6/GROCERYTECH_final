import pymysql
from PyQt5.QtCore import QRect

from GROCERYTECH_final import LoginRegister
from GROCERYTECH_final import BuyerFunctionality
from PyQt5.QtWidgets import *

from GROCERYTECH_final import CheckRegistration


class BuyerRegistration(QWidget):

    def __init__(self):
        super(BuyerRegistration, self).__init__()

        self.initUI()

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password=None,
                                          db="grocerytech",
                                          charset="utf8mb4")

    def initUI(self):

        root = QGridLayout()

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
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.emailEdit = QLineEdit()
        self.house_numberEdit = QLineEdit()
        self.streetEdit = QLineEdit()
        self.cityEdit = QLineEdit()

        self.l_name = QLabel("Last Name")
        self.phone = QLabel("Phone")
        self.conf_password = QLabel("Confirm Password")
        self.state = QLabel("State")
        self.zip = QLabel("Zip Code")
        self.def_store = QLabel("Default Store")

        self.l_nameEdit = QLineEdit()
        self.phoneEdit = QLineEdit()
        self.conf_passwordEdit = QLineEdit()
        self.conf_passwordEdit.setEchoMode(QLineEdit.Password)
        self.stateEdit = QLineEdit()
        self.zipEdit = QLineEdit()

        self.asgn_storeCB = QComboBox()
        self.asgn_storeCB.addItem("Select Default Store")
        self.asgn_storeCB.addItem("1 - Publix: 7971 Anglesey Drift")
        self.asgn_storeCB.addItem("2 - Publix: 7912 Crown Terrace")
        self.asgn_storeCB.addItem("3 - Publix: 6491 Valley Corner")
        self.asgn_storeCB.addItem("4 - Publix: 5728 Southgate Royd")
        self.asgn_storeCB.addItem("5 - Publix: 2445 Garnlwyd Close")
        self.asgn_storeCB.addItem("6 - Publix: 1758 Hyde Grove")
        self.asgn_storeCB.addItem("7 - Publix: 8754 Brewery Oval")
        self.asgn_storeCB.addItem("8 - Kroger: 6745 Archer Laurels")
        self.asgn_storeCB.addItem("9 - Kroger: 6158 West View Village")
        self.asgn_storeCB.addItem("10 - Kroger: 3758 Barley Brae")
        self.asgn_storeCB.addItem("11 - Kroger: 6161 Belvedere Cottages")
        self.asgn_storeCB.addItem("12 - Kroger: 1105 Lark Leas")
        self.asgn_storeCB.addItem("13 - Kroger: 5165 Belton Hey")
        self.asgn_storeCB.addItem("14 - Whole Foods: 1554 Adam Corner")
        self.asgn_storeCB.addItem("15 - Whole Foods: 9097 Fisher Brook")
        self.asgn_storeCB.addItem("16 - Sprouts: 384 Andover Hollies")
        self.asgn_storeCB.addItem("17 - Sprouts: 378 Grant Brow")
        self.asgn_storeCB.addItem("18 - Piggly Wiggly: 4716 Warrington Newydd")
        self.asgn_storeCB.addItem("19 - Walmart: 2618 Silverdale Wharf")
        self.asgn_storeCB.addItem("20 - Walmart: 3424 Backsands Lane")
        self.asgn_storeCB.addItem("21 - Target: 8505 Netherfield Dene")
        self.asgn_storeCB.addItem("22 - Target: 7158 Windings Road")
        self.asgn_storeCB.addItem("23 - Aldi: 1338 Byker Street")
        self.asgn_storeCB.addItem("24 - Aldi: 8134 Anglesey Ride")
        self.asgn_storeCB.addItem("25 - Aldi: 4769 Moorlands Leaze")
        self.asgn_storeCB.addItem("26 - Winndixie: 782 Gipton Gate East")
        self.asgn_storeCB.addItem("27 - Sams: 6953 Marina Paddocks")
        self.asgn_storeCB.addItem("28 - Sams: 9923 Brackley Drove")
        self.asgn_storeCB.addItem("29 - Sams: 4933 Godbold Road")
        self.asgn_storeCB.addItem("30 - Sams: 1203 Frogmire Close")
        self.asgn_storeCB.addItem("31 - Costco: 742 Vaughan Pines")
        self.asgn_storeCB.addItem("32 - Costco: 8261 Parkside East")
        self.asgn_storeCB.addItem("33 - Costco: 8328 Montpelier Newydd")
        self.asgn_storeCB.addItem("34 - Trader Joes: 8897 Bell Weir Close")
        self.asgn_storeCB.addItem("35 - Trader Joes: 4490 Fourth Field")
        self.asgn_storeCB.setMaximumWidth(150)
        self.asgn_storeCB.setGeometry(QRect(40, 40, 491, 31))

        self.back = QPushButton("Back")
        self.register = QPushButton("Register")
        self.register.setToolTip("Click here to confirm registration")
        self.back.clicked.connect(self.backClicked)
        self.register.clicked.connect(self.registerClicked)

        root.addWidget(self.f_name, 1, 1)
        root.addWidget(self.f_nameEdit, 1, 2)
        root.addWidget(self.l_name, 1, 3)
        root.addWidget(self.l_nameEdit, 1, 4)
        root.addWidget(self.usernameLabel, 2, 1)
        root.addWidget(self.usernameEdit, 2, 2)
        root.addWidget(self.phone, 2, 3)
        root.addWidget(self.phoneEdit, 2, 4)
        root.addWidget(self.password, 3, 1)
        root.addWidget(self.passwordEdit, 3, 2)
        root.addWidget(self.conf_password, 3, 3)
        root.addWidget(self.conf_passwordEdit, 3, 4)
        root.addWidget(self.house_number, 4, 1)
        root.addWidget(self.house_numberEdit, 4, 2)
        root.addWidget(self.street, 4, 3)
        root.addWidget(self.streetEdit, 4, 4)
        root.addWidget(self.city, 5, 1)
        root.addWidget(self.cityEdit, 5, 2)
        root.addWidget(self.state, 5, 3)
        root.addWidget(self.stateEdit, 5, 4)
        root.addWidget(self.zip, 6, 1)
        root.addWidget(self.zipEdit, 6, 2)
        root.addWidget(self.email, 6, 3)
        root.addWidget(self.emailEdit, 6, 4)
        root.addWidget(self.def_store, 7, 3)
        root.addWidget(self.asgn_storeCB, 7, 4)
        root.addWidget(self.back, 8, 3)
        root.addWidget(self.register, 8, 4)

        self.setLayout(root)
        self.setWindowTitle("Register Buyer")
        self.setGeometry(450, 150, 500, 200)
        self.show()

    def backClicked(self):
        self.registerWindow = LoginRegister.RegisterWindow()
        self.registerWindow.show()
        self.close()

        self.connection.close()

    # ** use the same registration check for Buyer, Deliverer, & Manager sign in
    # update USER table to include new buyer
    # if registration fails (phone number not 10 digits, etc.), send to registerFailed() to open failed message
    def registerClicked(self):
        house_number = self.house_numberEdit.text()
        zip_code = self.zipEdit.text()
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        conf_password = self.conf_passwordEdit.text()
        email = self.emailEdit.text()
        phone = self.phoneEdit.text()

        addressValid = CheckRegistration.validAddress(house_number, zip_code)
        userValid = CheckRegistration.validUser(username, password, conf_password, email)
        buyerValid = CheckRegistration.validBuyer(username, phone)

        if not addressValid:
            self.addressError = CheckRegistration.AddressErrorWindow()
            self.addressError.show()
            self.close()

        elif not userValid:
            self.userError = CheckRegistration.UserErrorWindow()
            self.userError.show()
            self.close()

        elif not buyerValid:
            self.buyerError = CheckRegistration.BuyerErrorWindow()
            self.buyerError.show()
            self.close()

        # create new row for address, user, and buyer (in that order)
        else:
            address_id = self.getMaxAddress() + 1
            house_number = int(self.house_numberEdit.text())
            street = self.streetEdit.text()
            city = self.cityEdit.text()
            state = self.stateEdit.text()
            zip_code = int(self.zipEdit.text())

            user_type = "buyer"
            first_name = self.f_nameEdit.text()
            last_name = self.l_nameEdit.text()

            phone = int(self.phoneEdit.text().replace("-", ""))
            default_store_id = self.getDefaultStore()

            cursor1 = self.connection.cursor()
            cursor2 = self.connection.cursor()
            cursor3 = self.connection.cursor()

            insertAddress = ('INSERT INTO ADDRESS VALUES ({}, {}, "{}", "{}", "{}", {});'.format(address_id, house_number, street, city, state, zip_code))
            cursor1.execute(insertAddress)
            self.connection.commit()

            insertUser = ('INSERT INTO USERR VALUES ("{}", "{}", "{}", "{}", "{}", "{}");'.format(username, password, user_type, email, first_name, last_name))
            cursor2.execute(insertUser)
            self.connection.commit()

            insertBuyer = ('INSERT INTO BUYER VALUES ("{}", "{}", {}, "NONE", {});'.format(username, phone, address_id, default_store_id))
            cursor3.execute(insertBuyer)
            self.connection.commit()

            self.buyerFunct = BuyerFunctionality.BuyerFunctWindow(username)
            self.buyerFunct.show()
            self.close()

        self.connection.close()

    def getMaxAddress(self):
        cursor = self.connection.cursor()
        select_max = ('SELECT MAX(id) FROM ADDRESS;')
        cursor.execute(select_max)
        max_address = cursor.fetchone()
        return int(max_address[0])

    def getDefaultStore(self):
        store_id = self.asgn_storeCB.currentText()
        return int(store_id[:store_id.index(" ")])
