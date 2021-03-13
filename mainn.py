import sys, os
import sqlite3
import addproduct, addmember , sellings , style
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PIL import Image

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
        self.setGeometry(250, 250, 1200, 600)
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
        self.getSatistics()

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
        self.sellProduct.triggered.connect(self.funcSellProduct)
        self.tb.addSeparator()

    def tabWidget(self):
        self.tabs = QTabWidget()
        self.tabs.blockSignals(True)#we use it at first of creating  tabs , and we use another one at the end , to help refreshing our tabs each time we add something
        #because block signals is not enough we can creat another function to recall the displaying functions
        self.tabs.currentChanged.connect(self.tabChanged)
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
        self.productTable.horizontalHeader().setSectionResizeMode(1,
                                                                  QHeaderView.Stretch)  # to resize the product name and manufacturer columns
        self.productTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.productTable.doubleClicked.connect(self.selectedProduct)

        ###################Right Main Layout widget###################
        ###################Right  top Layout widget###################
        self.searchText = QLabel("Search")
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("Search For Products")
        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.searchProduct)
        self.searchButton.setStyleSheet("QPushButton { background-color: #fcc324;  border-style:outset; border-style:outset; border-width: 2px ; border-radius:10px; border-color:beige; font:12px; padding:6px;min-width:6em;}"
                                         "QPushButton:pressed { background-color: red;}" )

        ###################Right  middle Layout widgets###################
        self.allProducts = QRadioButton("All Products")
        self.availableProducts = QRadioButton("Available")
        self.notAvailableProducts = QRadioButton("Not Available")
        self.listButton = QPushButton("List")
        self.listButton.clicked.connect(self.listProducts)
        self.listButton.setStyleSheet(("QPushButton { background-color: #9bc9ff;  border-style:outset; border-style:outset; border-width: 2px ; border-radius:10px; border-color:beige; font:12px; padding:6px;min-width:6em;}"
                                         "QPushButton:pressed { background-color: red;}" ))

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
        self.memberTable.doubleClicked.connect(self.selectedMember)
        ###################Right widget###################
        self.memberSearchText = QLabel("Search Members")
        self.memberSearchEntry = QLineEdit()
        self.memberSearchButton = QPushButton("Search")
        self.memberSearchButton.clicked.connect(self.searchMember)

        ##########################################################
        ###################Tab3 Widgets###########################
        ##########################################################
        self.totalProductsValue=QLabel()
        self.totalMembersValue=QLabel()
        self.soldProductsValue=QLabel()
        self.totalAmountValue=QLabel()


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
        self.topGroupBox.setStyleSheet(style.searchBoxStyle())#function outside the class
        self.middleGroupBox = QGroupBox("List Box")
        self.middleGroupBox.setStyleSheet(style.listhBoxStyle())
        self.bottomGroupBox = QGroupBox()
        ###################Add layouts###################
        self.mainLayout.addLayout(self.leftMainLayout, 70)
        self.leftMainLayout.addWidget(self.productTable)
        ##################Right Main Layout#####################
        self.mainLayout.addLayout(self.rightMainLayout, 30)
        self.rightMainLayout.addWidget(self.topGroupBox,20)
        self.rightMainLayout.addWidget(self.middleGroupBox,20)
        self.rightMainLayout.addWidget(self.bottomGroupBox,60)
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
        ###################Tab2 Layout##########################
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
        ###################Tab3 Layout##########################
        ########################################################
        self.statisticsMainLayout=QVBoxLayout()
        self.statisticsLayout=QFormLayout()
        self.statisticsGroupBox=QGroupBox("Statistics")
        self.statisticsGroupBox.setLayout(self.statisticsLayout)
        self.statisticsGroupBox.setFont(QFont("Arial",28))
        self.statisticsMainLayout.addWidget(self.statisticsGroupBox)
        self.tab3.setLayout(self.statisticsMainLayout)
        ###############Adding statistics Form LAyout widgets################
        self.statisticsLayout.addRow(QLabel("Total Products: "), self.totalProductsValue)
        self.statisticsLayout.addRow(QLabel("Total members: "), self.totalMembersValue)
        self.statisticsLayout.addRow(QLabel("Sold Products: "), self.soldProductsValue)
        self.statisticsLayout.addRow(QLabel("Total Amount: "),self.totalAmountValue)
        self.tabs.blockSignals(False)#one at the end , but its not enough we should creat a funct ,to refresh our tabs


        ########################################################
        ###################Action functions######################
        ########################################################

    def funcAddProduct(self):
        self.newProduct = addproduct.AddProduct()  # addproduct is our new python file/ AddProduct is the class

    def funAddMember(self):
        self.newMember = addmember.AddMember()

    def funcSellProduct(self):
        self.sell=sellings.SellProduct()

    def getSatistics(self):
        countProducts=cur.execute(("SELECT count(product_id) FROM products")).fetchone()#fonction count qui somme le nombre de differents produit
        countMembers=cur.execute(("SELECT count(member_id) FROM members")).fetchone()
        soldProducts=cur.execute(("SELECT sum(selling_quantity) FROM sellings")).fetchone()
        totalAmount=cur.execute(("SELECT sum(selling_amount) FROM sellings")).fetchone()
        self.totalProductsValue.setText(str(countProducts[0]))
        self.totalMembersValue.setText(str(countMembers[0]))
        self.soldProductsValue.setText(str(soldProducts[0]))
        self.totalAmountValue.setText(str(totalAmount[0] )+"euros")
    ###############################the refresh function##########################
    def tabChanged(self):
        #here we call all the displaying functions, when a change has happened
        self.displayProduct()
        self.displayMembers()
        self.getSatistics()

    def displayProduct(self):
        self.productTable.setFont(QFont("Times", 12))
        print("display products")
        print(self.productTable.rowCount())
        # we need to remove or clean our table widgets first
        for i in reversed(range(self.productTable.rowCount())):
            print("i:", i)
            self.productTable.removeRow(i)
        query = cur.execute(
            "SELECT product_id,product_name,product_manufacturer,product_price,product_qouta, product_availability FROM products")
        for row_data in query:  # 0,1,2
            print(
                row_data)  # first row :(1, 'Playstation', 'Sony', 300, 50, 'Available'),second :(2, 'computer', 'HP', 1200, 21, 'Available'),third: (3, 'S9', 'Samsung', 400, 33, 'Available')
            row_number = self.productTable.rowCount()
            print(row_number)  # 0,1,2
            self.productTable.insertRow(row_number)  # inserting row zero,row 1 , row 2
            # exemple if there is 3 rows in the query
            # the first time i insert an empty row in the table, then i fill it with info from the query
            for column_number, data in enumerate(row_data):  # column number is how many element in the row_data list
                self.productTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.productTable.setEditTriggers(
            QAbstractItemView.NoEditTriggers)  # this line will prevent someone from changing the table product

    def displayMembers(self):
        self.memberTable.setFont(QFont("Times", 12))
        for i in reversed(range(self.memberTable.rowCount())):
            self.memberTable.removeRow(i)
        query = con.execute("SELECT member_id,member_name,member_surname,member_phone FROM members")
        for row_number, row_data in enumerate(query):
            print(row_data)
            print("Row", row_number)  # another methode
            self.memberTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.memberTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.memberTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def selectedProduct(self):
        global productId  # so we could use it the id in another class
        listProduct = []
        for i in range(0, 6):  # we have 6 feildes (prodct ud, prod name...)
            listProduct.append(self.productTable.item(self.productTable.currentRow(), i).text())
            # result(listproduct values each lap) of this for loop:
            # ['1']
            # ['1', 'Playstation']
            # ['1', 'Playstation', 'Sony']
            # ['1', 'Playstation', 'Sony', '300']
            # ['1', 'Playstation', 'Sony', '300', '50']
            # ['1', 'Playstation', 'Sony', '300', '50', 'Available']
        productId = listProduct[0]  # first elment is the id that we gonna use it after
        self.display = DisplayProduct()

    def selectedMember(self):
        global memberId
        listMember = []
        for i in range(0, 4):
            listMember.append(self.memberTable.item(self.memberTable.currentRow(), i).text())
        memberId=listMember[0]
        #print(listMember)
        self.displayMembersWindow=DisplayMember()

    def searchProduct(self):
        value=self.searchEntry.text()
        if value == "":
            QMessageBox.information(self,"WARNING","Search bar cannot be empty!!")
        else:
            self.searchEntry.setText("")
            #i want to display all fields but not the image, and we are searching by our product name, and product manufact only(LIKE ?)
            query=("SELECT product_id,product_name,product_manufacturer,product_price,product_qouta,product_availability  FROM products WHERE product_name LIKE ? or product_manufacturer LIKE ?")
            # the % means that the product name or manufct , starts or ends with my value : exemple playstation => we can search by tion or pla
            results=cur.execute(query,("%"+value+"%","%"+value+"%")).fetchall()
            if results == []:
                QMessageBox.information(self, "WARNING", "Cannot find what you are looking for!!")
            else:
                #now i should remove evrything on the window and display de nouveau the products detected by our search
                for i in reversed(range(self.productTable.rowCount())):
                    self.productTable.removeRow(i)
                for row_count,row_data in enumerate(results):
                    self.productTable.insertRow(row_count)
                    for column,data in enumerate(row_data):
                        self.productTable.setItem(row_count,column,QTableWidgetItem(str(data)))

    def searchMember(self):
        value=self.memberSearchEntry.text()
        if value == "":
            QMessageBox.information(self,"WARNING","Search bar cannot  be empty")
        else:
            query=("SELECT member_id,member_name,member_surname,member_phone FROM members WHERE member_name LIKE ? or member_surname LIKE ? or member_phone LIKE ?")
            results=cur.execute(query,("%"+value+"%","%"+value+"%","%"+value+"%"))
            if results == []:
                QMessageBox.information(self, "WARNING", "Member not found")
            else:
                for i in reversed(range(self.memberTable.rowCount())):
                    self.memberTable.removeRow(i)
                for row_count,row_data in enumerate(results):#row_count means the number of the current row
                    self.memberTable.insertRow(row_count)
                    for column, data in enumerate(row_data):
                        self.memberTable.setItem(row_count,column,QTableWidgetItem(str(data)))


    def listProducts(self):
        if self.allProducts.isChecked() == True:
            self.displayProduct()

        elif self.availableProducts.isChecked():
            query=("SELECT product_id,product_name,product_manufacturer,product_price,product_qouta,product_availability FROM products WHERE product_availability='Available'")
            result= cur.execute(query).fetchall()
            for i in reversed(range(self.productTable.rowCount())):
                self.productTable.removeRow(i)
            for row_count, row_data in enumerate(result):
                self.productTable.insertRow(row_count)
                for column, data in enumerate(row_data):
                    self.productTable.setItem(row_count, column, QTableWidgetItem(str(data)))

        elif self.notAvailableProducts.isChecked():
            query=("SELECT product_id,product_name,product_manufacturer,product_price,product_qouta,product_availability FROM products WHERE product_availability='Unavailable'")
            result= cur.execute(query).fetchall()
            for i in reversed(range(self.productTable.rowCount())):
                self.productTable.removeRow(i)
            for row_count, row_data in enumerate(result):
                self.productTable.insertRow(row_count)
                for column, data in enumerate(row_data):
                    self.productTable.setItem(row_count, column, QTableWidgetItem(str(data)))





    ###################################################################################
    ###################New Class for displaying each member spec######################
    ###################################################################################
class DisplayMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Member Details")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(450,150,350,600)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.memberDetails()
        self.widgets()
        self.layouts()


    def memberDetails(self):
        global memberId
        try:
            query=("SELECT * FROM members WHERE member_id = ?")
            member=cur.execute(query,(memberId,)).fetchone()
            print(member)
            self.memberName=member[1]
            self.memberSurname=member[2]
            self.memberPhone=member[3]

        except:
            QMessageBox.warning(self,"WARNING","ERROR while fetching data")

    def widgets(self):
        #####################Creating top  widgets################
        self.memberImg=QLabel()
        self.memberImg.setPixmap(QPixmap("icons/members.png"))
        self.memberImg.setAlignment(Qt.AlignCenter)
        self.memberText=QLabel("Display Member")
        self.memberText.setAlignment(Qt.AlignCenter)
        #####################Creating bottom  widgets################
        self.nameEntry=QLineEdit()
        self.nameEntry.setText(self.memberName)
        self.surnameEntry=QLineEdit()
        self.surnameEntry.setText(self.memberSurname)
        self.phoneEntry=QLineEdit()
        self.phoneEntry.setText(self.memberPhone)
        self.deleteBtn=QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.deleteMember)
        self.updateBtn=QPushButton("Update")
        self.updateBtn.clicked.connect(self.updateMember)

    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QVBoxLayout()
        self.bottomLayout=QFormLayout()
        self.topFrame=QFrame()
        self.topFrame.setStyleSheet(style.memberTopFrameStyle())
        self.bottomFrame=QFrame()
        self.bottomFrame.setStyleSheet(style.memberBottomFrameStyle())

        #######################Adding top layout widgets####################
        self.topLayout.addWidget(self.memberText)
        self.topLayout.addWidget(self.memberImg)
        #######################Adding bottom layout widgets####################
        self.bottomLayout.addRow(QLabel("Name: "),self.nameEntry)
        self.bottomLayout.addRow(QLabel("Surname: "),self.surnameEntry)
        self.bottomLayout.addRow(QLabel("Phone: "),self.phoneEntry)
        self.bottomLayout.addRow(QLabel(""),self.updateBtn)
        self.bottomLayout.addRow(QLabel(""),self.deleteBtn)

        #######################setting  main  layout ####################
        self.topFrame.setLayout(self.topLayout)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    ######################Actions Functions ################################
    def deleteMember(self):
        global memberId
        choice = QMessageBox.question(self,"WARNING","Are you sure you want to delete this member?!",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if choice == QMessageBox.Yes:
            try:
                cur.execute(("DELETE FROM members WHERE member_id=?"),(memberId))
                con.commit()
                QMessageBox.information(self,"INFO","Member has been deleted")
                self.close()
            except :
                QMessageBox.information(self, "WARNING", "Member has not been deleted")

    def updateMember(self):
        global memberId
        name = self.nameEntry.text()
        surname= self.surnameEntry.text()
        phone= self.phoneEntry.text()

        if (name and surname and phone != ""):
            try:
                query="UPDATE members SET member_name=?,member_surname=?,member_phone=? WHERE member_id=? "
                cur.execute(query,(name,surname,phone,memberId))
                con.commit()
                QMessageBox.information(self, "INFO", "Member has been updated successfully")

            except :
                QMessageBox.information(self, "WARNING", "Member has not been updated")

        else:
            QMessageBox.information(self, "WARNING", "Fields cannot be empty!!")







    ###################################################################################
    ###################New Class for displaying each product spec######################
    ###################################################################################


class DisplayProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Details")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(450, 150, 350, 600)
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
        query = ("SELECT * FROM products WHERE product_id=?")
        productDetails = cur.execute(query, (productId,)).fetchone()
        print(productDetails)  # (1, 'Playstation', 'Sony', 300, 50, '71PGvPXpk5L._AC_.jpg', 'Available')
        self.productName = productDetails[1]
        self.productManufacturer = productDetails[2]
        self.productPrice = productDetails[3]
        self.productQouta = productDetails[4]
        self.productImg = productDetails[5]
        self.productAvailability = productDetails[6]

    def widgets(self):
        ########################adding top widgets########################
        self.product_Img = QLabel()
        self.product_Img.setPixmap(QPixmap("img/{}".format(self.productImg)))
        self.product_Img.setAlignment(Qt.AlignCenter)
        self.productText = QLabel("Update Product")
        self.productText.setAlignment(Qt.AlignCenter)
        ########################adding bottom widgets####################
        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.productName)
        self.manufacturerEntry = QLineEdit()
        self.manufacturerEntry.setText(self.productManufacturer)
        self.priceEntry = QLineEdit()
        self.priceEntry.setText(str(self.productPrice))
        self.qoutaEntry = QLineEdit()
        self.qoutaEntry.setText(str(self.productQouta))
        self.availabilityComboBox = QComboBox()
        self.availabilityComboBox.addItems(["Available", "Unavailable"])
        self.uploadBtn = QPushButton("Upload")
        self.uploadBtn.clicked.connect(self.uploadImageFunc)
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.deleteProductFunc)
        self.updateBtn = QPushButton("Update")
        self.updateBtn.clicked.connect(self.updateProductFunc)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.topFrame.setStyleSheet(style.productTopFrameStyle())
        self.bottomFrame = QFrame()
        self.bottomFrame.setStyleSheet(style.productBottomFrameStyle())
        ####################adding top widgets ##############
        self.topLayout.addWidget(self.productText)
        self.topLayout.addWidget(self.product_Img)
        ####################adding bottom widgets ##############
        self.bottomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("Manufacturer: "), self.manufacturerEntry)
        self.bottomLayout.addRow(QLabel("Price: "), self.priceEntry)
        self.bottomLayout.addRow(QLabel("Qouta: "), self.qoutaEntry)
        self.bottomLayout.addRow(QLabel("Status: "), self.availabilityComboBox)
        self.bottomLayout.addRow(QLabel("Image: "), self.uploadBtn)
        self.bottomLayout.addRow(QLabel(""), self.deleteBtn)
        self.bottomLayout.addRow(QLabel(""), self.updateBtn)

        ####################setting main Layout#####################
        self.topFrame.setLayout(self.topLayout)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    ################################Action Functions################
    def uploadImageFunc(self):
        size = (256, 256)
        self.filename, ok = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.png *.jpg)")
        if ok:
            self.productImg = os.path.basename(
                self.filename)  # filename is contains the path from where i chose the picture
            img = Image.open(self.filename)  # then i open the img
            img = img.resize(size)
            img.save("img/{}".format(self.productImg))

    def updateProductFunc(self):
        global productId
        name = self.nameEntry.text()
        manufacturer = self.manufacturerEntry.text()
        price = int(self.priceEntry.text())
        qouta = int(self.qoutaEntry.text())
        status = self.availabilityComboBox.currentText()
        img = self.productImg

        if (name and manufacturer and price and qouta != ""):
            try:
                query = "UPDATE products set product_name=? ,product_manufacturer=? ,product_price=? ,product_qouta=?,product_img= ?,product_availability=? WHERE product_id=? "
                cur.execute(query, (name, manufacturer, price, qouta, img, status, productId))
                con.commit()
                QMessageBox.information(self, "Info", "Product has been successfully updated")
            except:
                QMessageBox.information(self, "WARNING", "Product has not  been  updated")
        else:
            QMessageBox.information(self, "Warning", "Fields cant be empty !!")

    def deleteProductFunc(self):
        global productId
        choice = QMessageBox.question(self, "WARNING", "Are you sure you want to delete this product?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if (choice == QMessageBox.Yes):
            try:
                cur.execute("DELETE FROM products WHERE product_id=?", (productId,))
                con.commit()
                QMessageBox.information(self, "Info", "Product has been deleted")
                self.close()
            except:
                QMessageBox.information(self, "WARNING", "Product has not been deleted")


###########################################################MAIN######################################
def main():
    App = QApplication(sys.argv)
    # App.setWindowIcon(QIcon("icons/icon.ico")) we con put an icon to the window in this way too
    window = Main()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
