import sys
import sqlite3
import addproduct, addmember
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
        self.displayProduct()
        self.displayMembers()


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
        self.addMember.triggered.connect(self.funAddMember)
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
        self.productTable.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)#to resize the product name and manufacturer columns
        self.productTable.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        self.productTable.doubleClicked.connect(self.selectedProduct)

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
        self.memberTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.memberTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        ###################Right widget###################
        self.memberSearchText = QLabel("Search Members")
        self.memberSearchEntry = QLineEdit()
        self.memberSearchButton = QPushButton("Search")

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

    def funAddMember(self):
        self.newMember = addmember.AddMember()

    def displayProduct(self):
        self.productTable.setFont(QFont("Times",12))
        print("display products")
        print(self.productTable.rowCount())
        # we need to remove or clean our table widgets first
        for i in reversed(range(self.productTable.rowCount())):
            print("i:",i)
            self.productTable.removeRow(i)
        query = cur.execute("SELECT product_id,product_name,product_manufacturer,product_price,product_qouta, product_availability FROM products")
        for row_data in query:#0,1,2
            print(row_data) # first row :(1, 'Playstation', 'Sony', 300, 50, 'Available'),second :(2, 'computer', 'HP', 1200, 21, 'Available'),third: (3, 'S9', 'Samsung', 400, 33, 'Available')
            row_number = self.productTable.rowCount()
            print(row_number)#0,1,2
            self.productTable.insertRow(row_number)#inserting row zero,row 1 , row 2
            #exemple if there is 3 rows in the query
            #the first time i insert an empty row in the table, then i fill it with info from the query
            for column_number, data in enumerate(row_data): #column number is how many element in the row_data list
                self.productTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        self.productTable.setEditTriggers(QAbstractItemView.NoEditTriggers)#this line will prevent someone from changing the table product
    
    def displayMembers(self):
        self.memberTable.setFont(QFont("Times", 12))
        for i in reversed(range(self.memberTable.rowCount())):
            self.memberTable.removeRow(i)
        query=con.execute("SELECT member_id,member_name,member_surname,member_phone FROM members")
        for row_number,row_data in enumerate(query):
            print(row_data)
            print("Row",row_number) #another methode
            self.memberTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.memberTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        self.memberTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def selectedProduct(self):
        global productId #so we could use it the id in another class
        listProduct=[]
        for i in range(0,6):#we have 6 feildes (prodct ud, prod name...)
            listProduct.append(self.productTable.item(self.productTable.currentRow(),i).text())
            #result(listproduct values each lap) of this for loop:
            #['1']
            #['1', 'Playstation']
            #['1', 'Playstation', 'Sony']
            #['1', 'Playstation', 'Sony', '300']
            #['1', 'Playstation', 'Sony', '300', '50']
            #['1', 'Playstation', 'Sony', '300', '50', 'Available']
        productId=listProduct[0]# first elment is the id that we gonna use it after
        self.display=DisplayProduct()



    ###################################################################################
    ###################New Class for displaying each product spec######################
    ###################################################################################
class DisplayProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Details")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(450,150,350,600)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.productDetails()
        self.widgets()
        self.layouts()


    ####################FETCHINF DATA using product ID of the chosen product################
    def productDetails(self):
        global productId
        query=("SELECT * FROM products WHERE product_id=?")
        productDetails=cur.execute(query,(productId,)).fetchone()
        print(productDetails)#(1, 'Playstation', 'Sony', 300, 50, '71PGvPXpk5L._AC_.jpg', 'Available')
        self.productName=productDetails[1]
        self.productManufacturer=productDetails[2]
        self.productPrice=productDetails[3]
        self.productQouta=productDetails[4]
        self.productImg=productDetails[5]
        self.productAvailability=productDetails[6]


    def widgets(self):
        ########################adding top widgets########################
        self.product_Img=QLabel()
        self.product_Img.setPixmap( QPixmap("img/{}".format(self.productImg)))
        self.product_Img.setAlignment(Qt.AlignCenter)
        self.productText=QLabel("Update Product")
        self.productText.setAlignment(Qt.AlignCenter)
        ########################adding bottom widgets####################
        self.nameEntry=QLineEdit()
        self.nameEntry.setText(self.productName)
        self.manufacturerEntry = QLineEdit()
        self.manufacturerEntry.setText(self.productManufacturer)
        self.priceEntry = QLineEdit()
        self.priceEntry.setText(str(self.productPrice))
        self.qoutaEntry = QLineEdit()
        self.qoutaEntry.setText(str(self.productQouta))
        self.availabilityComboBox=QComboBox()
        self.availabilityComboBox.addItems(["Available","Unavailable"])
        self.uploadBtn=QPushButton("Upload")
        self.deleteBtn=QPushButton("Delete")
        self.updateBtn=QPushButton("Update")


    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QVBoxLayout()
        self.bottomLayout=QFormLayout()
        self.topFrame=QFrame()
        self.bottomFrame=QFrame()
        ####################adding top widgets ##############
        self.topLayout.addWidget(self.productText)
        self.topLayout.addWidget(self.product_Img)
        ####################adding bottom widgets ##############
        self.bottomLayout.addRow(QLabel("Name: "),self.nameEntry)
        self.bottomLayout.addRow(QLabel("Manufacturer: "),self.manufacturerEntry)
        self.bottomLayout.addRow(QLabel("Price: "),self.priceEntry)
        self.bottomLayout.addRow(QLabel("Qouta: "),self.qoutaEntry)
        self.bottomLayout.addRow(QLabel("Status: "),self.availabilityComboBox)
        self.bottomLayout.addRow(QLabel("Image: "),self.uploadBtn)
        self.bottomLayout.addRow(QLabel(""),self.deleteBtn)
        self.bottomLayout.addRow(QLabel(""),self.updateBtn)

        ####################setting main Layout#####################
        self.topFrame.setLayout(self.topLayout)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

###########################################################MAIN######################################
def main():
    App = QApplication(sys.argv)
    # App.setWindowIcon(QIcon("icons/icon.ico")) we con put an icon to the window in this way too
    window = Main()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
