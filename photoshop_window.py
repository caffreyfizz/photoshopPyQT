import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    


class Photoshop(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('photoshop.ui', self)
        
        #db_name = "users.sqlite"
        #self.con = sqlite3.connect(db_name)
        #self.cur = self.con.cursor()
        #self.curr_image = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]

        self.circuit_btn.clicked.connect(self.circuit)
        self.detailing_btn.clicked.connect(self.detailing)
        self.bright_warm_btn.clicked.connect(self.bright_warm)
        self.bright_btn.clicked.connect(self.bright)
        self.chill_btn.clicked.connect(self.chill)
        self.blackwhite_btn.clicked.connect(self.blackwhite)
        self.back_btn.clicked.connect(self.back)

    def circuit(self):
        pass

    def detailing(self):
        pass

    def bright_warm(self):
        pass

    def bright(self):
        pass

    def chill(self):
        pass

    def blackwhite(self):
        pass

    def back(self):
        pass

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = Photoshop()
    plan.show()
    sys.exit(app.exec_())