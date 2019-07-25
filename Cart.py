import pymysql

from GROCERYTECH_final import StoreHomepage
from GROCERYTECH_final import BuyerFunctionality
from GROCERYTECH_final import Checkout

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Cart(QWidget):

    def __init__(self, username, store_id, order_id):
        super(Cart, self).__init__()

        self.username = username
        self.store_id = store_id
        self.order_id = order_id

        self.qRadioGroup = QButtonGroup()
        self.qSpinGroup = QButtonGroup()

        self.numItems = 0

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password=None,
                                          db="grocerytech",
                                          charset="utf8mb4")

        self.initUI()

    def initUI(self):

        root = QVBoxLayout()
        bottom = QHBoxLayout()

        self.instructions = QLabel("To update quantity, click the item/quantity cell you wish to change, enter the new quantity, and press 'Update'.\nTo delete an item, check the circle under 'Select' and press 'Delete'.")
        root.addWidget(self.instructions)

        self.tableWidget = self.populate()
        self.tableWidget.setMinimumWidth(700)

        self.back = QPushButton("Back")
        self.delete = QPushButton("Delete")
        self.update = QPushButton("Update")
        self.checkout = QPushButton("Checkout")

        self.item = QLabel(str(self.numItems))

        self.back.setMaximumWidth(75)
        self.delete.setMaximumWidth(100)
        self.checkout.setMaximumWidth(120)

        bottom.addWidget(self.item)
        bottom.addWidget(self.back)
        bottom.addWidget(self.delete)
        bottom.addWidget(self.update)
        bottom.addWidget(self.checkout)

        self.back.clicked.connect(self.backClicked)
        self.delete.clicked.connect(self.deleteClicked)
        self.update.clicked.connect(self.updateClicked)
        self.checkout.clicked.connect(self.checkoutClicked)

        root.addWidget(self.tableWidget)
        root.addLayout(bottom)

        self.setLayout(root)
        self.setWindowTitle("Cart")
        self.setGeometry(300, 150, 600, 400)

        self.show()

    def backClicked(self):
        self.storeHomepage = StoreHomepage.StoreHomepage(self.username, self.store_id, self.order_id)
        self.storeHomepage.show()
        self.close()

        self.connection.close()

    def deleteClicked(self):
        index = self.qRadioGroup.checkedId()
        item_id = self.getItemIDs()[index]

        cursor = self.connection.cursor()
        delete = ('DELETE FROM SELECTITEM WHERE item_id={} and order_id={};'.format(item_id, self.order_id))
        cursor.execute(delete)
        self.connection.commit()

        self.connection.close()

        self.updateCart = Cart(self.username, self.store_id, self.order_id)
        self.updateCart.show()
        self.close()

    def updateClicked(self):
        item_IDs = self.getItemIDs()

        if item_IDs == []:
            return

        for i in range(len(item_IDs)):
            quantity = self.getQuantity(item_IDs[i])

            new_quantity = int(self.tableWidget.item(i, 3).text())

            if quantity != new_quantity:
                cursor = self.connection.cursor()
                update = ('UPDATE SELECTITEM SET quantity={} WHERE item_id={} and order_id={};'.format(new_quantity, item_IDs[i], self.store_id))
                cursor.execute(update)
                self.connection.commit()

                updateCart = Cart(self.username, self.store_id, self.order_id)
                updateCart.show()
                self.close()


    def checkoutClicked(self):
        self.checkoutWin = Checkout.Checkout(self.username, self.store_id, self.order_id)
        self.checkoutWin.show()
        self.close()

        self.connection.close()

    def populate(self):
        table = QTableWidget()

        table.setColumnCount(6)
        table.setRowCount(self.getNumRows())
        table.setMinimumHeight(300)
        table.setHorizontalHeaderLabels(["Select", "Item Name", "Description", "Quantity", "Price", "In Stock"])
        table.setColumnWidth(2, 600)

        item_IDs = self.getItemIDs()

        for i in range(self.getNumRows()):
            radioBtn = QRadioButton()
            self.qButtonGroup.addButton(radioBtn, i)
            table.setCellWidget(i, 0, radioBtn)

            for j in range(5):

                if j == 0:
                    item_name = QTableWidgetItem(self.getItemName(item_IDs[i]))
                    item_name.setTextAlignment(Qt.AlignCenter)
                    item_name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    table.setItem(i, 1, item_name)

                if j == 1:
                    description = QTableWidgetItem(self.getDescription(item_IDs[i]))
                    description.setTextAlignment(Qt.AlignCenter)
                    description.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    table.setItem(i, 2, description)

                if j == 2:
                    quantity = self.getQuantity(item_IDs[i])

                    spin = QSpinBox()
                    self.qSpinGroup.addButton(spin, i)
                    spin.setValue(self.getCartQuantity(item_IDs[i]))
                    spin.setMaximum(quantity)

                    table.setCellWidget(i, 3, spin)

                if j == 3:
                    item_quantity = self.getQuantity(item_IDs[i])
                    price = self.getPrice(item_IDs[i])

                    sum_total = item_quantity * price

                    self.numItems += item_quantity

                    total_price = QTableWidgetItem(str(sum_total))
                    total_price.setTextAlignment(Qt.AlignCenter)
                    total_price.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 4, total_price)

                if j == 4:
                    in_stock = QTableWidgetItem(self.isInStock(item_IDs[i]))
                    in_stock.setTextAlignment(Qt.AlignCenter)
                    in_stock.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 5, in_stock)

        return table


    def getNumRows(self):
        cursor = self.connection.cursor()

        select = ('SELECT COUNT(*) FROM SELECTITEM, ORDERR WHERE SELECTITEM.order_id=ORDERR.order_id and ORDERR.order_id={};'.format(self.order_id))
        cursor.execute(select)

        return cursor.fetchone()[0]

    def getItemIDs(self):
        cursor = self.connection.cursor()

        select = ('SELECT item_id FROM SELECTITEM, ORDERR WHERE SELECTITEM.order_id=ORDERR.order_id and ORDERR.order_id={};'.format(self.order_id))
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

    def getPrice(self, item_id):
        cursor = self.connection.cursor()

        select = ('SELECT listed_price FROM ITEM WHERE item_id={};'.format(item_id))
        cursor.execute(select)

        return cursor.fetchone()[0]

    def isInStock(self, item_id):
        if self.getInventory(item_id) > 0:
            return "YES"

        return "NO"

    def getInventory(self, item_id):
        cursor = self.connection.cursor()

        select = ('SELECT quantity FROM ITEM WHERE item_id={};'.format(item_id))
        cursor.execute(select)

        return cursor.fetchone()[0]

    def getCartQuantity(self, item_id):
        cursor = self.connection.cursor()

        select = ('SELECT quantity FROM SELECTITEM WHERE order_id={} and item_id={};'.format(self.order_id, item_id))
        cursor.execute(select)

        return cursor.fetchone()[0]


class ConfirmDeleteOrder(QWidget):

    def __init__(self, username, store_id, order_id):
        super(ConfirmDeleteOrder, self).__init__()

        self.username = username
        self.store_id = store_id
        self.order_id = order_id

        self.initUI()

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password="kwrohde",
                                          db="grocerytech",
                                          charset="utf8mb4")

    def initUI(self):

        root = QVBoxLayout()
        msg = QHBoxLayout()
        btns = QGridLayout()

        self.message = QLabel("ARE YOU SURE YOU WANT TO DELETE YOUR ORDER?")
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
        self.setWindowTitle("Confirm Order Deletion")
        self.show()

    def cancelClicked(self):
        self.connection.close()

        self.cart = Cart(self.username, self.store_id, self.order_id)
        self.cart.show()
        self.close()

    def confClicked(self):
        cursor = self.connection.cursor()

        delete = ('DELETE FROM ORDERR WHERE order_id={};'.format(self.order_id))

        cursor.execute(delete)
        self.connection.commit()

        self.connection.close()

        self.buyerFunct = BuyerFunctionality.BuyerFunctWindow(self.username)
        self.buyerFunct.show()
        self.close()





