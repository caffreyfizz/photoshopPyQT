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
    def __init__(self, label):
        super().__init__()
        uic.loadUi('save_dialog.ui', self)
        self.picture = label
        
        self.save_as_btn.clicked.connect(self.save_as)
        self.save_cloud_btn.clicked.connect(self.save_cloud)

    def save_as(self):
        file_name = QFileDialog.getSaveFileName(self, "Сохранение картинки", "result", "*.png")[0]
        if not file_name:
            return

        self.picture.pixmap().save(file_name)
        self.close()

    def save_cloud(self):
        pass


        
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = SaveFile()
    plan.show()
    sys.exit(app.exec_())