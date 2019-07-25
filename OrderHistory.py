import pymysql

from GROCERYTECH_final import BuyerFunctionality
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class OrderHistory(QWidget):

    def __init__(self, username):
        super(OrderHistory, self).__init__()

        self.username = username

        self.qbuttonGroup = QButtonGroup()

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
        self.tableWidget.setMinimumWidth(600)

        self.back = QPushButton("Back")
        self.viewDetails = QPushButton("View Order Details")

        self.back.setMaximumWidth(75)
        self.viewDetails.setMaximumWidth(150)

        bottom.addWidget(self.back)
        bottom.addWidget(self.viewDetails)

        self.back.clicked.connect(self.backClicked)
        self.viewDetails.clicked.connect(self.viewDetailsClicked)

        root.addWidget(self.tableWidget)
        root.addLayout(bottom)

        self.setLayout(root)
        self.setWindowTitle("Order History")
        self.setGeometry(300, 150, 800, 350)

        self.show()


    def backClicked(self):
        self.buyerFunct = BuyerFunctionality.BuyerFunctWindow(self.username)
        self.buyerFunct.show()
        self.close()

        self.connection.close()

    def viewDetailsClicked(self):
        index = self.qbuttonGroup.checkedId()

        if index == -1:

            self.noOrderSelected = NoOrderSelected(self.username)
            self.noOrderSelected.show()
            self.close()

        else:

            order_id = self.getOrderIDs()[index]

            self.viewDets = ViewOrderDetails(order_id, self.username)
            self.viewDets.show()
            self.close()

            self.connection.close()


    def populate(self):
        table = QTableWidget()
        table.setColumnCount(7)
        table.setRowCount(self.getRowCount())
        table.setHorizontalHeaderLabels(["Select", "Store Name", "Order ID", "Date", "Total Price", "Num Items", "Delivered"])

        order_IDs = self.getOrderIDs()

        for i in range(self.getRowCount()):
            radioBtn = QRadioButton()
            self.qbuttonGroup.addButton(radioBtn, i)
            table.setCellWidget(i, 0, radioBtn)

            for j in range(6):

                if j == 0:
                    store_name = QTableWidgetItem(self.getStoreName(order_IDs[i]))
                    store_name.setTextAlignment(Qt.AlignCenter)
                    store_name.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 1, store_name)

                if j == 1:
                    order_id = QTableWidgetItem(str(order_IDs[i]))
                    order_id.setTextAlignment(Qt.AlignCenter)
                    order_id.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 2, order_id)

                if j == 2:
                    date = QTableWidgetItem(self.getDate(order_IDs[i]))
                    date.setTextAlignment(Qt.AlignCenter)
                    date.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 3, date)

                if j == 3:
                    total_price = QTableWidgetItem(str(self.getTotalPrice(order_IDs[i])))
                    total_price.setTextAlignment(Qt.AlignCenter)
                    total_price.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 4, total_price)

                if j == 4:
                    num_items = QTableWidgetItem(str(self.getNumItems(order_IDs[i])))
                    num_items.setTextAlignment(Qt.AlignCenter)
                    num_items.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 5, num_items)

                if j == 5:
                    deliver = self.getDelivered(order_IDs[i])

                    delivered = QTableWidgetItem(deliver)
                    delivered.setTextAlignment(Qt.AlignCenter)
                    delivered.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 6, delivered)

        return table



    def getRowCount(self):
        cursor = self.connection.cursor()

        select = ('SELECT COUNT(*) FROM ORDEREDBY WHERE buyer_username="{}";'.format(self.username))
        cursor.execute(select)

        return cursor.fetchone()[0]

    def getOrderIDs(self):
        cursor = self.connection.cursor()

        select = ('SELECT order_id FROM ORDEREDBY WHERE buyer_username="{}";'.format(self.username))
        cursor.execute(select)
        found = cursor.fetchall()

        if found == ():
            return []

        order_IDs = []
        for num in found:
            order_IDs.append(num[0])

        return order_IDs

    def getStoreName(self, order_id):
        cursor = self.connection.cursor()

        select = ('SELECT store_name FROM ORDERFROM, ORDEREDBY, GROCERYSTORE WHERE ORDERFROM.store_address_id=GROCERYSTORE.store_id and ORDEREDBY.order_id=ORDERFROM.order_id and ORDEREDBY.order_id={};'.format(order_id))
        cursor.execute(select)

        return cursor.fetchone()[0]

    def getDate(self, order_id):
        cursor = self.connection.cursor()

        select = ('SELECT order_placed_date FROM ORDERR WHERE order_id={};'.format(order_id))
        cursor.execute(select)

        return cursor.fetchone()[0]

    def getTotalPrice(self, order_id):
        cursor = self.connection.cursor()

        select = ('SELECT SUM(ITEM.listed_price * SELECTITEM.quantity) FROM ORDERR, SELECTITEM, ITEM WHERE ORDERR.order_id=SELECTITEM.order_id and SELECTITEM.item_id=ITEM.item_id and ORDERR.order_id={};'.format(order_id))
        cursor.execute(select)

        return cursor.fetchone()[0]

    def getNumItems(self, order_id):
        cursor = self.connection.cursor()

        select = ('SELECT COUNT(*) FROM SELECTITEM WHERE order_id={};'.format(order_id))
        cursor.execute(select)

        return cursor.fetchone()[0]

    def getDelivered(self, order_id):
        cursor = self.connection.cursor()

        select = ('SELECT is_delivered FROM DELIVEREDBY WHERE order_id={};'.format(order_id))
        cursor.execute(select)
        found = cursor.fetchone()

        if found is None:
            return "NO"
        return "YES"


