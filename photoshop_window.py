import sys
from os import remove
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
import io

from PIL import Image, ImageFilter, ImageEnhance


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    


class Photoshop(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('photoshop.ui', self)

        self.filters = []
        
        self.curr_image = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        self.pix_map = QPixmap(self.curr_image)
        scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
        self.imgLabel.setPixmap(scaled)

        self.blur_btn.clicked.connect(self.blur)
        self.circuit_btn.clicked.connect(self.circuit)
        self.detailing_btn.clicked.connect(self.detailing)
        self.bright_warm_btn.clicked.connect(self.bright_warm)
        self.bright_btn.clicked.connect(self.bright)
        self.chill_btn.clicked.connect(self.chill)
        self.blackwhite_btn.clicked.connect(self.blackwhite)
        self.save_btn.clicked.connect(self.save)
        
        self.lightSlider.setMinimum(0)
        self.lightSlider.setMaximum(50)
        self.lightSlider.setValue(25)
        self.lightSlider.valueChanged.connect(lambda: self.light(self.lightSlider.value(), after_filter=False))
        self.past_value = 25
    
    def get_bytes_image(*pixmapLabel):
        pixmap_img = pixmapLabel[-1]
        ba = QtCore.QByteArray()
        buff = QtCore.QBuffer(ba)
        buff.open(QtCore.QIODevice.WriteOnly) 
        ok = pixmap_img.save(buff, "PNG")
        pixmap_bytes = ba.data()
        return pixmap_bytes

    def blur(self):

        if self.blur_btn.isChecked():
            self.img_from_label = self.imgLabel.pixmap()
            pixmap_bytes = self.get_bytes_image(self.img_from_label)
            with Image.open(io.BytesIO(pixmap_bytes)) as image:
        
                blur_image = image.filter(ImageFilter.BLUR)
                blur_image.save("blur.png")
                self.pix_map = QPixmap("blur.png")
                scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)

                self.imgLabel.setPixmap(scaled)
            if "blur" not in self.filters:
                self.filters.append("blur")
            remove("blur.png")
        else:
            self.filters.remove("blur")
            self.pix_map = QPixmap(self.curr_image)
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(scaled)
            
            for img_filter in self.filters:
                filter_for_img = getattr(Photoshop, img_filter)
                if img_filter == "light":
                    filter_for_img(self, self.lightSlider.value(), after_filter=True)
                else:
                    filter_for_img(self)

    def circuit(self):
        if self.circuit_btn.isChecked():
            self.img_from_label = self.imgLabel.pixmap()
            pixmap_bytes = self.get_bytes_image(self.img_from_label)
            with Image.open(io.BytesIO(pixmap_bytes)) as image:
        
                circuit_image = image.filter(ImageFilter.CONTOUR)
                circuit_image.save("circuit.png")
                self.pix_map = QPixmap("circuit.png")
                scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)

                self.imgLabel.setPixmap(scaled)
            if "circuit" not in self.filters:
                self.filters.append("circuit")
            remove("circuit.png")
        else:
            self.filters.remove("circuit")
            self.pix_map = QPixmap(self.curr_image)
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(scaled)
            
            for img_filter in self.filters:
                filter_for_img = getattr(Photoshop, img_filter)
                if img_filter == "light":
                    filter_for_img(self, self.lightSlider.value(), after_filter=True)
                else:
                    filter_for_img(self)

    def detailing(self):
        if self.detailing_btn.isChecked():
            self.img_from_label = self.imgLabel.pixmap()
            pixmap_bytes = self.get_bytes_image(self.img_from_label)
            with Image.open(io.BytesIO(pixmap_bytes)) as image:
        
                detailing_image = image.filter(ImageFilter.DETAIL)
                detailing_image.save("detailing.png")
                self.pix_map = QPixmap("detailing.png")
                scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)

                self.imgLabel.setPixmap(scaled)
            if "detailing" not in self.filters:
                self.filters.append("detailing")
            remove("detailing.png")
        else:
            self.filters.remove("detailing")
            self.pix_map = QPixmap(self.curr_image)
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(scaled)
            
            for img_filter in self.filters:
                filter_for_img = getattr(Photoshop, img_filter)
                if img_filter == "light":
                    filter_for_img(self, self.lightSlider.value(), after_filter=True)
                else:
                    filter_for_img(self)

    def bright_warm(self):
        if self.bright_warm_btn.isChecked():
            self.img_from_label = self.imgLabel.pixmap()
            pixmap_bytes = self.get_bytes_image(self.img_from_label)
            with Image.open(io.BytesIO(pixmap_bytes)) as image:
                image = image.convert("RGB")
                x, y = image.size
                pixels = image.load()
                for i in range(x):
                    for j in range(y):
                        r, g, b = pixels[i, j]
                        pixels[i, j] = r + 50, g + 12, b
                image.save("bright_warm.png")
                self.pix_map = QPixmap("bright_warm.png")
                scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)

                self.imgLabel.setPixmap(scaled)
            if "bright_warm" not in self.filters:
                self.filters.append("bright_warm")
            remove("bright_warm.png")
        else:
            self.filters.remove("bright_warm")
            self.pix_map = QPixmap(self.curr_image)
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(scaled)
            
            for img_filter in self.filters:
                filter_for_img = getattr(Photoshop, img_filter)
                if img_filter == "light":
                    filter_for_img(self, self.lightSlider.value(), after_filter=True)
                else:
                    filter_for_img(self)

    def bright(self):
        if self.bright_btn.isChecked():
            self.img_from_label = self.imgLabel.pixmap()
            pixmap_bytes = self.get_bytes_image(self.img_from_label)
            with Image.open(io.BytesIO(pixmap_bytes)) as image:
                image = image.convert("RGB")
                x, y = image.size
                pixels = image.load()
                for i in range(x):
                    for j in range(y):
                        r, g, b = pixels[i, j]
                        pixels[i, j] = r + 18, g + 25, b
                image.save("bright.png")
                self.pix_map = QPixmap("bright.png")
                scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)

                self.imgLabel.setPixmap(scaled)
            if "bright" not in self.filters:
                self.filters.append("bright")
            remove("bright.png")
        else:
            self.filters.remove("bright")
            self.pix_map = QPixmap(self.curr_image)
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(scaled)
            
            for img_filter in self.filters:
                filter_for_img = getattr(Photoshop, img_filter)
                if img_filter == "light":
                    filter_for_img(self, self.lightSlider.value(), after_filter=True)
                else:
                    filter_for_img(self)

    def chill(self):
        if self.chill_btn.isChecked():
            self.img_from_label = self.imgLabel.pixmap()
            pixmap_bytes = self.get_bytes_image(self.img_from_label)
            with Image.open(io.BytesIO(pixmap_bytes)) as image:
                image = image.convert("RGB")
                x, y = image.size
                pixels = image.load()
                for i in range(x):
                    for j in range(y):
                        r, g, b = pixels[i, j]
                        pixels[i, j] = r, g + 10, b + 35
                image.save("chill.png")
                self.pix_map = QPixmap("chill.png")
                scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)

                self.imgLabel.setPixmap(scaled)
            if "chill" not in self.filters:
                self.filters.append("chill")
            remove("chill.png")
        else:
            self.filters.remove("chill")
            self.pix_map = QPixmap(self.curr_image)
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(scaled)
            
            for img_filter in self.filters:
                filter_for_img = getattr(Photoshop, img_filter)
                if img_filter == "light":
                    filter_for_img(self, self.lightSlider.value(), after_filter=True)
                else:
                    filter_for_img(self)

    def blackwhite(self):
        if self.blackwhite_btn.isChecked():
            self.img_from_label = self.imgLabel.pixmap()
            pixmap_bytes = self.get_bytes_image(self.img_from_label)
            with Image.open(io.BytesIO(pixmap_bytes)) as image:
                image = image.convert("RGB")
                x, y = image.size
                pixels = image.load()
                for i in range(x):
                    for j in range(y):
                        r, g, b = pixels[i, j]
                        bw = (r + g + b) // 3
                        pixels[i, j] = bw, bw, bw
                image.save("blackwhite.png")
                self.pix_map = QPixmap("blackwhite.png")
                scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)

                self.imgLabel.setPixmap(scaled)
            if "blackwhite" not in self.filters:
                self.filters.append("blackwhite")
            remove("blackwhite.png")
        else:
            self.filters.remove("blackwhite")
            self.pix_map = QPixmap(self.curr_image)
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(scaled)
            
            for img_filter in self.filters:
                filter_for_img = getattr(Photoshop, img_filter)
                if img_filter == "light":
                    filter_for_img(self, self.lightSlider.value(), after_filter=True)
                else:
                    filter_for_img(self)

    def light(self, value, after_filter=False):
        step = (value - 25) / 50
        if self.past_value > value and value < 25:
            step = step
        elif self.past_value < value and value < 25:
            step = (value - 25) / 50 - abs((self.past_value - 25) / 50)
        elif self.past_value > value and value > 25:
            step = (value - 25) / 50 - (self.past_value - 25) / 50
        elif self.past_value < value and value > 25:
            step = step
        self.past_value = value
        pixmap_bytes = self.get_bytes_image(QPixmap(self.curr_image))
        with Image.open(io.BytesIO(pixmap_bytes)) as image:
            enhancer = ImageEnhance.Brightness(image)
            im_output = enhancer.enhance(1 + step)
            im_output.save('light.png')

            self.pix_map = QPixmap("light.png")
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)

            self.imgLabel.setPixmap(scaled)
        if "light" not in self.filters:
            self.filters.append("light")
        remove("light.png")
   
    def save(self):
        pass
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = Photoshop()
    plan.show()
    sys.exit(app.exec_())