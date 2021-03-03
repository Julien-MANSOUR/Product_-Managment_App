import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


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
        self.tabs=QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()
        self.tabs.addTab(self.tab1,"Products")
        self.tabs.addTab(self.tab2,"Members")
        self.tabs.addTab(self.tab3,"Statistics")

    def widgets(self):
        ###################Tab1 Layout###################
        ###################Left Main Layout widget###################
        self.productTable=QTableWidget()
        self.productTable.setColumnCount(6)
        self.productTable.setColumnHidden(0,True)#i want to hide the id column , we just want to use the id , no need to show it
        self.productTable.setHorizontalHeaderItem(0,QTableWidgetItem("Product Id"))
        self.productTable.setHorizontalHeaderItem(1,QTableWidgetItem("Product Name"))
        self.productTable.setHorizontalHeaderItem(2,QTableWidgetItem("Manufacturer"))
        self.productTable.setHorizontalHeaderItem(3,QTableWidgetItem("Price"))
        self.productTable.setHorizontalHeaderItem(4,QTableWidgetItem("Qouta"))
        self.productTable.setHorizontalHeaderItem(5,QTableWidgetItem("Availability"))
        ###################Right Main Layout widget###################
        ###################Right  top Layout widget###################
        self.searchText=QLabel("Search")
        self.searchEntry=QLineEdit()
        self.searchEntry.setPlaceholderText("Search For Products")
        self.searchButton=QPushButton("Search")
        ###################Right  middle Layout widgets###################
        self.allProducts=QRadioButton("All Products")
        self.availableProducts=QRadioButton("Available")
        self.notAvailableProducts=QRadioButton("Not Available")
        self.listButton=QPushButton("List")




    def layouts(self):
        ###################Tab1 Layout###################
        self.mainLayout=QHBoxLayout()
        self.leftMainLayout=QVBoxLayout()
        self.rightMainLayout=QVBoxLayout()
        self.rightTopLayout=QHBoxLayout()
        self.rightMiddleLayout=QHBoxLayout()
        self.topGroupBox=QGroupBox("Search Box")
        self.middleGroupBox=QGroupBox("List Box")
        ###################Add layouts###################
        self.mainLayout.addLayout(self.leftMainLayout,70)
        self.leftMainLayout.addWidget(self.productTable)
        ##################Right Main Layout#####################
        self.mainLayout.addLayout(self.rightMainLayout,30)
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




        self.tab1.setLayout(self.mainLayout)

def main():
    App = QApplication(sys.argv)
    # App.setWindowIcon(QIcon("icons/icon.ico")) we con put an icon to the window in this way too
    window = Main()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
