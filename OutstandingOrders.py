import pymysql

from GROCERYTECH_final import ManagerFunctionality

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class OutstandingOrders(QWidget):

    def __init__(self, username, store_id):
        super(OutstandingOrders, self).__init__()

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

        self.tableWidget = self.populate()

        self.back = QPushButton("Back")
        self.back.setMaximumWidth(75)

        bottom.addWidget(self.back)

        self.back.clicked.connect(self.backClicked)

        root.addWidget(self.tableWidget)
        root.addLayout(bottom)
        self.setLayout(root)
        self.setWindowTitle("Outstanding Orders")
        self.setGeometry(300, 150, 850, 600)

        self.show()

    def backClicked(self):
        self.managerFunctWindow = ManagerFunctionality.ManagerFunctWindow(self.username)
        self.managerFunctWindow.show()
        self.close()

        self.connection.close()

    def populate(self) -> QWidget:
        table = QTableWidget()
        table.setColumnCount(7)
        table.setColumnWidth(6, 200)
        table.setRowCount(self.getRowCount())
        table.setHorizontalHeaderLabels(["Select", "Store Address", "Order ID", "Date", "Total Price", "Num of Items", "Delivery Address"])

        order_IDs = self.getOrderIDs()

        for i in range(self.getRowCount()):

            for j in range(7):
                if j == 0:
                    storeName = QTableWidgetItem(self.getStoreName(order_IDs[i]))
                    storeName.setTextAlignment(Qt.AlignCenter)
                    storeName.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, j, storeName)

                if j == 1:
                    storeAddress = QTableWidgetItem(self.getStoreAddress(order_IDs[i]))
                    storeAddress.setTextAlignment(Qt.AlignCenter)
                    storeAddress.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, j, storeAddress)

                if j == 2:
                    order_id = QTableWidgetItem(str(order_IDs[i]))
                    order_id.setTextAlignment(Qt.AlignCenter)
                    order_id.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, j, order_id)

                if j == 3:
                    date = QTableWidgetItem(self.getOrderDate(order_IDs[i]))
                    date.setTextAlignment(Qt.AlignCenter)
                    date.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, j, date)

                if j == 4:
                    price = QTableWidgetItem(str(self.getTotalPrice(order_IDs[i])))
                    price.setTextAlignment(Qt.AlignCenter)
                    price.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, j, price)

                if j == 5:
                    num_items = QTableWidgetItem(str(self.getNumItems(order_IDs[i])))
                    num_items.setTextAlignment(Qt.AlignCenter)
                    num_items.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, j, num_items)

                if j == 6:
                    del_address = QTableWidgetItem(self.getDelAddress(order_IDs[i]))
                    del_address.setTextAlignment(Qt.AlignCenter)
                    del_address.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, j, del_address)

        return table


    def getRowCount(self):
        cursor = self.connection.cursor()

        select = ('SELECT COUNT(*) from DELIVEREDBY, ORDERR, ORDERFROM WHERE DELIVEREDBY.order_id=ORDERR.order_id and ORDERFROM.order_id=ORDERR.order_id and is_delivered=0 and store_address_id={};'.format(self.store_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getOrderIDs(self):
        cursor = self.connection.cursor()

        select = ('SELECT ORDERR.order_id from DELIVEREDBY, ORDERR, ORDERFROM WHERE DELIVEREDBY.order_id=ORDERR.order_id and ORDERFROM.order_id=ORDERR.order_id and is_delivered=0 and store_address_id={};'.format(self.store_id))
        cursor.execute(select)

        found = cursor.fetchall()

        if found == ():
            return []

        order_IDs = []
        for id in found:
            order_IDs.append(id[0])

        return order_IDs

    def getStoreName(self, order_id):
        cursor = self.connection.cursor()

        select = ('SELECT store_name FROM GROCERYSTORE, ORDERFROM WHERE GROCERYSTORE.store_id=ORDERFROM.store_address_id and ORDERFROM.order_id={};'.format(order_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getStoreID(self, order_id):
        cursor = self.connection.cursor()

        select = ('SELECT store_id FROM GROCERYSTORE, ORDERFROM WHERE GROCERYSTORE.store_id=ORDERFROM.store_address_id and ORDERFROM.order_id={};'.format(order_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getStoreAddress(self, order_id):
        store_id = self.getStoreID(order_id)
        cursor1 = self.connection.cursor()
        cursor2 = self.connection.cursor()

        select = ('SELECT house_number FROM ADDRESS, GROCERYSTORE WHERE ADDRESS.id=GROCERYSTORE.address_id and GROCERYSTORE.store_id={};'.format(store_id))
        cursor1.execute(select)
        house_number = str(cursor1.fetchone()[0])

        select = ('SELECT street FROM ADDRESS, GROCERYSTORE WHERE ADDRESS.id=GROCERYSTORE.address_id and GROCERYSTORE.store_id={};'.format(store_id))
        cursor2.execute(select)
        street = cursor2.fetchone()[0]

        return (house_number + " " + street)

    def getOrderDate(self, order_id):
        cursor = self.connection.cursor()

        select = ('SELECT order_placed_date FROM ORDERR WHERE order_id={};'.format(order_id))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getTotalPrice(self, order_id):
        cursor = self.connection.cursor()

        select = ('SELECT (SUM(listed_price * SELECTITEM.quantity)) FROM SELECTITEM, ITEM, ORDERR WHERE SELECTITEM.order_id=ORDERR.order_id and SELECTITEM.item_id=ITEM.item_id and ORDERR.order_id={};'.format(order_id))
        cursor.execute(select)
        return str(cursor.fetchone()[0])

    def getNumItems(self, order_id):
        cursor = self.connection.cursor()

        select = ('SELECT COUNT(SELECTITEM.quantity) FROM SELECTITEM WHERE order_id={};'.format(order_id))
        cursor.execute(select)
        return str(cursor.fetchone()[0])

    def getDelAddress(self, order_id):
        cursor1 = self.connection.cursor()
        cursor2 = self.connection.cursor()
        cursor3 = self.connection.cursor()
        cursor4 = self.connection.cursor()
        cursor5 = self.connection.cursor()
        cursor6 = self.connection.cursor()

        select1 = ('SELECT buyer_username FROM ORDEREDBY, BUYER WHERE ORDEREDBY.order_id={};'.format(order_id))
        cursor1.execute(select1)

        buyer_username = cursor1.fetchone()[0]

        select2 = ('SELECT house_number FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and BUYER.username="{}";'.format(buyer_username))
        cursor2.execute(select2)

        house_number = str(cursor2.fetchone()[0])

        select3 = ('SELECT street FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and BUYER.username="{}";'.format(buyer_username))
        cursor3.execute(select3)

        street = cursor3.fetchone()[0]

        select4 = ('SELECT city FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and BUYER.username="{}";'.format(buyer_username))
        cursor4.execute(select4)

        city = cursor4.fetchone()[0]

        select5 = ('SELECT state FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and BUYER.username="{}";'.format(buyer_username))
        cursor5.execute(select5)

        state = cursor5.fetchone()[0]

        select6 = ('SELECT zip_code FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and BUYER.username="{}";'.format(buyer_username))
        cursor6.execute(select6)

        zip_code = str(cursor6.fetchone()[0])

        return (house_number + " " + street + ", " + city + ", " + state + " " + zip_code)