class ViewOrderDetails(QWidget):

    def __init__(self, order_id, username):
        super(ViewOrderDetails, self).__init__()

        self.order_id = order_id
        self.username = username
        self.order_total = 0

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
        self.tableWidget.setMinimumWidth(700)

        self.back = QPushButton("Back")
        self.total = QLabel(str("ORDER TOTAL: " + "$" + str(self.order_total)))
        self.back.setMaximumWidth(75)
        bottom.addWidget(self.back)
        bottom.addWidget(self.total)

        self.back.clicked.connect(self.backClicked)

        root.addWidget(self.tableWidget)
        root.addLayout(bottom)

        self.setLayout(root)
        self.setWindowTitle("Order Details")
        self.setGeometry(300, 150, 500, 350)
        self.show()

    def backClicked(self):
        self.ordrHist = OrderHistory(self.username)
        self.ordrHist.show()
        self.close()

        self.connection.close()

    def populate(self):
        table = QTableWidget()
        table.setMinimumWidth(500)
        table.setColumnCount(4)
        table.setColumnWidth(1, 150)
        table.setRowCount(self.getRowCount())
        table.setHorizontalHeaderLabels(["Item Name", "Description", "Quantity", "Price"])

        item_IDs = self.getItemIDs()

        for i in range(self.getRowCount()):
            table.setRowHeight(i, 60)

            for j in range(4):

                if j == 0:
                    item_name = QTableWidgetItem(self.getItemName(item_IDs[i]))
                    item_name.setTextAlignment(Qt.AlignCenter)
                    item_name.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, j, item_name)

                if j == 1:
                    description = QTableWidgetItem(self.getDescription(item_IDs[i]))
                    description.setTextAlignment(Qt.AlignCenter)
                    description.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, j, description)

                if j == 2:
                    quantity = QTableWidgetItem(str(self.getQuantity(item_IDs[i])))
                    quantity.setTextAlignment(Qt.AlignCenter)
                    quantity.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, j, quantity)

                if j == 3:
                    item_quantity = self.getQuantity(item_IDs[i])
                    price = self.getPrice(item_IDs[i])

                    sum_total = item_quantity * price

                    self.order_total += sum_total

                    total_price = QTableWidgetItem(str(sum_total))
                    total_price.setTextAlignment(Qt.AlignCenter)
                    total_price.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, j, total_price)

        return table

    def getRowCount(self):
        cursor = self.connection.cursor()

        select = ('SELECT COUNT(*) FROM SELECTITEM WHERE order_id={};'.format(self.order_id))
        cursor.execute(select)

        return cursor.fetchone()[0]

    def getItemIDs(self):
        cursor = self.connection.cursor()

        select = ('SELECT item_id FROM SELECTITEM WHERE order_id={};'.format(self.order_id))
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

        select = ('SELECT quantity FROM SELECTITEM WHERE item_id={} and order_id={};'.format(item_id, self.order_id))
        cursor.execute(select)

        return cursor.fetchone()[0]

    def getPrice(self, item_id):
        cursor = self.connection.cursor()

        select = ('SELECT listed_price FROM ITEM WHERE item_id={};'.format(item_id))
        cursor.execute(select)

        return cursor.fetchone()[0]


class NoOrderSelected(QMessageBox):

    def __init__(self, username):
        super(NoOrderSelected, self).__init__()

        self.username = username

        self.initUI()

    def initUI(self):
        self.setIcon(QMessageBox.Information)
        self.setText("There was an error")
        self.setInformativeText('You must select an order to view the details.')
        self.setDetailedText('Click a button under the "Select" column, then click "View Details".')
        self.setStandardButtons(QMessageBox.Ok)
        self.buttonClicked.connect(self.btnClicked)

        self.show()

    def btnClicked(self):
        self.orderHist = OrderHistory(self.username)
        self.orderHist.show()
        self.close()



