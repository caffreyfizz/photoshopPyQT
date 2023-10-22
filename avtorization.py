import sys
import hashlib
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Registration(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('avtorization.ui', self)
        
        db_name = "users.sqlite"
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

        self.registration_btn.clicked.connect(self.add_info)
    
    def add_info(self):
        if self.loginEdit.text() and self.passwordEdit.text():
            logins = self.cur.execute(f"""SELECT id FROM logins_and_passwords WHERE login = ?""", (self.loginEdit.text(),)).fetchall()
            if logins:
                self.errorLable.setText("Такой логин уже существует")
                return
            
            hashed_password = hashlib.sha1(self.passwordEdit.text().encode())
            params = (self.loginEdit.text(), hashed_password.hexdigest(), "abcd")
            self.cur.execute(f"""INSERT INTO logins_and_passwords ('login', 'password', 'salt')
                                          VALUES (?, ?, ?)""", params).fetchall()
            self.errorLable.setText("Добро пожаловать!")
            self.con.commit()                      


if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = Registration()
    plan.show()
    sys.exit(app.exec_())
