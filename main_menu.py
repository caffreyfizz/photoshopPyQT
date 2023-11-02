import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from photoshop_window import Photoshop


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        
        #db_name = "users.sqlite"
        #self.con = sqlite3.connect(db_name)
        #self.cur = self.con.cursor()
        self.folder_btn.setIcon(QIcon("folder.png"))
        self.folder_btn.setIconSize(QSize(121, 111))

        self.add_btn.clicked.connect(self.new_photo)

    def new_photo(self):
        Photoshop().show()
        self.close()


        
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = MainWindow()
    plan.show()
    sys.exit(app.exec_())