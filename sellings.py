import sys, os
import sqlite3
import addproduct, addmember
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PIL import Image
###################Data base###########################
con = sqlite3.connect("Products.db")
cur = con.cursor()



class SellProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Product")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(458, 150, 350, 600)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ##########################Creating Top widgets######################
        self.sellProductImg=QLabel()
        self.sellProductImg.setPixmap(QPixmap("icons/shop.png"))
        self.sellProductImg.setAlignment(Qt.AlignCenter)
        self.sellProductText=QLabel("Sell Products")
        self.sellProductText.setAlignment(Qt.AlignCenter)
        ##########################Creating bottom widgets######################
        self.productCombo=QComboBox()
        self.productCombo.currentIndexChanged.connect(self.changeComboValue)#to connect the product combo to its quantity combo
        self.memberCombo=QComboBox()
        self.quantityCombo=QComboBox()
        self.submitBtn=QPushButton("Submit")
        self.submitBtn.clicked.connect(self.sellProduct)



    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QVBoxLayout()
        self.bottomLayout=QFormLayout()
        self.topFrame=QFrame()
        self.bottomFrame=QFrame()
        #############################Adding top widgets#######################
        self.topLayout.addWidget(self.sellProductImg)
        self.topLayout.addWidget(self.sellProductText)
        #############################Adding bottom widgets#######################
        self.bottomLayout.addRow(QLabel("Name: "),self.productCombo)
        self.bottomLayout.addRow(QLabel("Member: "),self.memberCombo )
        self.bottomLayout.addRow(QLabel("Quantity: "),self.quantityCombo )
        self.bottomLayout.addRow(QLabel(""),self.submitBtn )
        #############################Setting mainlayout widgets#######################
        self.topFrame.setLayout(self.topLayout)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)




        query1=("SELECT * FROM products WHERE product_availability=?")
        products=cur.execute(query1,("Available",)).fetchall()
        print(products)#[(4, 'PS5', 'SONY', 650, 20, '1280x720+Filler+Image.jpeg', 'Available'), (6, 'S9', 'Samsung', 200, 20, '41XDA3cCeOL.jpg', 'Available')]
                       #its a list containning tupls, so to choose the quantity (20) of the ps5, it is products[0][4]
        product_number =[]
        quantity=products[0][4]

        for product in products:
            self.productCombo.addItem(str(product[1]),str(product[0]))#product[0] is the id , im using it but @hiden


        query2=("SELECT member_id,member_name FROM members ")
        members=cur.execute(query2).fetchall()

        for member in members:
            self.memberCombo.addItem(member[1],member[0])


        #for i in range(1, quantity + 1):
           # self.quantityCombo.addItem(str(i))

    def changeComboValue(self):
        product_id=self.productCombo.currentData()# we didnt choose currentText(),bcz we need the @hiden data that we placed it before , and it was the  id
        print(product_id)
        query=("SELECT product_qouta FROM products WHERE product_id =?")
        quantity=cur.execute(query,(product_id,)).fetchone()
        print(quantity)
        self.quantityCombo.clear()
        for i in range(1, quantity[0] + 1):
            self.quantityCombo.addItem(str(i))



    def sellProduct(self):
        global productName, productId,memberName,memberId,quantity #i need them in the other class
        productName=self.productCombo.currentText()
        productId=self.productCombo.currentData()# the @hiden values str(product[0])
        memberName=self.memberCombo.currentText()
        memberId=self.memberCombo.currentData()
        quantity=int(self.quantityCombo.currentText())
        self.confirm=ConfirmWindow()
        self.close()


##############################################################
#######################ConfirmWindow Class##########################
##############################################################

class ConfirmWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Product")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(458, 150, 350, 600)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ##########################top widgets####################
        self.sellProductImg=QLabel()
        self.sellProductImg.setPixmap(QPixmap("icons/shop.png"))
        self.sellProductImg.setAlignment(Qt.AlignCenter)
        self.sellProductText=QLabel("Sell Product")
        self.sellProductText.setAlignment(Qt.AlignCenter)
        ###########################Bottom widgets################
        global productName, productId, memberName, memberId, quantity
        priceQuery=("SELECT product_price FROM products WHERE product_id=?")
        price=cur.execute(priceQuery,(productId,)).fetchone()
        self.ammount=price[0]*quantity
        print(self.ammount)
        self.ProductText=QLabel()
        self.ProductText.setText(productName)
        self.memberText=QLabel()
        self.memberText.setText(memberName)
        self.ammountText=QLabel("{}x{}={}".format(price[0],quantity,self.ammount))
        self.confirmBtn=QPushButton("Confirm")
        self.confirmBtn.clicked.connect(self.confirmFunc)

    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QVBoxLayout()
        self.bottomLayout=QFormLayout()
        self.topFrame=QFrame()
        self.bottomFrame=QFrame()
        #############################Adding top widgets####################
        self.topLayout.addWidget(self.sellProductText)
        self.topLayout.addWidget(self.sellProductImg)
        #############################Adding Bottom widgets####################
        self.bottomLayout.addRow(QLabel("Product: "),self.ProductText)
        self.bottomLayout.addRow(QLabel("Memeber: "),self.memberText)
        self.bottomLayout.addRow(QLabel("Amount: "),self.ammountText)
        self.bottomLayout.addRow(QLabel(""),QLabel(""))
        self.bottomLayout.addRow(QLabel(""),self.confirmBtn)
        ############################ Setting mainlayout ####################
        self.topFrame.setLayout(self.topLayout)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    #####################Action functions########################
    def confirmFunc(self):
        global productName, productId, memberName, memberId, quantity
        try:
            sellingsQuery=("INSERT INTO 'sellings' (selling_product_id,selling_member_id,selling_quantity,selling_amount)  VALUES(?,?,?,?)  ")
            cur.execute(sellingsQuery,(productId,memberId,quantity,self.ammount))
            #we need a query for the quota to update it each time we sell products
            qoutaQuery=("SELECT product_qouta FROM products WHERE product_id=?")
            qouta=cur.execute(qoutaQuery,(productId,)).fetchone()#exemple : 20
            print(qouta[0])
            con.commit()

            if quantity == qouta[0]:
                updateQoutaQuery=("UPDATE products set product_qouta=?,product_availability=? WHERE product_id=?")
                cur.execute(updateQoutaQuery,(0,'Unavailable',productId))
                con.commit()
                con.close()
            else:
                newQouta = qouta[0] - quantity  # 20-10=10
                updateQoutaQuery = ("UPDATE products SET product_qouta=? WHERE product_id=? ")
                cur.execute(updateQoutaQuery, (newQouta,productId))
                con.commit()
                con.close()

            QMessageBox.information(self,"INFO","SUCCESS")

        except :
            QMessageBox.information(self, "INFO", "Something went wrong")