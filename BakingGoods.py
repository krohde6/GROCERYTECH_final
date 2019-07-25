from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from GROCERYTECH_final import FindItem
from GROCERYTECH_final import AddToCart
from GROCERYTECH_final import Checkout

import pymysql

class BakingGoods(QWidget):

    def __init__(self, username, store_id, order_id):
        super(BakingGoods, self).__init__()
        self.username = username
        self.store_id = store_id
        self.order_id = order_id
        self.food_group = BakingGoods
        self.qButtonGroup = QButtonGroup()
        self.connection = pymysql.connect(host='localhost',
                                     user = 'root',
                                     password=None,
                                     db = 'GroceryTech',
                                     charset = 'utf8mb4')


        self.initUI()

    def initUI(self):

        #setLayout
        root = QVBoxLayout()
        bottom = QHBoxLayout()


        #widgets

        self.back = QPushButton("Back")
        self.addtocart = QPushButton("Add to Cart")
        self.checkout = QPushButton("Checkout")
        self.bakinggoodstable = self.populate()

        bottom.addWidget(self.back)
        bottom.addWidget(self.addtocart)
        bottom.addWidget(self.checkout)

        self.back.clicked.connect(self.backClicked)
        self.addtocart.clicked.connect(self.addtoCart)
        self.checkout.clicked.connect(self.checkOut)

        root.addWidget(self.bakinggoodstable)
        root.addLayout(bottom)
        self.setLayout(root)
        self.setWindowTitle("Baking Goods")
        self.setGeometry(550, 450, 600, 300)



        self.show()


    def backClicked(self):
        self.connection.close()

        self.FindItem = FindItem.FindItem(self.username, self.store_id, self.order_id)
        self.FindItem.show()
        self.close()


    def addtoCart(self):

        numRow = self.getRowCount()
        item_IDs = self.getItemIDs()

        for i in range(numRow):
            currrent_value = int(self.bakinggoodstable.item(i, 0).text())

            if currrent_value != 0:
                AddToCart.addToCart(self.order_id, item_IDs[i], currrent_value)



    def checkOut(self):
        self.connection.close()

        self.checkOut = Checkout.Checkout(self.username, self.store_id, self.order_id)
        self.checkOut.show()
        self.close()

    def populate(self):

        bakinggoodstable = QTableWidget()
        bakinggoodstable.setRowCount(self.getRowCount())
        bakinggoodstable.setColumnCount(6)
        bakinggoodstable.setHorizontalHeaderLabels(['Quantity','Item Name', 'Description','Expiration Date','Price','In Stock'])

        item_IDs = self.getItemIDs()

        for i in range(self.getRowCount()):
            # spinBox = QSpinBox()
            # spinBox.setValue(0)
            # bakinggoodstable.setCellWidget(i, 0, spinBox)

            default_quantity = QTableWidgetItem("0")
            bakinggoodstable.setItem(i, 0, default_quantity)

            for j in range(5):
                if j == 0:
                    itemName = QTableWidgetItem(self.getItemName(item_IDs[i]))
                    itemName.setTextAlignment(Qt.AlignCenter)
                    itemName.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    bakinggoodstable.setItem(i, 1, itemName)

                if j == 1:
                    description = QTableWidgetItem(self.getDescription(item_IDs[i]))
                    description.setTextAlignment(Qt.AlignCenter)
                    description.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    bakinggoodstable.setItem(i, 2, description)

                if j == 2:
                    quantity = QTableWidgetItem(str(self.getExpDate(item_IDs[i])))
                    quantity.setTextAlignment(Qt.AlignCenter)
                    quantity.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    bakinggoodstable.setItem(i, 3, quantity)

                if j == 3:
                    retailPrice = QTableWidgetItem(str(self.getRetailPrice(item_IDs[i])))
                    retailPrice.setTextAlignment(Qt.AlignCenter)
                    retailPrice.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    bakinggoodstable.setItem(i, 4, retailPrice)

                if j == 4:
                    expDate = QTableWidgetItem(str(self.getQuantity(item_IDs[i])))
                    expDate.setTextAlignment(Qt.AlignCenter)
                    expDate.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    bakinggoodstable.setItem(i, 6, expDate)

        return bakinggoodstable

    def getRowCount(self):
        cursor = self.connection.cursor()
        numofRows = 'select count(*) from item, grocerystore, soldat where food_group="Baking Goods" and item.item_id=soldat.item_id and soldat.store_id=grocerystore.store_id and grocerystore.store_id={};'.format(self.store_id)

        cursor.execute(numofRows)
        return cursor.fetchone()[0]


    def getItemIDs(self):
        cursor = self.connection.cursor()

        select = ('SELECT item.item_id FROM ITEM, SOLDAT WHERE item.item_id = soldat.item_id and food_group = "Baking Goods" and soldat.store_id={};'.format(self.store_id))
        cursor.execute(select)
        found = cursor.fetchall()



        item_IDs = []
        for num in found:
            item_IDs.append(num[0])

        return item_IDs

    def getExpDate(self, item_id):
        cursor = self.connection.cursor()

        select = ('SELECT item.exp_date FROM ITEM WHERE food_group = "Baking Goods" and item_id={};'.format(item_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getItemName(self, item_id):
        cursor = self.connection.cursor()

        select = ('SELECT item.item_name FROM ITEM WHERE food_group = "Baking Goods" and item_id={};'.format(item_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getRetailPrice(self, item_id):
        cursor = self.connection.cursor()

        select = ('SELECT item.listed_price FROM ITEM WHERE food_group = "Baking Goods" and item_id={};'.format(item_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getDescription(self, item_id):
        cursor = self.connection.cursor()

        select = ('SELECT item.description FROM ITEM WHERE food_group = "Baking Goods" and item_id={};'.format(item_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getQuantity(self, item_id):
        cursor = self.connection.cursor()

        select = ('SELECT item.quantity FROM ITEM WHERE food_group = "Baking Goods" and item_id={};'.format(item_id))
        cursor.execute(select)
        if cursor.fetchone()[0] > 0:
            return 'Yes'
        else:
            return 'No'





        #help populate Baking Goods
        #select grocerystore.store_id, store_name, item_name from item, grocerystore, soldat where food_group="Baking Goods" and soldat.store_id=grocerystore.store_id and item.item_id=soldat.item_id;
