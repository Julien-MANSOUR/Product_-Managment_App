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


class AddMember(QWidget):
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
        #################Creating Top widgets####################
        self.addMemberImg=QLabel()
        self.img=QPixmap("icons/addmember.png")
        self.addMemberImg.setPixmap(self.img)
        self.addMemberImg.setAlignment(Qt.AlignCenter)#to meve my img to the center , we can also use set margin
        self.titleText=QLabel("Add Member")
        self.titleText.setAlignment(Qt.AlignCenter)
        #################Creating Bottom widgets####################
        self.nameEntry=QLineEdit()
        self.nameEntry.setPlaceholderText("Enter name of member")
        self.surnameEntry = QLineEdit()
        self.surnameEntry.setPlaceholderText("Enter Surname of member")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setPlaceholderText("Enter phone number")
        self.submitBtn=QPushButton("Submit")






    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QVBoxLayout()
        self.bottomLayout=QFormLayout()
        self.topFrame=QFrame()
        self.bottomFrame=QFrame()
        #################add top layout widgets ###############
        self.topLayout.addWidget(self.addMemberImg)
        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)
        #################add bottom layouts widgets#############
        self.bottomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("Surname: "), self.surnameEntry)
        self.bottomLayout.addRow(QLabel("Phone: "), self.phoneEntry)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)
        ################# setting mainLayout##################
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)



