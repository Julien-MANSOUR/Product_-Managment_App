import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Manager")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(450, 150, 1350, 750)
        self.setFixedSize(self.size())  # to fix windows size without minimize or maximize it
        self.UI()
        self.show()

    def UI(self):
        self.toolBar()

    def toolBar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # so the name we chose could appear under the button
        ##################ToolBar Button###################
        #################Add Product ######################
        self.addProduct=QAction(QIcon("icons/add.png"),"Add Product",self)
        self.tb.addAction(self.addProduct)
        self.tb.addSeparator()
        #################Add Product ######################
        self.addMember=QAction(QIcon("icons/users.png"),"Add Member",self)
        self.tb.addAction(self.addMember)
        self.tb.addSeparator()
        #################Add Product ######################
        self.sellProduct=QAction(QIcon("icons/sell.png"),"Sell Product",self)
        self.tb.addAction(self.sellProduct)
        self.tb.addSeparator()

def main():
    App = QApplication(sys.argv)
    # App.setWindowIcon(QIcon("icons/icon.ico")) we con put an icon to the window in this way too
    window = Main()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
