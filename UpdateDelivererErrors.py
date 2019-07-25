from GROCERYTECH_final import UpdateDelivererInformation

from PyQt5.QtWidgets import *


class NameErrorWindow(QMessageBox):

    def __init__(self, username):
        super(NameErrorWindow, self).__init__()

        self.username = username

        self.initUI()

    def initUI(self):
        self.setIcon(QMessageBox.Information)
        self.setText("There was an error")
        self.setInformativeText('Please click "Show Details..." below')
        self.setDetailedText('Name cannot be empty.')
        self.setStandardButtons(QMessageBox.Ok)
        self.buttonClicked.connect(self.btnClicked)

        self.show()

    def btnClicked(self):
        self.updateActInfo = UpdateDelivererInformation.UpdateDelivererInformation(self.username)
        self.updateActInfo.show()
        self.close()


class UsernameErrorWindow(QMessageBox):

    def __init__(self, username):
        super(UsernameErrorWindow, self).__init__()

        self.username = username

        self.initUI()

    def initUI(self):
        self.setIcon(QMessageBox.Information)
        self.setText("There was an error")
        self.setInformativeText('Please click "Show Details..." below')
        self.setDetailedText('It appears this username is already taken. Please try again')
        self.setStandardButtons(QMessageBox.Ok)
        self.buttonClicked.connect(self.btnClicked)

        self.show()

    def btnClicked(self):
        self.updateActInfo = UpdateDelivererInformation.UpdateDelivererInformation(self.username)
        self.updateActInfo.show()
        self.close()


class PasswordErrorWindow(QMessageBox):

    def __init__(self, username):
        super(PasswordErrorWindow, self).__init__()

        self.username = username

        self.initUI()

    def initUI(self):
        self.setIcon(QMessageBox.Information)
        self.setText("There was an error")
        self.setInformativeText('Please click "Show Details..." below')
        self.setDetailedText('The password you entered did not match the confirmation password. Please try again.')
        self.setStandardButtons(QMessageBox.Ok)
        self.buttonClicked.connect(self.btnClicked)

        self.show()

    def btnClicked(self):
        self.updateActInfo = UpdateDelivererInformation.UpdateDelivererInformation(self.username)
        self.updateActInfo.show()
        self.close()


class EmailErrorWindow(QMessageBox):

    def __init__(self, username):
        super(EmailErrorWindow, self).__init__()

        self.username = username

        self.initUI()

    def initUI(self):
        self.setIcon(QMessageBox.Information)
        self.setText("There was an error")
        self.setInformativeText('Please click "Show Details..." below')
        self.setDetailedText('The email should contain exactly one "." and exactly one "@".')
        self.setStandardButtons(QMessageBox.Ok)
        self.buttonClicked.connect(self.btnClicked)

        self.show()

    def btnClicked(self):
        self.updateActInfo = UpdateDelivererInformation.UpdateDelivererInformation(self.username)
        self.updateActInfo.show()
        self.close()


