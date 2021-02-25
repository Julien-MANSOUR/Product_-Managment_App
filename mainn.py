import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Manager")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(450, 150, 1350, 750)
        self.setFixedSize(self.size())# to fix windows size without minimize or maximize it 
        self.UI()
        self.show()

    def UI(self):
        pass


def main():
    App = QApplication(sys.argv)
    #App.setWindowIcon(QIcon("icons/icon.ico")) we con put an icon to the window in this way too
    window = Main()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
