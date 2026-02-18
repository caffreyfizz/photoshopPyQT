import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtWidgets


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    


class Share(QMainWindow):
    def __init__(self, img):
        super().__init__()
        uic.loadUi('share.ui', self)
        self.setWindowTitle("Поделиться")
        self.errorLabel.setStyleSheet("color: rgb(235, 63, 59)")

        db_name = "users.sqlite"
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

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

        self.img = img

        self.share_btn.clicked.connect(self.mail_to_user)
        self.share_btn.setStyleSheet(style_for_btn)

    def mail_to_user(self):
        user = self.cur.execute("""SELECT id from logins WHERE login = ?""", (self.username.text(),)).fetchall()
        if not user:
            self.errorLabel.setText("Такого пользователя не существует")
        else:
            self.cur.execute(f"""INSERT INTO images(name, user) VALUES (?, ?)""", (self.img, user[0][0])).fetchall()
            self.con.commit()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = Share()
    plan.show()
    sys.exit(app.exec_())  