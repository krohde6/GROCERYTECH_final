import pymysql

from GROCERYTECH_final import DelivererFunctionality

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Assignments(QWidget):

    def __init__(self, username):
        super(Assignments, self).__init__()

        self.username = username
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
        self.tableWidget.setMinimumWidth(800)

        self.back = QPushButton("Back")
        self.viewDets = QPushButton("View Assignment Details")

        self.back.setMaximumWidth(75)
        self.viewDets.setMaximumWidth(200)

        bottom.addWidget(self.back)
        bottom.addWidget(self.viewDets)

        self.back.clicked.connect(self.backClicked)
        self.viewDets.clicked.connect(self.viewDetsClicked)

        root.addWidget(self.tableWidget)
        root.addLayout(bottom)

        self.setLayout(root)
        self.setWindowTitle("Assignments")
        self.setGeometry(300, 150, 850, 400)

        self.show()

    def backClicked(self):
        self.delivFunct = DelivererFunctionality.DelivererFunctWindow(self.username)
        self.delivFunct.show()
        self.close()

        self.connection.close()

    def viewDetsClicked(self):
        index = self.qButtonGroup.checkedId()

        if index == -1:
            return

        else:
            order_id = self.getOrderIDs()[index]
            store_name = self.getStoreName(order_id)
            time_placed = self.getOrderTime(order_id)
            deliver_time = self.getDeliverTime(order_id)

            self.viewDetsWindow = AssignmentDetails(self.username, order_id, store_name, time_placed, deliver_time)
            self.viewDetsWindow.show()
            self.close()

            self.connection.close()


    def populate(self) -> QTableWidget:
        table = QTableWidget()
        table.setColumnCount(8)
        table.setRowCount(self.getRowCount())
        table.setHorizontalHeaderLabels(["Select", "Store Name", "Order ID", "Date", "Time Order Made", "Time of Delivery", "Order Price", "Num Items"])

        order_IDs = self.getOrderIDs()

        for i in range(self.getRowCount()):
            radioBtn = QRadioButton()
            self.qButtonGroup.addButton(radioBtn, i)
            table.setCellWidget(i, 0, radioBtn)

            for j in range(7):

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
                    orderTime = QTableWidgetItem(self.getOrderTime(order_IDs[i]))
                    orderTime.setTextAlignment(Qt.AlignCenter)
                    orderTime.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 4, orderTime)

                if j == 4:
                    deliverTime = QTableWidgetItem(self.getDeliverTime(order_IDs[i]))
                    deliverTime.setTextAlignment(Qt.AlignCenter)
                    deliverTime.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 5, deliverTime)

                if j == 5:
                    total = QTableWidgetItem(str(self.getOrderTotal(order_IDs[i])))
                    total.setTextAlignment(Qt.AlignCenter)
                    total.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 6, total)

                if j == 6:
                    numItems = QTableWidgetItem(str(self.getNumItems(order_IDs[i])))
                    numItems.setTextAlignment(Qt.AlignCenter)
                    numItems.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 7, numItems)

        return table

    def getRowCount(self):
        return len(self.getOrderIDs())

    def getOrderIDs(self):
        cursor = self.connection.cursor()

        select = ('SELECT order_id FROM DELIVEREDBY WHERE is_delivered=0 and deliverer_username="{}";'.format(self.username))
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

        select = ('SELECT STORE_NAME FROM GROCERYSTORE, ORDERFROM WHERE store_address_id=store_id and order_id={};'.format(order_id))
        cursor.execute(select)

        return cursor.fetchone()[0]

    def getDate(self, order_id):
        cursor = self.connection.cursor()

        select = ('SELECT order_placed_date FROM ORDERR WHERE order_id={};'.format(order_id))
        cursor.execute(select)

        found = cursor.fetchone()[0]

        if found is None:
            return "NONE"

        return found

    def getOrderTime(self, order_id):
        cursor = self.connection.cursor()

        select = ('SELECT order_placed_time FROM ORDERR WHERE order_id={};'.format(order_id))
        cursor.execute(select)

        return cursor.fetchone()[0]

    def getDeliverTime(self, order_id):
        cursor = self.connection.cursor()

        select = ('SELECT delivery_time FROM DELIVEREDBY WHERE order_id={};'.format(order_id))
        cursor.execute(select)

        found = cursor.fetchone()[0]

        if found is None:
            return "NONE"

        return cursor.fetchone()[0]

    def getOrderTotal(self, order_id):
        cursor = self.connection.cursor()

        select = ('SELECT SUM(SELECTITEM.quantity * listed_price) FROM SELECTITEM, ITEM WHERE ITEM.item_id=SELECTITEM.item_id and order_id={};'.format(order_id))
        cursor.execute(select)

        return cursor.fetchone()[0]

    def getNumItems(self, order_id):
        cursor = self.connection.cursor()

        select = ('SELECT SUM(SELECTITEM.quantity) FROM SELECTITEM, ITEM WHERE ITEM.item_id=SELECTITEM.item_id and order_id={};'.format(order_id))
        cursor.execute(select)

        return cursor.fetchone()[0]


