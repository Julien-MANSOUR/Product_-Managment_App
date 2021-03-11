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






