import pymysql

from GROCERYTECH_final import ManagerFunctionality

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Inventory(QWidget):

    def __init__(self, username, store_id):
        super(Inventory, self).__init__()

        self.username = username
        self.store_id = store_id

        self.qButtonGroup = QButtonGroup()

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password=None,
                                          db="grocerytech",
                                          charset="utf8mb4")

        self.initUI()

    def initUI(self):

        root = QVBoxLayout()
        bottom = QHBoxLayout()

        self.instructions = QLabel("To update inventory, click the item/quantity cell you wish to change, enter the new quantity, and press enter.\nTo delete an item, check the circle under 'Select' and press 'Delete Item'.")
        root.addWidget(self.instructions)

        self.tableWidget = self.populate()
        self.tableWidget.setMinimumWidth(700)

        self.back = QPushButton("Back")
        self.update = QPushButton("Update Item")
        self.delete = QPushButton("Delete Item")

        self.back.setMaximumWidth(75)
        self.update.setMaximumWidth(100)
        self.delete.setMaximumWidth(100)

        bottom.addWidget(self.back)
        bottom.addWidget(self.update)
        bottom.addWidget(self.delete)

        self.back.clicked.connect(self.backClicked)
        self.update.clicked.connect(self.updateClicked)
        self.delete.clicked.connect(self.deleteClicked)

        root.addWidget(self.tableWidget)
        root.addLayout(bottom)

        self.setLayout(root)
        self.setWindowTitle("Inventory")
        self.setGeometry(300, 150, 850, 400)

        self.show()

    def backClicked(self):
        self.manageFunctWindow = ManagerFunctionality.ManagerFunctWindow(self.username)
        self.manageFunctWindow.show()
        self.close()

        self.connection.close()

    def updateClicked(self):
        item_IDs = self.getItemIDs()

        if item_IDs == []:
            return

        quantities = []
        for id in item_IDs:
            quantity = str(self.getQuantity(id))
            quantities.append(quantity)

        for i in range(len(item_IDs)):
            current_quantity = self.tableWidget.item(i, 3).text()

            if current_quantity != quantities[i]:
                self.updateQuantity(current_quantity, item_IDs[i])


    def deleteClicked(self):
        index = self.qButtonGroup.checkedId()

        if index == -1:

            self.noItemSelected = NoItemSelected(self.username, self.store_id)
            self.noItemSelected.show()
            self.close()

        else:

            item_id = self.getItemIDs()[index]

            self.confDelete = ConfirmDeleteItem(item_id, self.getItemName(item_id), self.username, self.store_id)
            self.confDelete.show()
            self.close()

        self.connection.close()

    def updateQuantity(self, current_quantity, item_id):
        cursor = self.connection.cursor()

        update = ('UPDATE ITEM SET quantity={} WHERE item_id={};'.format(current_quantity, item_id))
        cursor.execute(update)
        self.connection.commit()

        self.updateSuccess = UpdateSuccessful(self.username, self.store_id)
        self.updateSuccess.show()
        self.close()

        self.connection.close()

    def populate(self):
        table = QTableWidget()
        table.setColumnCount(7)
        table.setColumnWidth(2, 150)
        table.setRowCount(self.getRowCount())
        table.setHorizontalHeaderLabels(["Select", "Item Name", "Description", "Quantity", "Retail Price", "Wholesale Price", "Exp. Date"])

        item_IDs = self.getItemIDs()

        for i in range(self.getRowCount()):
            radioBtn = QRadioButton()
            self.qButtonGroup.addButton(radioBtn, i)
            table.setCellWidget(i, 0, radioBtn)

            for j in range(6):

                if j == 0:
                    itemName = QTableWidgetItem(self.getItemName(item_IDs[i]))
                    itemName.setTextAlignment(Qt.AlignCenter)
                    itemName.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 1, itemName)

                if j == 1:
                    description = QTableWidgetItem(self.getDescription(item_IDs[i]))
                    description.setTextAlignment(Qt.AlignCenter)
                    description.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 2, description)

                if j == 2:
                    quantity = QTableWidgetItem(str(self.getQuantity(item_IDs[i])))
                    quantity.setTextAlignment(Qt.AlignCenter)
                    table.setItem(i, 3, quantity)

                if j == 3:
                    retailPrice = QTableWidgetItem(str(self.getRetailPrice(item_IDs[i])))
                    retailPrice.setTextAlignment(Qt.AlignCenter)
                    retailPrice.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 4, retailPrice)

                if j == 4:
                    wholePrice = QTableWidgetItem(str(self.getWholesalePrice(item_IDs[i])))
                    wholePrice.setTextAlignment(Qt.AlignCenter)
                    wholePrice.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 5, wholePrice)

                if j == 5:
                    expDate = QTableWidgetItem(str(self.getExpDate(item_IDs[i])))
                    expDate.setTextAlignment(Qt.AlignCenter)
                    expDate.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 6, expDate)

        return table

    def getRowCount(self):
        cursor = self.connection.cursor()

        select =('SELECT COUNT(*) FROM ITEM, SOLDAT WHERE ITEM.item_id=SOLDAT.item_id and SOLDAT.store_id={};'.format(self.store_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getItemIDs(self):
        cursor = self.connection.cursor()

        select = ('SELECT item_id FROM SOLDAT WHERE store_id={};'.format(self.store_id))
        cursor.execute(select)
        found = cursor.fetchall()

        if found == ():
            return []

        item_IDs = []
        for num in found:
            item_IDs.append(num[0])

        return item_IDs

    def getItemName(self, item_id):
        cursor = self.connection.cursor()

        select = ('SELECT item_name FROM ITEM WHERE item_id={};'.format(item_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getDescription(self, item_id):
        cursor = self.connection.cursor()

        select = ('SELECT description FROM ITEM WHERE item_id={};'.format(item_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getQuantity(self, item_id):
        cursor = self.connection.cursor()

        select = ('SELECT quantity FROM ITEM WHERE item_id={};'.format(item_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getRetailPrice(self, item_id):
        cursor = self.connection.cursor()

        select = ('SELECT listed_price FROM ITEM WHERE item_id={};'.format(item_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getWholesalePrice(self, item_id):
        cursor = self.connection.cursor()

        select = ('SELECT wholesale_price FROM ITEM WHERE item_id={};'.format(item_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getExpDate(self, item_id):
        cursor = self.connection.cursor()

        select = ('SELECT exp_date FROM ITEM WHERE item_id={};'.format(item_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

class ConfirmDeleteItem(QWidget):

    def __init__(self, item_id, item_name, username, store_id):
        super(ConfirmDeleteItem, self).__init__()

        self.item_id = item_id
        self.item_name = item_name
        self.username = username
        self.store_id = store_id

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password=None,
                                          db="grocerytech",
                                          charset="utf8mb4")

        self.initUI()

    def initUI(self):

        root = QVBoxLayout()
        msg = QHBoxLayout()
        btns = QGridLayout()

        self.message = QLabel("ARE YOU SURE YOU WANT TO DELETE THIS ITEM?\nPAYMENT NAME: {}".format(self.item_name))
        self.message.setStyleSheet("color: red")
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
        self.setGeometry(400, 250, 100, 75)
        self.setWindowTitle("Confirm Delete Item")
        self.show()

    def cancelClicked(self):
        self.backToInventory()

    def confClicked(self):
        cursor = self.connection.cursor()

        delete = ('DELETE FROM ITEM WHERE item_id={};'.format(self.item_id))
        cursor.execute(delete)
        self.connection.commit()

        self.backToInventory()

    def backToInventory(self):
        self.invWin = Inventory(self.username, self.store_id)
        self.invWin.show()
        self.close()

        self.connection.close()

class NoItemSelected(QMessageBox):

    def __init__(self, username, store_id):
        super(NoItemSelected, self).__init__()

        self.username = username
        self.store_id = store_id

        self.initUI()

    def initUI(self):
        self.setIcon(QMessageBox.Information)
        self.setText("There was an error")
        self.setInformativeText('You must check an item before deleting.')
        self.setDetailedText('Click a button under the "Select" column, then click "Delete Item".')
        self.setStandardButtons(QMessageBox.Ok)
        self.buttonClicked.connect(self.btnClicked)

        self.show()

    def btnClicked(self):
        self.invWin = Inventory(self.username, self.store_id)
        self.invWin.show()
        self.close()

class UpdateSuccessful(QWidget):

    def __init__(self, username, store_id):
        super(UpdateSuccessful, self).__init__()

        self.username = username
        self.store_id = store_id

        self.initUI()

    def initUI(self):

        root = QVBoxLayout()
        msg = QHBoxLayout()
        btns = QGridLayout()

        self.message = QLabel("THE INVENTORY HAS BEEN SUCCESSFULLY UPDATE")
        msg.addWidget(self.message)

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.okClicked)

        btns.addWidget(self.okBtn, 1, 4)

        root.addLayout(msg)
        root.addLayout(btns)
        self.setLayout(root)
        self.setGeometry(500, 250, 150, 150)
        self.setWindowTitle("Item Updated")
        self.show()

    def okClicked(self):
        self.acctInfo = Inventory(self.username, self.store_id)
        self.acctInfo.show()
        self.close()



