import sys
import os
import io
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QHeaderView, QFrame, QButtonGroup
from PyQt5 import QtCore, QtWidgets, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
from PIL import Image
from photoshop_window import Photoshop

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    


class MainWindow(QMainWindow):
    def __init__(self, login):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.setWindowTitle("Главное меню")
        self.setStyleSheet('.QWidget {background-image: url(background.jpg);}')

        db_name = "users.sqlite"
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        
        self.login = login
        self.buttons_icon = {}
        self.all_buttons = QButtonGroup()

        style_for_table = """
            QTableWidget {
                background-image: url(background.jpg);  
                color: blue;             
            }
        """

        style_for_btn = """background-color: rgb(255, 255, 255);\n
border-radius: 10px;\n
\n
}\n
QPushButton:hover{    \n
    background-color: rgb(191, 191, 191);\n
    effect = QtWidgets.QGraphicsDropShadowEffect(QPushButton)\n
    effect.setOffset(0, 0)\n
    effect.setBlurRadius(20)\n
    effect.setColor(QColor(57, 219, 255))\n
    QPushButton.setGraphicsEffect(effect)
    border-radius: 48px;        /* круглый */
border: 2px solid #09009B;
"""
        self.add_btn.setStyleSheet(style_for_btn)
        self.imgTable.setStyleSheet(style_for_table)
        
        self.imgTable.verticalHeader().hide()
        self.imgTable.horizontalHeader().hide()
        self.imgTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.imgTable.setFrameStyle(QFrame.NoFrame)
        self.imgTable.setShowGrid(False)
        self.imgTable.verticalHeader().setDefaultSectionSize(180)

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
                self.button = QPushButton(f"image{img_counter}", objectName=f"btn{img_counter}")
                self.all_buttons.addButton(self.button)
                self.button.text()
                
                with Image.open(io.BytesIO(all_images[i][0])) as img_icon:
                    self.buttons_icon[self.button] = io.BytesIO(all_images[i][0])
                    
                    img_icon.save(f"image{img_counter}.png")
                    self.result_pm = QPixmap(f"image{img_counter}.png")
                    scaled = self.result_pm.scaled(self.button.size(), QtCore.Qt.KeepAspectRatio)
                    self.button.setIcon(QIcon(scaled))
                    self.button.setIconSize(QSize(640, 480))
                
                self.imgTable.setCellWidget(line, column, self.button)
                os.remove(f"image{img_counter}.png")
                column += 1
                img_counter += 1

            self.all_buttons.buttonClicked.connect(self.open_photo)


    def new_photo(self):
        self.phtsp = Photoshop(self.login)
        self.phtsp.show()
        self.close()

    def open_photo(self, btn):
        self.phtsp = Photoshop(self.login, self.buttons_icon[btn])
        self.phtsp.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = MainWindow()
    plan.show()
    sys.exit(app.exec_())