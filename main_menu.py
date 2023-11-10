import sys
import os
import io
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QHeaderView, QFrame
from PyQt5 import QtCore, QtWidgets
from photoshop_window import Photoshop
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
from PIL import Image

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    


class MainWindow(QMainWindow):
    def __init__(self, login):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        db_name = "users.sqlite"
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        
        self.login = login
        self.buttons_icon = []
        
        self.imgTable.verticalHeader().hide()
        self.imgTable.horizontalHeader().hide()
        self.imgTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.imgTable.setFrameStyle(QFrame.NoFrame)
        self.imgTable.setShowGrid(False)
        self.imgTable.verticalHeader().setDefaultSectionSize(180)
        self.imgTable.

        self.welcomeLabel.setText(f"Добро пожаловать, {self.login}")
        self.add_btn.clicked.connect(self.new_photo)
        images = self.cur.execute("""SELECT name FROM images WHERE user=(SELECT id from logins WHERE login = ?)""",
                                        (self.login,)).fetchall()
        if not images:
            self.imgTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.imgTable.setRowCount(3)
            self.imgTable.setColumnCount(3)
            no_find_img = QLabel()
            no_find_img.setText("Нет изображений")
            no_find_img.setAlignment(QtCore.Qt.AlignCenter)
            self.imgTable.setCellWidget(1, 1, no_find_img)
        else:
            all_images = self.cur.execute("""SELECT name FROM images WHERE user=
                                          (SELECT id FROM logins WHERE login=?)""", (self.login,)).fetchall()
            column = 0
            line = 0
            self.imgTable.setRowCount(len(all_images) // 5 + 1)
            self.imgTable.setColumnCount(5)
            img_counter = 1
            for i in range(len(all_images)):
                if column == 4:
                    line += 1
                    column = 0
                self.button = QPushButton(f"image{img_counter}")
                self.buttons_icon.append(self.button)
                with Image.open(io.BytesIO(all_images[i][0])) as img_icon:
                    img_icon.save(f"image{img_counter}.png")
                    self.result_pm = QPixmap(f"image{img_counter}.png")
                    scaled = self.result_pm.scaled(self.button.size(), QtCore.Qt.KeepAspectRatio)
                    self.button.setIcon(QIcon(scaled))
                    self.button.setIconSize(QSize(640, 480))
                self.imgTable.setCellWidget(line, column, self.button)
                os.remove(f"image{img_counter}.png")
                column += 1
                img_counter += 1


    def new_photo(self):
        self.phtsp = Photoshop(self.login)
        self.phtsp.show()
        self.close()


        
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = MainWindow()
    plan.show()
    sys.exit(app.exec_())