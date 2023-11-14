import sys
import sqlite3
import hashlib
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtWidgets
from main_menu import MainWindow


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Registration(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('reg.ui', self)
        self.setWindowTitle("Регистрация")
        self.setStyleSheet('.QWidget {background-image: url(background2.jpg);}')
        
        db_name = "users.sqlite"
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.reg_btn.clicked.connect(self.reg)

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
        style_for_edit = """
QLineEdit {
    font: 12pt "Rockwell Condensend";
    background-color: #83cbc1;
    border-radius: 15px;
    border: 2px solid rgb(55, 55, 55);
    padding-left: 10px;
    padding-right: 10px;
}
"""
        self.nameEdit.setStyleSheet(style_for_edit)
        self.mailEdit.setStyleSheet(style_for_edit)
        self.passwordEdit.setStyleSheet(style_for_edit)
        self.reg_btn.setStyleSheet(style_for_btn)
        self.errorLabel.setStyleSheet("color: rgb(235, 63, 59)")

    def reg(self):
        if self.nameEdit.text() and self.passwordEdit.text():
            logins = self.cur.execute(f"""SELECT id FROM logins WHERE login = ?""", (self.nameEdit.text(),)).fetchall()
            if logins:
                self.errorLabel.setText("Такой логин уже существует")
                return
            
            hashed_password = hashlib.sha1(f"{self.passwordEdit.text()}".encode())
            params = (self.nameEdit.text(), hashed_password.hexdigest(), self.mailEdit.text())
            self.cur.execute(f"""INSERT INTO logins ('login', 'password', 'mail')
                                          VALUES (?, ?, ?)""", params).fetchall()
            self.con.commit()
            self.main_win = MainWindow(self.nameEdit.text())
            self.main_win.show()
            self.close()
        else:
            self.errorLabel.setText("Вы не ввели логин или пароль")
            return
    
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = Registration()
    plan.show()
    sys.exit(app.exec_())
 