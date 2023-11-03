import sys
from os import remove
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap

from PIL import Image, ImageFilter


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    


class Photoshop(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('photoshop.ui', self)
        
        self.curr_image = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        self.pix_map = QPixmap(self.curr_image)
        scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)

        self.imgLabel.setPixmap(scaled)

        self.image_pts = Image.open(self.curr_image)
        
        self.blur_btn.clicked.connect(self.blur)
        self.circuit_btn.clicked.connect(self.circuit)
        self.detailing_btn.clicked.connect(self.detailing)
        self.bright_warm_btn.clicked.connect(self.bright_warm)
        self.bright_btn.clicked.connect(self.bright)
        self.chill_btn.clicked.connect(self.chill)
        self.blackwhite_btn.clicked.connect(self.blackwhite)
        self.forward_btn.clicked.connect(self.forward)
        self.back_btn.clicked.connect(self.back)
        self.save_btn.clicked.connect(self.save)

    def blur(self):
        blur_image = self.image_pts.filter(ImageFilter.BLUR)
        blur_image.save("blur.png")
        self.image_pts = Image.open("blur.png")

        self.pix_map = QPixmap("blur.png")
        remove("blur.png")
        scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)

        self.imgLabel.setPixmap(scaled)

    def circuit(self):
        circuit_image = self.image_pts.filter(ImageFilter.CONTOUR)
        circuit_image.save("circuit.png")
        self.image_pts = Image.open("circuit.png")

        self.pix_map = QPixmap("circuit.png")
        remove("circuit.png")
        scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)

        self.imgLabel.setPixmap(scaled)

    def detailing(self):
        pass

    def bright_warm(self):
        pass

    def bright(self):
        pass

    def chill(self):
        pass

    def blackwhite(self):
        pixels = self.image_pts.load()
        x, y = self.image_pts.size

        

        """ self.image_pts.save("bw.png")

        self.pix_map = QPixmap("bw.png")
        remove("bw.png")
        scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)

        self.imgLabel.setPixmap(scaled) """

    def forward(self):
        pass

    def back(self):
        pass
    
    def save(self):
        pass
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = Photoshop()
    plan.show()
    sys.exit(app.exec_())