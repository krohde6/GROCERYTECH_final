import pymysql

from random import randint

from GROCERYTECH_final import BuyerFunctionality
from GROCERYTECH_final import StoreHomepage

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class StoreList(QWidget):

    def __init__(self, username):
        super(StoreList, self).__init__()

        self.username = username

        self.qButtonGroup = QButtonGroup()

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password=None,
                                          db="grocerytech",
                                          charset="utf8mb4")

        self.initUI()

    def initUI(self):

        self.root = QVBoxLayout()
        bottom = QHBoxLayout()

        self.tableWidget = self.populate()

        self.back = QPushButton("Back")
        self.choose = QPushButton("Choose")

        bottom.addWidget(self.back)
        bottom.addWidget(self.choose)

        self.back.clicked.connect(self.backClicked)
        self.choose.clicked.connect(self.chooseClicked)

        self.root.addWidget(self.tableWidget)
        self.root.addLayout(bottom)
        self.setLayout(self.root)
        self.setWindowTitle("List of Stores")
        self.setGeometry(300, 150, 850, 1000)
        self.show()

    def backClicked(self):
        self.buyerFunct = BuyerFunctionality.BuyerFunctWindow(self.username)
        self.buyerFunct.show()
        self.close()

        self.connection.close()

    def chooseClicked(self):
        index = self.qButtonGroup.checkedId()

        if index == -1:
            self.noStore = NoStoreSelected(self.username)
            self.noStore.show()
            self.close()

        else:
            store_name = self.store[index][0][0]
            store_phone = self.store[index][2][0]

            store_id = self.getStoreID(store_name, store_phone)
            order_id = self.getNewOrderID()

            self.newOrderedBy(order_id, self.username)
            self.newOrderFrom(store_id, order_id)
            self.newDeliveredBy(order_id)

            self.storeHomepage = StoreHomepage.StoreHomepage(self.username, store_id, order_id)
            self.storeHomepage.show()
            self.close()

        self.connection.close()

    def populate(self) -> QTableWidget:
        table = QTableWidget()
        table.setColumnCount(6)
        table.setRowCount(35)
        table.setColumnWidth(0, 50)
        table.setColumnWidth(1, 100)
        table.setColumnWidth(2, 350)
        table.setColumnWidth(3, 100)
        table.setColumnWidth(4, 80)
        table.setColumnWidth(5, 80)
        table.setHorizontalHeaderLabels(["Select", "Store Name", "Address", "Phone", "Opening Time", "Closing Time"])

        self.store1 = [self.getStoreName(25), self.getStoreAddress(25), self.getStorePhone(25), self.getOpeningTime(25), self.getClosingTime(25)]
        self.store2 = [self.getStoreName(24), self.getStoreAddress(24), self.getStorePhone(24), self.getOpeningTime(24), self.getClosingTime(24)]
        self.store3 = [self.getStoreName(23), self.getStoreAddress(23), self.getStorePhone(23), self.getOpeningTime(23), self.getClosingTime(23)]
        self.store4 = [self.getStoreName(33), self.getStoreAddress(33), self.getStorePhone(33), self.getOpeningTime(33), self.getClosingTime(33)]
        self.store5 = [self.getStoreName(32), self.getStoreAddress(32), self.getStorePhone(32), self.getOpeningTime(32), self.getClosingTime(32)]
        self.store6 = [self.getStoreName(31), self.getStoreAddress(31), self.getStorePhone(31), self.getOpeningTime(31), self.getClosingTime(31)]
        self.store7 = [self.getStoreName(8), self.getStoreAddress(8), self.getStorePhone(8), self.getOpeningTime(8), self.getClosingTime(8)]
        self.store8 = [self.getStoreName(9), self.getStoreAddress(9), self.getStorePhone(9), self.getOpeningTime(9), self.getClosingTime(9)]
        self.store9 = [self.getStoreName(10), self.getStoreAddress(10), self.getStorePhone(10), self.getOpeningTime(10), self.getClosingTime(10)]
        self.store10 = [self.getStoreName(11), self.getStoreAddress(11), self.getStorePhone(11), self.getOpeningTime(11), self.getClosingTime(11)]
        self.store11 = [self.getStoreName(12), self.getStoreAddress(12), self.getStorePhone(12), self.getOpeningTime(12), self.getClosingTime(12)]
        self.store12 = [self.getStoreName(13), self.getStoreAddress(13), self.getStorePhone(13), self.getOpeningTime(13), self.getClosingTime(13)]
        self.store13 = [self.getStoreName(18), self.getStoreAddress(18), self.getStorePhone(18), self.getOpeningTime(18), self.getClosingTime(18)]
        self.store14 = [self.getStoreName(1), self.getStoreAddress(1), self.getStorePhone(1), self.getOpeningTime(1), self.getClosingTime(1)]
        self.store15 = [self.getStoreName(7), self.getStoreAddress(7), self.getStorePhone(7), self.getOpeningTime(7), self.getClosingTime(7)]
        self.store16 = [self.getStoreName(6), self.getStoreAddress(6), self.getStorePhone(6), self.getOpeningTime(6), self.getClosingTime(6)]
        self.store17 = [self.getStoreName(5), self.getStoreAddress(5), self.getStorePhone(5), self.getOpeningTime(5), self.getClosingTime(5)]
        self.store18 = [self.getStoreName(4), self.getStoreAddress(4), self.getStorePhone(4), self.getOpeningTime(4), self.getClosingTime(4)]
        self.store19 = [self.getStoreName(3), self.getStoreAddress(3), self.getStorePhone(3), self.getOpeningTime(3), self.getClosingTime(3)]
        self.store20 = [self.getStoreName(2), self.getStoreAddress(2), self.getStorePhone(2), self.getOpeningTime(2), self.getClosingTime(2)]
        self.store21 = [self.getStoreName(27), self.getStoreAddress(27), self.getStorePhone(27), self.getOpeningTime(27), self.getClosingTime(27)]
        self.store22 = [self.getStoreName(28), self.getStoreAddress(28), self.getStorePhone(28), self.getOpeningTime(28), self.getClosingTime(28)]
        self.store23 = [self.getStoreName(29), self.getStoreAddress(29), self.getStorePhone(29), self.getOpeningTime(29), self.getClosingTime(29)]
        self.store24 = [self.getStoreName(30), self.getStoreAddress(30), self.getStorePhone(30), self.getOpeningTime(30), self.getClosingTime(30)]
        self.store25 = [self.getStoreName(16), self.getStoreAddress(16), self.getStorePhone(16), self.getOpeningTime(16), self.getClosingTime(16)]
        self.store26 = [self.getStoreName(17), self.getStoreAddress(17), self.getStorePhone(17), self.getOpeningTime(17), self.getClosingTime(17)]
        self.store27 = [self.getStoreName(21), self.getStoreAddress(21), self.getStorePhone(21), self.getOpeningTime(21), self.getClosingTime(21)]
        self.store28 = [self.getStoreName(22), self.getStoreAddress(22), self.getStorePhone(22), self.getOpeningTime(22), self.getClosingTime(22)]
        self.store29 = [self.getStoreName(34), self.getStoreAddress(34), self.getStorePhone(34), self.getOpeningTime(34), self.getClosingTime(34)]
        self.store30 = [self.getStoreName(35), self.getStoreAddress(35), self.getStorePhone(35), self.getOpeningTime(35), self.getClosingTime(35)]
        self.store31 = [self.getStoreName(19), self.getStoreAddress(19), self.getStorePhone(19), self.getOpeningTime(19), self.getClosingTime(19)]
        self.store32 = [self.getStoreName(20), self.getStoreAddress(20), self.getStorePhone(20), self.getOpeningTime(20), self.getClosingTime(20)]
        self.store33 = [self.getStoreName(15), self.getStoreAddress(15), self.getStorePhone(15), self.getOpeningTime(15), self.getClosingTime(15)]
        self.store34 = [self.getStoreName(14), self.getStoreAddress(14), self.getStorePhone(14), self.getOpeningTime(14), self.getClosingTime(14)]
        self.store35 = [self.getStoreName(26), self.getStoreAddress(26), self.getStorePhone(26), self.getOpeningTime(26), self.getClosingTime(26)]

        self.store = [self.store1, self.store2, self.store3, self.store4, self.store5, self.store6, self.store7, self.store8, self.store9, self.store10, self.store11, self.store12, self.store13, self.store14, self.store15, self.store16, self.store17, self.store18, self.store19, self.store20, self.store21, self.store22, self.store23, self.store24, self.store25, self.store26, self.store27, self.store28, self.store29, self.store30, self.store31, self.store32, self.store33, self.store34, self.store35]

        for i in range(35):
            radioBtn = QRadioButton()
            self.qButtonGroup.addButton(radioBtn, i)
            table.setCellWidget(i, 0, radioBtn)

            for j in range(5):
                element = QTableWidgetItem(self.store[i][j][0])
                element.setTextAlignment(Qt.AlignCenter)
                element.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                table.setItem(i, j+1, element)

        return table

    def getStoreAddress(self, store_id):
        cursor = self.connection.cursor()

        select = ('SELECT house_number, street, city, state, zip_code FROM GROCERYSTORE, ADDRESS WHERE address_id=id and store_id={};'.format(store_id))
        cursor.execute(select)
        store = cursor.fetchone()
        address = (str(store[0]) + " " + store[1] + ", " + store[2] + ", " + store[3] + " " + str(store[4]))

        return (address,)

    def getStoreName(self, store_id):
        cursor = self.connection.cursor()
        select = ('SELECT store_name FROM GROCERYSTORE WHERE store_id={};'.format(store_id))
        cursor.execute(select)
        return cursor.fetchone()

    def getStorePhone(self, store_id):
        cursor = self.connection.cursor()
        select = ('SELECT phone FROM GROCERYSTORE WHERE store_id={};'.format(store_id))
        cursor.execute(select)
        return cursor.fetchone()

    def getOpeningTime(self, store_id):
        cursor = self.connection.cursor()
        select = ('SELECT opening_time FROM GROCERYSTORE WHERE store_id={};'.format(store_id))
        cursor.execute(select)
        time_tuple = cursor.fetchone()
        time_str = str(time_tuple[0])
        return (time_str,)

    def getClosingTime(self, store_id):
        cursor = self.connection.cursor()
        select = ('SELECT closing_time FROM GROCERYSTORE WHERE store_id={};'.format(store_id))
        cursor.execute(select)
        time_tuple = cursor.fetchone()
        time_str = str(time_tuple[0])
        return (time_str,)

    def getStoreID(self, store_name, store_phone):
        cursor = self.connection.cursor()
        select = ('SELECT store_id FROM GROCERYSTORE WHERE store_name="{}" and phone="{}";'.format(store_name, str(store_phone)))
        cursor.execute(select)
        return cursor.fetchone()[0]

    def getNewOrderID(self):
        cursor = self.connection.cursor()
        order_id = randint(10000, 99999)

        insert = ('INSERT INTO ORDERR (order_id, delivery_time, order_placed_date, order_placed_time) VALUES ({}, "NONE", "NONE", "NONE");'.format(order_id))
        cursor.execute(insert)
        self.connection.commit()

        return order_id

    def newOrderedBy(self, order_id, buyer_username):
        cursor = self.connection.cursor()

        insert = ('INSERT INTO ORDEREDBY VALUES ({}, "{}");'.format(order_id, buyer_username))
        cursor.execute(insert)
        self.connection.commit()

        return

    def newOrderFrom(self, store_id, order_id):
        cursor = self.connection.cursor()

        insert = ('INSERT INTO ORDERFROM VALUES ({}, {});'.format(store_id, order_id))
        cursor.execute(insert)
        self.connection.commit()

        return

    def newDeliveredBy(self, order_id):
        cursor = self.connection.cursor()
        random_deliverer = self.getRandomDeliverer()

        insert = ('INSERT INTO DELIVEREDBY (order_id, deliverer_username, is_delivered) VALUES ({}, "{}", 0);'.format(order_id, random_deliverer))
        cursor.execute(insert)
        self.connection.commit()

        return

    def getRandomDeliverer(self):
        cursor = self.connection.cursor()

        select = ('select username from userr where user_type="deliverer" order by rand() limit 1;')
        cursor.execute(select)
        return cursor.fetchone()[0]


    def getStoreAddressID(self, store_id):
        cursor = self.connection.cursor()

        select = ('SELECT address_id FROM GROCERYSTORE WHERE store_id={};'.format(store_id))
        cursor.execute(select)

        address_id = cursor.fetchone()[0]

        return address_id


class NoStoreSelected(QMessageBox):

    def __init__(self, username):
        super(NoStoreSelected, self).__init__()

        self.username = username

        self.initUI()

    def initUI(self):
        self.setIcon(QMessageBox.Information)
        self.setText("There was an error")
        self.setInformativeText('You must check a store before continuing.')
        self.setDetailedText('Click a button under the "Select" column.')
        self.setStandardButtons(QMessageBox.Ok)
        self.buttonClicked.connect(self.btnClicked)

        self.show()

    def btnClicked(self):
        self.storeList = StoreList(self.username)
        self.storeList.show()
        self.close()