class AssignmentDetails(QWidget):

    def __init__(self, username, order_id, store_name, time_placed, deliver_time):
        super(AssignmentDetails, self).__init__()

        self.username = username
        self.order_id = order_id
        self.store_name = store_name
        self.time_placed = time_placed
        self.deliver_time = deliver_time

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password="kwrohde",
                                          db="grocerytech",
                                          charset="utf8mb4")

        self.initUI()

    def initUI(self):

        root = QHBoxLayout()
        top = self.buildTop()
        bottom = self.buildBottom()

        root.addLayout(top)
        root.addLayout(bottom)

        self.setLayout(root)
        self.setWindowTitle("Assignment Details")
        self.setGeometry(250, 150, 850, 400)

    def buildTop(self) -> QVBoxLayout:
        root = QVBoxLayout()
        top = QGridLayout()
        bottom = QHBoxLayout()

        order_placed = QLabel("Order Placed")
        deliver_time = QLabel("Delivery Time")
        self.status = QLabel("Status")
        buyer_address = QLabel("Buyer Address")
        store_name = QLabel("Store Name")

        order_placedEdit = QLineEdit()
        deliver_timeEdit = QLineEdit()
        self.statusEdit = QComboBox()
        buyer_addressEdit = QLineEdit()
        buyer_addressEdit.setMinimumWidth(250)
        store_nameEdit = QLineEdit()

        order_placedEdit.setReadOnly(True)
        deliver_timeEdit.setReadOnly(True)
        buyer_addressEdit.setReadOnly(True)
        store_nameEdit.setReadOnly(True)

        self.statusEdit.addItem("Pending")
        self.statusEdit.addItem("Delivered")

        order_placedEdit.setText(self.time_placed)
        deliver_timeEdit.setText(self.deliver_time)
        buyer_addressEdit.setText(self.getBuyerAddress(self.getBuyerUsername()))
        store_nameEdit.setText(self.store_name)

        top.addWidget(order_placed, 1, 1)
        top.addWidget(order_placedEdit, 1, 2)
        top.addWidget(deliver_time, 1, 3)
        top.addWidget(deliver_timeEdit, 1, 4)
        top.addWidget(self.status, 2, 1)
        top.addWidget(self.statusEdit, 2, 2)
        top.addWidget(store_name, 2, 3)
        top.addWidget(store_nameEdit, 2, 4)
        bottom.addWidget(buyer_address)
        bottom.addWidget(buyer_addressEdit)

        root.addLayout(top)
        root.addLayout(bottom)

        return root

    def buildBottom(self) -> QVBoxLayout:
        root = QVBoxLayout()
        bottom = QHBoxLayout()

        table = QTableWidget()

        table.setColumnCount(2)
        table.setRowCount(len(self.getItemIDs()))
        table.setHorizontalHeaderLabels(["Item Name", "Quantity"])

        item_IDs = self.getItemIDs()

        for i in range(len(self.getItemIDs())):

            for j in range(2):

                if j == 0:
                    item_name = QTableWidgetItem(self.getItemName(item_IDs[i]))
                    item_name.setTextAlignment(Qt.AlignCenter)
                    item_name.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 0, item_name)

                if j == 1:
                    quantity = QTableWidgetItem(str(self.getQuantity(item_IDs[i])))
                    quantity.setTextAlignment(Qt.AlignCenter)
                    quantity.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    table.setItem(i, 1, quantity)

        root.addWidget(table)

        back = QPushButton("Back")
        update = QPushButton("Update Status")

        bottom.addWidget(back)
        bottom.addWidget(update)

        back.clicked.connect(self.backClicked)
        update.clicked.connect(self.updateClicked)

        root.addLayout(bottom)

        return root


    def backClicked(self):
        self.assign = Assignments(self.username)
        self.assign.show()
        self.close()

        self.connection.close()

    def updateClicked(self):
        current_status = self.statusEdit.currentText()
        cursor = self.connection.cursor()

        if current_status == "Pending":
            update = ('UPDATE DELIVEREDBY SET is_delivered=0 WHERE order_id={};'.format(self.order_id))
        else:
            update = ('UPDATE DELIVEREDBY SET is_delivered=1 WHERE order_id={};'.format(self.order_id))

        cursor.execute(update)
        self.connection.commit()

        self.connection.close()

        self.updateSuccess = UpdateSuccessful(self.username, self.order_id, self.store_name, self.time_placed, self.deliver_time)
        self.updateSuccess.show()
        self.close()


    def getBuyerAddress(self, buyer_username):
        cursor1 = self.connection.cursor()
        cursor2 = self.connection.cursor()

        select1 = ('SELECT house_number FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and username="{}";'.format(buyer_username))
        cursor1.execute(select1)
        house_number = cursor1.fetchone()
        house_number = str(house_number[0])

        select2 = ('SELECT street FROM ADDRESS, BUYER WHERE ADDRESS.id=BUYER.address_id and username="{}";'.format(buyer_username))
        cursor2.execute(select2)
        street = cursor2.fetchone()
        street = street[0]

        return (house_number + " " + street)

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

    def getQuantity(self, item_id):
        cursor = self.connection.cursor()

        select = ('SELECT quantity FROM SELECTITEM WHERE item_id={} and order_id={};'.format(item_id, self.order_id))
        cursor.execute(select)

        return cursor.fetchone()[0]

    def getBuyerUsername(self):
        cursor = self.connection.cursor()

        select = ('SELECT buyer_username FROM ORDEREDBY WHERE order_id={};'.format(self.order_id))
        cursor.execute(select)

        return cursor.fetchone()[0]

class UpdateSuccessful(QWidget):

    def __init__(self, username, order_id, store_name, time_placed, deliver_time):
        super(UpdateSuccessful, self).__init__()

        self.username = username
        self.order_id = order_id
        self.store_name = store_name
        self.time_place = time_placed
        self.deliver_time = deliver_time

        self.initUI()

    def initUI(self):

        root = QVBoxLayout()
        msg = QHBoxLayout()
        btns = QGridLayout()

        self.message = QLabel("THE DELIVERY STATUS HAS BEEN UPDATED.")
        msg.addWidget(self.message)

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.okClicked)

        btns.addWidget(self.okBtn, 1, 4)

        root.addLayout(msg)
        root.addLayout(btns)
        self.setLayout(root)
        self.setGeometry(500, 250, 150, 150)
        self.setWindowTitle("Account Updated")
        self.show()

    def okClicked(self):
        self.assignDet = AssignmentDetails(self.username, self.order_id, self.store_name, self.time_place, self.deliver_time)
        self.assignDet.show()
        self.close()



