import pymysql
from PyQt5.QtWidgets import *

from GROCERYTECH_final import LoginRegister

connection = pymysql.connect(host="localhost",
                             user="root",
                             password=None,
                             db="grocerytech",
                             charset="utf8mb4")

def validAddress(house_number=None, zipcode=None):

    if ((house_number == None) or (zipcode == None)):
        return False

    if len(zipcode) != 5:
        return False
    if not zipcode.isdigit():
        return False
    if not house_number.isdigit():
        return False

    return True

def validHouseNum(house_number=None):
    if house_number == None:
        return False

    if not house_number.isdigit():
        return False

    return True

def validUser(username=None, password=None, conf_password=None, email=None):

    if ((username == None) or (password == None) or (conf_password == None) or (email == None)):
        return False

    if password != conf_password:
        return False
    if not validEmail(email):
        return False
    if not validUsername(username):
        return False
    return True

def validManager(conf_code=None):

    if (conf_code == None):
        return False

    cursor = connection.cursor()
    select = ('SELECT user_codes FROM SYSTEMINFORMATION WHERE system_id=1;')
    cursor.execute(select)
    code = cursor.fetchone()

    if code[0] == conf_code:
        return True

    return False

def validDeliverer(conf_code=None):

    if (conf_code == None):
        return False

    cursor = connection.cursor()
    select = ('SELECT user_codes FROM SYSTEMINFORMATION WHERE system_id=0;')
    cursor.execute(select)
    code = cursor.fetchone()

    if code[0] == conf_code:
        return True

    return False

def validBuyer(username=None, phone=None):

    if ((username == None) or (phone == None)):
        return False

    if not validPhone(phone):
        return False
    if not validUsername(username):
        return False

    return True

def validUsername(username=None):

    if (username == None):
        return False

    cursor = connection.cursor()

    select = ('SELECT username FROM USERR WHERE username="{}";'.format(username))
    cursor.execute(select)
    user = cursor.fetchone()

    if user == None:
        return True

    return False

def validPassword(password=None, conf_password=None):

    if ((password == None) or (conf_password == None)):
        return False

    if (password == conf_password):
        return True

    return False

def validEmail(email=None):

    if (email == None):
        return False

    if "@" not in email:
        return False

    if "." not in email:
        return False

    count1, count2 = 0, 0
    for char in email:
        if char == "@":
            count1 += 1
        if char == ".":
            count2 += 1

    if count1 > 1 or count2 > 1:
        return False

    return True

def validPhone(phone=None):

    if (phone == None):
        return False

    import re
    pattern = re.compile("^[\dA-Z]{3}-[\dA-Z]{3}-[\dA-Z]{4}$", re.IGNORECASE)
    return pattern.match(phone) is not None

class AddressErrorWindow(QMessageBox):

    def __init__(self):
        super(AddressErrorWindow, self).__init__()

        self.initUI()

    def initUI(self):
        self.setIcon(QMessageBox.Information)
        self.setText("There was an error")
        self.setInformativeText('Please click "Show Details..." below')
        self.setDetailedText('There seems to be an error with the address you entered. Please try again')
        self.setStandardButtons(QMessageBox.Ok)
        self.buttonClicked.connect(self.btnClicked)

        self.show()

    def btnClicked(self):
        self.registerWindow = LoginRegister.RegisterWindow()
        self.registerWindow.show()
        self.close()


class UserErrorWindow(QMessageBox):

    def __init__(self):
        super(UserErrorWindow, self).__init__()

        self.initUI()

    def initUI(self):
        self.setIcon(QMessageBox.Information)
        self.setText("There was an error")
        self.setInformativeText('Please click "Show Details..." below')
        self.setDetailedText('Either your password did not match the confirmation, your email was not a valid email, or the username is already taken. Please try again.')
        self.setStandardButtons(QMessageBox.Ok)
        self.buttonClicked.connect(self.btnClicked)

        self.show()

    def btnClicked(self):
        self.registerWindow = LoginRegister.RegisterWindow()
        self.registerWindow.show()
        self.close()

class BuyerErrorWindow(QMessageBox):

    def __init__(self):
        super(BuyerErrorWindow, self).__init__()

        self.initUI()

    def initUI(self):
        self.setIcon(QMessageBox.Information)
        self.setText("There was an error")
        self.setInformativeText('Please click "Show Details..." below')
        self.setDetailedText('Please enter phone number like XXX-XXX-XXXX. If you entered your phone like this format, the username you entered is already taken.')
        self.setStandardButtons(QMessageBox.Ok)
        self.buttonClicked.connect(self.btnClicked)

        self.show()

    def btnClicked(self):
        self.registerWindow = LoginRegister.RegisterWindow()
        self.registerWindow.show()
        self.close()

class ManagerErrorWindow(QMessageBox):

    def __init__(self):
        super(ManagerErrorWindow, self).__init__()

        self.initUI()

    def initUI(self):
        self.setIcon(QMessageBox.Information)
        self.setText("There was an error")
        self.setInformativeText('Please click "Show Details..." below')
        self.setDetailedText('Your confirmation code is invalid. Please try again or check with your manager to verify the confirmation code.')
        self.setStandardButtons(QMessageBox.Ok)
        self.buttonClicked.connect(self.btnClicked)

        self.show()

    def btnClicked(self):
        self.registerWindow = LoginRegister.RegisterWindow()
        self.registerWindow.show()
        self.close()
