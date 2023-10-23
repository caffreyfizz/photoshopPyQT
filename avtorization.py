import sys
import hashlib
import sqlite3
from random import choice, shuffle
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtWidgets

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    


class Registration(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('avtorization.ui', self)
        
        db_name = "users.sqlite"
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

        self.salt_for_password = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

        self.registration_btn.clicked.connect(self.add_info)
    
    def add_info(self):
        if self.loginEdit.text() and self.passwordEdit.text():
            logins = self.cur.execute(f"""SELECT id FROM logins_and_passwords WHERE login = ?""", (self.loginEdit.text(),)).fetchall()
            if logins:
                self.errorLable.setText("Такой логин уже существует")
                return
            
            salt = shuffle([choice(self.salt_for_password) for _ in range(5)])
            hashed_password = hashlib.sha1(f"{self.passwordEdit.text() + salt}".encode())
            params = (self.loginEdit.text(), hashed_password.hexdigest(), "abc")
            self.cur.execute(f"""INSERT INTO logins_and_passwords ('login', 'password', 'salt')
                                          VALUES (?, ?, ?)""", params).fetchall()
            self.errorLable.setText("Добро пожаловать!")
            self.con.commit()  
            self.close()
        else:
            self.errorLable.setText("Вы не ввели логин или пароль")
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = Registration()
    plan.show()
    sys.exit(app.exec_())
