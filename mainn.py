import sys
import sqlite3
import addproduct
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

#################################################
######Data base#######
#################################################
con = sqlite3.connect("Products.db")
cur = con.cursor()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Manager")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(250, 250, 1000, 500)
        self.setFixedSize(self.size())  # to fix windows size without minimize or maximize it
        self.UI()
        self.show()

    def UI(self):
        self.toolBar()
        self.tabWidget()
        self.widgets()
        self.layouts()

    def toolBar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # so the name we chose could appear under the button
        ##################ToolBar Button###################
        #################Add Product ######################
        self.addProduct = QAction(QIcon("icons/add.png"), "Add Product", self)
        self.tb.addAction(self.addProduct)
        self.addProduct.triggered.connect(self.funcAddProduct)
        self.tb.addSeparator()
        #################Add Member ######################
        self.addMember = QAction(QIcon("icons/users.png"), "Add Member", self)
        self.tb.addAction(self.addMember)
        self.tb.addSeparator()
        #################Sell Product ######################
        self.sellProduct = QAction(QIcon("icons/sell.png"), "Sell Product", self)
        self.tb.addAction(self.sellProduct)
        self.tb.addSeparator()

    def tabWidget(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab1, "Products")
        self.tabs.addTab(self.tab2, "Members")
        self.tabs.addTab(self.tab3, "Statistics")

    def widgets(self):
        #################################################
        ###################Tab1 Widgets###################
        #################################################
        ###################Left Main Layout widget###################
        self.productTable = QTableWidget()
        self.productTable.setColumnCount(6)
        self.productTable.setColumnHidden(0,
                                          True)  # i want to hide the id column , we just want to use the id , no need to show it
        self.productTable.setHorizontalHeaderItem(0, QTableWidgetItem("Product Id"))
        self.productTable.setHorizontalHeaderItem(1, QTableWidgetItem("Product Name"))
        self.productTable.setHorizontalHeaderItem(2, QTableWidgetItem("Manufacturer"))
        self.productTable.setHorizontalHeaderItem(3, QTableWidgetItem("Price"))
        self.productTable.setHorizontalHeaderItem(4, QTableWidgetItem("Qouta"))
        self.productTable.setHorizontalHeaderItem(5, QTableWidgetItem("Availability"))
        ###################Right Main Layout widget###################
        ###################Right  top Layout widget###################
        self.searchText = QLabel("Search")
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("Search For Products")
        self.searchButton = QPushButton("Search")
        ###################Right  middle Layout widgets###################
        self.allProducts = QRadioButton("All Products")
        self.availableProducts = QRadioButton("Available")
        self.notAvailableProducts = QRadioButton("Not Available")
        self.listButton = QPushButton("List")

        #################################################
        ###################Tab2 Widgets###################
        #################################################
        ###################Left  widget###########
        self.memberTable = QTableWidget()
        self.memberTable.setColumnCount(4)
        self.memberTable.setHorizontalHeaderItem(0, QTableWidgetItem("Member ID"))
        self.memberTable.setHorizontalHeaderItem(1, QTableWidgetItem("Member Name"))
        self.memberTable.setHorizontalHeaderItem(2, QTableWidgetItem("Member Surname"))
        self.memberTable.setHorizontalHeaderItem(3, QTableWidgetItem("Member Phone"))
        ###################Right widget###################
        self.memberSearchText = QLabel("Search Members")
        self.memberSearchEntry = QLineEdit()
        self.memberSearchButton = QPushButton("Button")

    def layouts(self):
        #################################################
        ###################Tab1 Layout###################
        #################################################
        self.mainLayout = QHBoxLayout()
        self.leftMainLayout = QVBoxLayout()
        self.rightMainLayout = QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()
        self.rightMiddleLayout = QHBoxLayout()
        self.topGroupBox = QGroupBox("Search Box")
        self.middleGroupBox = QGroupBox("List Box")
        ###################Add layouts###################
        self.mainLayout.addLayout(self.leftMainLayout, 70)
        self.leftMainLayout.addWidget(self.productTable)
        ##################Right Main Layout#####################
        self.mainLayout.addLayout(self.rightMainLayout, 30)
        self.rightMainLayout.addWidget(self.topGroupBox)
        self.rightMainLayout.addWidget(self.middleGroupBox)
        ##########Right top  Layout widgets##############
        self.rightTopLayout.addWidget(self.searchText)
        self.rightTopLayout.addWidget(self.searchEntry)
        self.rightTopLayout.addWidget(self.searchButton)
        self.topGroupBox.setLayout(self.rightTopLayout)
        ##########Right middle  Layout widgets##############
        self.rightMiddleLayout.addWidget(self.allProducts)
        self.rightMiddleLayout.addWidget(self.availableProducts)
        self.rightMiddleLayout.addWidget(self.notAvailableProducts)
        self.rightMiddleLayout.addWidget(self.listButton)
        self.middleGroupBox.setLayout(self.rightMiddleLayout)
        self.tab1.setLayout(self.mainLayout)  # tab1
        ########################################################
        ###################Tab1 Layout##########################
        ########################################################
        self.memberMainLayout = QHBoxLayout()
        self.memberLeftLayout = QVBoxLayout()
        self.memberRightLayout = QHBoxLayout()
        self.memberRightGroupBox = QGroupBox("Search For Members")
        self.memberRightGroupBox.setContentsMargins(5, 5, 5, 300)  # im adding 300 pixels for botumn
        ###################Add layouts###########################
        self.memberMainLayout.addLayout(self.memberLeftLayout, 70)
        self.memberMainLayout.addWidget(self.memberRightGroupBox, 30)
        ###################Add Left widgets###########################
        self.memberLeftLayout.addWidget(self.memberTable)
        ###################Add Right widgets###########################
        self.memberRightLayout.addWidget(self.memberSearchText)
        self.memberRightLayout.addWidget(self.memberSearchEntry)
        self.memberRightLayout.addWidget(self.memberSearchButton)
        self.memberRightGroupBox.setLayout(self.memberRightLayout)
        self.tab2.setLayout(self.memberMainLayout)

        ########################################################
        ###################Action functions######################
        ########################################################
    def funcAddProduct(self):
        self.newProduct = addproduct.AddProduct()  # addproduct is our new python file/ AddProduct is the class


def main():
    App = QApplication(sys.argv)
    # App.setWindowIcon(QIcon("icons/icon.ico")) we con put an icon to the window in this way too
    window = Main()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
