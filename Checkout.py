import pymysql

from GROCERYTECH_final import BuyerFunctionality
from GROCERYTECH_final import Cart

from PyQt5.QtWidgets import *

from datetime import datetime

class Checkout(QWidget):

    def __init__(self, username, store_id, order_id):
        super(Checkout, self).__init__()

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

        root = QVBoxLayout()
        middle = QGridLayout()
        bottom = QHBoxLayout()
        delivery = QHBoxLayout()

        self.payment = QLabel("Payment")
        self.deliv_time = QLabel("Delivery Time (in hours)")
        self.total_price = QLabel("Total Price ($)")
        self.deliv_instructions = QLabel("Delivery Instructions")

        self.paymentCB = QComboBox()
        self.deliv_timeCB = QComboBox()
        self.total_priceEdit = QLineEdit()
        self.deliv_instructionsEdit = QLineEdit()

        self.deliv_instructions.setMaximumWidth(200)
        self.deliv_instructionsEdit.setMinimumWidth(300)
        self.total_priceEdit.setReadOnly(True)

        self.setPaymentNames()
        self.setDelivTimes()

        self.total_priceEdit.setText(self.getTotalPrice(self.store_id))

        self.back = QPushButton("Back")
        self.finalize = QPushButton("Finalize")

        self.back.clicked.connect(self.backClicked)
        self.finalize.clicked.connect(self.finalizeClicked)

        middle.addWidget(self.payment, 1, 1)
        middle.addWidget(self.paymentCB, 1, 2)
        middle.addWidget(self.deliv_time, 1, 3)
        middle.addWidget(self.deliv_timeCB, 1, 4)
        middle.addWidget(self.total_price, 2, 3)
        middle.addWidget(self.total_priceEdit, 2, 4)

        root.addLayout(middle)

        delivery.addWidget(self.deliv_instructions)
        delivery.addWidget(self.deliv_instructionsEdit)

        bottom.addWidget(self.back)
        bottom.addWidget(self.finalize)

        root.addLayout(delivery)
        root.addLayout(bottom)

        self.setLayout(root)
        self.setWindowTitle("Checkout")
        self.setGeometry(300, 150, 400, 200)

        self.show()

    def backClicked(self):
        self.cart = Cart.Cart(self.username, self.store_id, self.order_id)
        self.cart.show()
        self.close()

        self.connection.close()

    def finalizeClicked(self):
        cursor = self.connection.cursor()

        delivery_time = self.deliv_timeCB.currentText()
        order_placed_date = datetime.now().strftime("%Y-%m-%d")
        order_placed_time = datetime.now().time().__str__()

        delivery_instructions = self.deliv_instructionsEdit.text()
        if delivery_instructions == "":
            delivery_instructions = None

        orderr = ('UPDATE ORDERR WHERE order_id={} SET delivery_instructions="{}", delivery_time="{}", order_placed_date="{}", order_placed_time="{}";'.format(self.order_id, delivery_instructions, delivery_time, order_placed_date, order_placed_time))
        cursor.execute(orderr)
        self.connection.commit()

        self.buyerFunct = BuyerFunctionality.BuyerFunctWindow(self.username)
        self.buyerFunct.show()
        self.close()

        self.connection.close()

    def setPaymentNames(self):
        cursor = self.connection.cursor()

        select = ('SELECT payment_name FROM PAYMENTS WHERE username="{}";'.format(self.username))
        cursor.execute(select)
        found = cursor.fetchall()

        for name in found:
            self.paymentCB.addItem(name[0])

    def setDelivTimes(self):
        self.deliv_timeCB.addItem("ASAP")
        self.deliv_timeCB.addItem("1")
        self.deliv_timeCB.addItem("2")
        self.deliv_timeCB.addItem("5")
        self.deliv_timeCB.addItem("10")
        self.deliv_timeCB.addItem("12")
        self.deliv_timeCB.addItem("24")

    def getTotalPrice(self, order_id):
        cursor = self.connection.cursor()

        select = ('SELECT (SUM(listed_price * SELECTITEM.quantity)) FROM SELECTITEM, ITEM, ORDERR WHERE SELECTITEM.order_id=ORDERR.order_id and SELECTITEM.item_id=ITEM.item_id and ORDERR.order_id={};'.format(order_id))
        cursor.execute(select)
        return str(cursor.fetchone()[0])