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
        pass


def main():
    App = QApplication(sys.argv)
    # App.setWindowIcon(QIcon("icons/icon.ico")) we con put an icon to the window in this way too
    window = AddProduct()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()