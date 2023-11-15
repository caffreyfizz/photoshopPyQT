import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt5 import QtCore, QtWidgets


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    


class SaveFile(QDialog):
    def __init__(self, label, login):
        super().__init__()
        uic.loadUi('save_dialog.ui', self)
        self.setWindowTitle("Сохранить")

        self.picture = label
        self.login = login

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

        db_name = "users.sqlite"
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        
        self.save_as_btn.clicked.connect(self.save_as)
        self.save_cloud_btn.clicked.connect(self.save_cloud)
        self.save_as_btn.setStyleSheet(style_for_btn)
        self.save_cloud_btn.setStyleSheet(style_for_btn)

    def get_bytes_image(*pixmapLabel):
        pixmap_img = pixmapLabel[-1]
        ba = QtCore.QByteArray()
        buff = QtCore.QBuffer(ba)
        buff.open(QtCore.QIODevice.WriteOnly) 
        ok = pixmap_img.save(buff, "PNG")
        pixmap_bytes = ba.data()
        return pixmap_bytes

    def save_as(self):
        file_name = QFileDialog.getSaveFileName(self, "Сохранение картинки", "result", "*.png")[0]
        if not file_name:
            return

        self.picture.pixmap().save(file_name)
        self.close()

    def save_cloud(self):
        self.img_from_label = self.picture.pixmap()
        pixmap_bytes = self.get_bytes_image(self.img_from_label)
        user = self.cur.execute("""SELECT id from logins WHERE login = ?""", (self.login,)).fetchall()
        
        self.cur.execute(f"""INSERT INTO images(name, user) VALUES (?, ?)""", (pixmap_bytes, user[0][0])).fetchall()
        self.con.commit()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = SaveFile()
    plan.show()
    sys.exit(app.exec_())