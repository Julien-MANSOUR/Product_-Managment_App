import sys
import sqlite3
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PIL import Image

###################Data base###########################
con = sqlite3.connect("Products.db")
cur = con.cursor()

##################Global variables##########################
defaultImg = "store.png"


class AddProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Product")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(458, 150, 350, 350)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ###############widgets of top layout#################
        self.addProductImg = QLabel()
        self.img = QPixmap("icons/addproduct.png")
        self.addProductImg.setPixmap(self.img)
        self.titleText = QLabel("Add Product")

        ###############widgets of bottom layout#################
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter name of product")
        self.manufactirerEntry = QLineEdit()
        self.manufactirerEntry.setPlaceholderText("Enter name of manufacturer")
        self.priceEntry = QLineEdit()
        self.priceEntry.setPlaceholderText("Enter price of product")
        self.qoutaEntry = QLineEdit()
        self.qoutaEntry.setPlaceholderText("Enter qouta of product")
        self.uploadBtn = QPushButton("Upload")
        self.uploadBtn.clicked.connect(self.uploadImg)
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.addProduct)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()  # QFrame is similar to groupeBox
        self.bottomFrame = QFrame()
        ################# add widgets######################

        #################top layout widgets################
        self.topLayout.addWidget(self.addProductImg)
        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)
        #################bottom layout widgets################
        self.bottomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("Manufacturer: "), self.manufactirerEntry)
        self.bottomLayout.addRow(QLabel("Price: "), self.priceEntry)
        self.bottomLayout.addRow(QLabel("Qouta: "), self.qoutaEntry)
        self.bottomLayout.addRow(QLabel("Upload: "), self.uploadBtn)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        ####################main layout widgets#################3
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    ########################################Action functions##################################

    ####################mUploading Image #################3
    def uploadImg(self):
        global defaultImg
        size = (256, 256)  # image size
        self.filename, ok = QFileDialog.getOpenFileName(self, "Upload,Image", "", "Image Files (*.jpg *.png *.jpeg)")
        if ok:
            print(self.filename)  # it gives us the whole URL of the img
            defaultImg = os.path.basename(self.filename)  # only the name of the img.png
            print(defaultImg)
            img = Image.open(self.filename)  # i need to use the whole URL of image
            img = img.resize(size)
            img.save("img/{0}".format(defaultImg))

    ####################add Product to data base #################
    def addProduct(self):
        global defaultImg
        name = self.nameEntry.text()
        manufacturer = self.manufactirerEntry.text()
        price = self.priceEntry.text()
        qouta = self.qoutaEntry.text()
        #img is already in defaultImg
        #product availability has already a default value:Available
        if (name and manufacturer and price and qouta !=""):#should not be empty
            try:
                query="INSERT INTO 'products' (product_name,product_manufacturer,product_price,product_qouta,product_img) VALUES(?,?,?,?,?) "
                cur.execute(query,(name,manufacturer,price,qouta,defaultImg))
                con.commit()#when we change something in the data base we should commit the change
                QMessageBox.information(self,"Info","Product has been added successfully")
                #con.close()
            except:
                QMessageBox.warning(self,"Warning","Product has not been added !")
        else:
            QMessageBox.warning(self,"Warning","Fields cant be empty !!")
def main():
    App = QApplication(sys.argv)
    # App.setWindowIcon(QIcon("icons/icon.ico")) we con put an icon to the window in this way too
    window = AddProduct()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
