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
        
        db_name = "users.sqlite"
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.reg_btn.clicked.connect(self.reg)

    def reg(self):
        if self.nameEdit.text() and self.passwordEdit.text():
            logins = self.cur.execute(f"""SELECT id FROM logins_and_passwords WHERE login = ?""", (self.nameEdit.text(),)).fetchall()
            if logins:
                self.errorLabel.setText("Такой логин уже существует")
                return
            
            #salt = shuffle([choice(self.salt_for_password) for _ in range(5)])
            hashed_password = hashlib.sha1(f"{self.passwordEdit.text()}".encode())
            params = (self.nameEdit.text(), hashed_password.hexdigest(), self.mailEdit.text())
            self.cur.execute(f"""INSERT INTO logins_and_passwords ('login', 'password', 'mail')
                                          VALUES (?, ?, ?)""", params).fetchall()
            self.errorLabel.setText("Добро пожаловать!")
            self.con.commit() 
            self.main_win = MainWindow()
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
 