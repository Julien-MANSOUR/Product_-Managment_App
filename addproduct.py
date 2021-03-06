import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

###################Data base###########################
con = sqlite3.connect("Products.db")
cur = con.cursor()
#######################################################

class AddProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Product")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(458,150,350,350)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()


    def widgets(self):
        ###############widgets of top layout#################
        self.addProductImg=QLabel()
        self.img=QPixmap("icons/addproduct.png")
        self.addProductImg.setPixmap(self.img)
        self.titleText=QLabel("Add Product")
        ###############widgets of bottom layout#################
        self.nameEntry=QLineEdit()
        self.nameEntry.setPlaceholderText("Enter name of product")
        self.manufactirerEntry=QLineEdit()
        self.manufactirerEntry.setPlaceholderText("Enter name of manufacturer")
        self.priceEntry=QLineEdit()
        self.priceEntry.setPlaceholderText("Enter price of product")
        self.qoutaEntry=QLineEdit()
        self.qoutaEntry.setPlaceholderText("Enter qouta of product")
        self.uploadBtn=QPushButton("Upload")
        self.submitBtn=QPushButton("Submit")





    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QHBoxLayout()
        self.bottomLayout=QFormLayout()
        self.topFrame=QFrame() #QFrame is similar to groupeBox
        self.bottomFrame=QFrame()
        ################# add widgets######################

        #################top layout widgets################
        self.topLayout.addWidget(self.addProductImg)
        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)
        #################bottom layout widgets################
        self.bottomLayout.addRow(QLabel("Name: "),self.nameEntry)
        self.bottomLayout.addRow(QLabel("Manufacturer: "),self.manufactirerEntry)
        self.bottomLayout.addRow(QLabel("Price: "),self.priceEntry)
        self.bottomLayout.addRow(QLabel("Qouta: "),self.qoutaEntry)
        self.bottomLayout.addRow(QLabel("Upload: "),self.uploadBtn)
        self.bottomLayout.addRow(QLabel(""),self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        ####################main layout widgets#################3
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)


def main():
    App = QApplication(sys.argv)
    # App.setWindowIcon(QIcon("icons/icon.ico")) we con put an icon to the window in this way too
    window = AddProduct()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()