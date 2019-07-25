import pymysql

from GROCERYTECH_final import StoreList
from GROCERYTECH_final import BuyerFunctionality
from GROCERYTECH_final import Cart
from GROCERYTECH_final import FindItem

from PyQt5.QtWidgets import *

class StoreHomepage(QWidget):

    def __init__(self, username, store_id, order_id):
        super(StoreHomepage, self).__init__()

        self.username = username
        self.store_id = store_id
        self.order_id = order_id

        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password=None,
                                          db="grocerytech",
                                          charset="utf8mb4")

        self.initUI()

    def initUI(self):

        root = QGridLayout()

        self.findItem = QPushButton("Find Item")
        self.viewCart = QPushButton("View Cart")
        self.cancelOrder = QPushButton("Cancel Order")
        self.back = QPushButton("Back")
        self.buffer = QLabel()
        self.buffer1 = QLabel()
        self.buffer2 = QLabel()
        self.buffer3 = QLabel()

        self.findItem.clicked.connect(self.findItemClicked)
        self.viewCart.clicked.connect(self.viewCartClicked)
        self.cancelOrder.clicked.connect(self.cancelOrderClicked)
        self.back.clicked.connect(self.backClicked)

        root.addWidget(self.buffer, 1, 1)
        root.addWidget(self.findItem, 1, 2)
        root.addWidget(self.viewCart, 1, 3)
        root.addWidget(self.buffer1, 1, 4)
        root.addWidget(self.buffer2, 2, 1)
        root.addWidget(self.back, 2, 2)
        root.addWidget(self.cancelOrder, 2, 3)
        root.addWidget(self.buffer3, 2, 4)

        self.setLayout(root)
        self.setWindowTitle("Store Homepage")
        self.setGeometry(500, 200, 300, 250)
        self.show()

    # Open window that shows list of item types
    def findItemClicked(self):
        self.findItemWindow = FindItem.FindItem(self.username, self.store_id, self.order_id)
        self.findItemWindow.show()
        self.close()

        self.connection.close()

    def viewCartClicked(self):
        self.viewCartWindow = Cart.Cart(self.username, self.store_id, self.order_id)
        self.viewCartWindow.show()
        self.close()

        self.connection.close()

    def cancelOrderClicked(self):
        self.deleteOrderr(self.order_id)

        self.buyerFunct = BuyerFunctionality.BuyerFunctWindow(self.username)
        self.buyerFunct.show()
        self.close()

        self.connection.close()

    def backClicked(self):
        self.storeList = StoreList.StoreList(self.username)
        self.storeList.show()
        self.close()

        self.connection.close()

    def deleteOrderr(self, order_id):
        cursor = self.connection.cursor()

        delete = ('DELETE FROM ORDERR WHERE order_id={}'.format(order_id))
        cursor.execute(delete)
        self.connection.commit()





