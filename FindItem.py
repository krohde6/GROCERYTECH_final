from GROCERYTECH_final import StoreHomepage
from GROCERYTECH_final import Beverages
from GROCERYTECH_final import Dairy
from GROCERYTECH_final import Produce
from GROCERYTECH_final import BakingGoods
from GROCERYTECH_final import FrozenGoods
from GROCERYTECH_final import Others
from GROCERYTECH_final import CannedGoods
from GROCERYTECH_final import Meat
from GROCERYTECH_final import CleaningProducts
from GROCERYTECH_final import PersonalCare
from GROCERYTECH_final import Checkout
from PyQt5.QtWidgets import *


class FindItem(QWidget):

    def __init__(self, username, store_id, order_id):
        super(FindItem, self).__init__()

        self.username = username
        self.store_id = store_id
        self.order_id = order_id

        self.initUI()

    def initUI(self):

        root = QGridLayout()

        self.beverages = QPushButton("Beverages")
        self.dairy = QPushButton("Dairy")
        self.produce = QPushButton("Produce")
        self.bakingGoods = QPushButton("Baking Goods")
        self.frozenGoods = QPushButton("Frozen Goods")
        self.others = QPushButton("Others")
        self.cannedGoods = QPushButton("Canned Goods")
        self.meat = QPushButton("Meat")
        self.cleaningProducts = QPushButton("Cleaning Products")
        self.personalCare = QPushButton("Personal Care")
        self.checkout = QPushButton("Checkout")
        self.back = QPushButton("Back")

        self.beverages.clicked.connect(self.beveragesClicked)
        self.dairy.clicked.connect(self.dairyClicked)
        self.produce.clicked.connect(self.produceClicked)
        self.bakingGoods.clicked.connect(self.bakingGoodsClicked)
        self.frozenGoods.clicked.connect(self.frozenFoodsClicked)
        self.others.clicked.connect(self.othersClicked)
        self.cannedGoods.clicked.connect(self.cannedGoodsClicked)
        self.meat.clicked.connect(self.meatClicked)
        self.cleaningProducts.clicked.connect(self.cleaningProductsClicked)
        self.personalCare.clicked.connect(self.personalCareClicked)
        self.checkout.clicked.connect(self.checkoutClicked)
        self.back.clicked.connect(self.backClicked)

        root.addWidget(self.beverages, 1, 1)
        root.addWidget(self.dairy, 1, 2)
        root.addWidget(self.produce, 1, 3)
        root.addWidget(self.bakingGoods, 2, 1)
        root.addWidget(self.frozenGoods, 2, 2)
        root.addWidget(self.others, 2, 3)
        root.addWidget(self.cannedGoods, 3, 1)
        root.addWidget(self.meat, 3, 2)
        root.addWidget(self.cleaningProducts, 4, 1)
        root.addWidget(self.personalCare, 4, 2)
        root.addWidget(self.checkout, 1, 4)
        root.addWidget(self.back, 5, 4)

        self.setLayout(root)
        self.setWindowTitle("Find Item")
        self.setGeometry(450, 150, 500, 200)

        self.show()

    def backClicked(self):
        self.StoreHomepage = StoreHomepage.StoreHomepage(self.username, self.store_id, self.order_id)
        self.StoreHomepage.show()
        self.close()

    def checkoutClicked(self):
        self.checkoutWin = Checkout.Checkout(self.username, self.store_id, self.order_id)
        self.checkoutWin.show()
        self.close()


    def beveragesClicked(self):
        self.beveragesWin = Beverages.Beverages(self.username, self.store_id, self.order_id)
        self.beveragesWin.show()
        self.close()

    def dairyClicked(self):
        self.dairyWin = Dairy.Dairy(self.username, self.store_id, self.order_id)
        self.dairyWin.show()
        self.close()

    def produceClicked(self):
        self.produceWin = Produce.Produce(self.username, self.store_id, self.order_id)
        self.produceWin.show()
        self.close()

    def bakingGoodsClicked(self):
        self.bakingGoodsWin = BakingGoods.BakingGoods(self.username, self.store_id, self.order_id)
        self.bakingGoodsWin.show()
        self.close()

    def frozenFoodsClicked(self):
        self.frozenGoodsWin = FrozenGoods.FrozenGoods(self.username, self.store_id, self.order_id)
        self.frozenGoodsWin.show()
        self.close()

    def othersClicked(self):
        self.othersWin = Others.Others(self.username, self.store_id, self.order_id)
        self.othersWin.show()
        self.close()

    def cannedGoodsClicked(self):
        self.cannedGoodsWin = CannedGoods.CannedGoods(self.username, self.store_id, self.order_id)
        self.cannedGoodsWin.show()
        self.close()

    def meatClicked(self):
        self.meatWin = Meat.Meat(self.username, self.store_id, self.order_id)
        self.meatWin.show()
        self.close()

    def cleaningProductsClicked(self):
        self.cleaningProductsWin = CleaningProducts.CleaningProducts(self.username, self.store_id, self.order_id)
        self.cleaningProductsWin.show()
        self.close()

    def personalCareClicked(self):
        self.personalCareWin = PersonalCare.PersonalCare(self.username, self.store_id, self.order_id)
        self.personalCareWin.show()
        self.close()



