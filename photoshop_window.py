import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
import io

from PIL import Image, ImageFilter, ImageEnhance
from save_win import SaveFile
from share_window import Share


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    


class Photoshop(QMainWindow):
    def __init__(self, login, *args):
        super().__init__()
        uic.loadUi('photoshop.ui', self)
        self.setWindowTitle("Редактирование")
        self.setStyleSheet('.QWidget {background-image: url(background.jpg);}')

        self.login = login
        self.args = args

        self.filters = []
        self.sliders = {"light": self.lightSlider,
                         "contrast": self.contrastSlider,
                         "sharpness": self.sharpnessSlider,
                         "transparency": self.transparencySlider}
        
        self.coordsLabel.setText("Координаты: None, None")
        self.setMouseTracking(True)
        if not self.args:
            self.curr_image = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
            self.pix_map = QPixmap(self.curr_image)
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(scaled)
        if self.args:
            with Image.open(args[0]) as image:
                image.save("icon.png")
                self.pix_map = QPixmap("icon.png")
                scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
                self.imgLabel.setPixmap(scaled)
            os.remove("icon.png")

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
        self.lightSlider.valueChanged.connect(self.light)

        self.contrastSlider.setMinimum(0)
        self.contrastSlider.setMaximum(50)
        self.contrastSlider.setValue(25)
        self.contrastSlider.valueChanged.connect(self.contrast)

        self.sharpnessSlider.setMinimum(0)
        self.sharpnessSlider.setMaximum(50)
        self.sharpnessSlider.setValue(25)
        self.sharpnessSlider.valueChanged.connect(self.sharpness)

        self.transparencySlider.setMinimum(0)
        self.transparencySlider.setMaximum(30)
        self.transparencySlider.setValue(30)
        self.transparencySlider.valueChanged.connect(self.transparency)

        self.save_btn.clicked.connect(self.save)
        self.share_btn.clicked.connect(self.share)

        style_for_imgLabel = """QLabel {
    background-image: url(background.jpg);
    color: #fff;
    border: 2px solid #fff;
    border-radius: 8px;
    padding: 2px;
    outline: none;
}
"""

        style_for_slider = """
            QSlider{
                background: #E3DEE2;
            }
            QSlider::groove:horizontal {  
                height: 10px;
                margin: 0px;
                border-radius: 5px;
                background: #B0AEB1;
            }
            QSlider::handle:horizontal {
                background: #fff;
                border: 1px solid #E3DEE2;
                width: 17px;
                margin: -5px 0; 
                border-radius: 8px;
            }
            QSlider::sub-page:qlineargradient {
                background: #3B99FC;
                border-radius: 5px;
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
        self.transparencySlider.setStyleSheet(style_for_slider)
        self.sharpnessSlider.setStyleSheet(style_for_slider)
        self.contrastSlider.setStyleSheet(style_for_slider)
        self.lightSlider.setStyleSheet(style_for_slider)
        self.save_btn.setStyleSheet(style_for_btn)
        self.share_btn.setStyleSheet(style_for_btn)
        self.imgLabel.setStyleSheet(style_for_imgLabel)

        
    
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
            os.remove("blur.png")
        else:
            self.filters.remove("blur")
            if self.args:
                with Image.open(self.args[0]) as image:
                    image.save("null_img.png")
                    self.pix_map = QPixmap("null_img.png")
                os.remove("null_img.png")
            else:
                self.pix_map = QPixmap(self.curr_image)
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(scaled)

            for img_filter, slider in self.sliders.items():
                if img_filter not in self.filters:
                    continue
                filter_for_img = getattr(Photoshop, img_filter)
                filter_for_img(self, slider.value())
            
            for img_filter in self.filters:
                filter_for_img = getattr(Photoshop, img_filter)
                if img_filter in self.sliders.keys():
                    continue
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
            os.remove("circuit.png")
        else:
            self.filters.remove("circuit")
            if self.args:
                with Image.open(self.args[0]) as image:
                    image.save("null_img.png")
                    self.pix_map = QPixmap("null_img.png")
                os.remove("null_img.png")
            else:
                self.pix_map = QPixmap(self.curr_image)
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(scaled)
            
            for img_filter, slider in self.sliders.items():
                if img_filter not in self.filters:
                    continue
                filter_for_img = getattr(Photoshop, img_filter)
                filter_for_img(self, slider.value())
            
            for img_filter in self.filters:
                filter_for_img = getattr(Photoshop, img_filter)
                if img_filter in self.sliders.keys():
                    continue
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
            os.remove("detailing.png")
        else:
            self.filters.remove("detailing")
            if self.args:
                with Image.open(self.args[0]) as image:
                    image.save("null_img.png")
                    self.pix_map = QPixmap("null_img.png")
                os.remove("null_img.png")
            else:
                self.pix_map = QPixmap(self.curr_image)
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(scaled)
            
            for img_filter, slider in self.sliders.items():
                if img_filter not in self.filters:
                    continue
                filter_for_img = getattr(Photoshop, img_filter)
                filter_for_img(self, slider.value())
            
            for img_filter in self.filters:
                filter_for_img = getattr(Photoshop, img_filter)
                if img_filter in self.sliders.keys():
                    continue
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
            os.remove("bright_warm.png")
        else:
            self.filters.remove("bright_warm")
            if self.args:
                with Image.open(self.args[0]) as image:
                    image.save("null_img.png")
                    self.pix_map = QPixmap("null_img.png")
                os.remove("null_img.png")
            else:
                self.pix_map = QPixmap(self.curr_image)
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(scaled)
            
            for img_filter, slider in self.sliders.items():
                if img_filter not in self.filters:
                    continue
                filter_for_img = getattr(Photoshop, img_filter)
                filter_for_img(self, slider.value())
            
            for img_filter in self.filters:
                filter_for_img = getattr(Photoshop, img_filter)
                if img_filter in self.sliders.keys():
                    continue
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
            os.remove("bright.png")
        else:
            self.filters.remove("bright")
            if self.args:
                with Image.open(self.args[0]) as image:
                    image.save("null_img.png")
                    self.pix_map = QPixmap("null_img.png")
                os.remove("null_img.png")
            else:
                self.pix_map = QPixmap(self.curr_image)
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(scaled)
            
            for img_filter, slider in self.sliders.items():
                if img_filter not in self.filters:
                    continue
                filter_for_img = getattr(Photoshop, img_filter)
                filter_for_img(self, slider.value())
            
            for img_filter in self.filters:
                filter_for_img = getattr(Photoshop, img_filter)
                if img_filter in self.sliders.keys():
                    continue
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
            os.remove("chill.png")
        else:
            self.filters.remove("chill")
            if self.args:
                with Image.open(self.args[0]) as image:
                    image.save("null_img.png")
                    self.pix_map = QPixmap("null_img.png")
                os.remove("null_img.png")
            else:
                self.pix_map = QPixmap(self.curr_image)
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(scaled)
            
            for img_filter, slider in self.sliders.items():
                if img_filter not in self.filters:
                    continue
                filter_for_img = getattr(Photoshop, img_filter)
                filter_for_img(self, slider.value())
            
            for img_filter in self.filters:
                filter_for_img = getattr(Photoshop, img_filter)
                if img_filter in self.sliders.keys():
                    continue
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
            os.remove("blackwhite.png")
        else:
            self.filters.remove("blackwhite")
            if self.args:
                with Image.open(self.args[0]) as image:
                    image.save("null_img.png")
                    self.pix_map = QPixmap("null_img.png")
                os.remove("null_img.png")
            else:
                self.pix_map = QPixmap(self.curr_image)
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(scaled)
            
            for img_filter, slider in self.sliders.items():
                if img_filter not in self.filters:
                    continue
                filter_for_img = getattr(Photoshop, img_filter)
                filter_for_img(self, slider.value())
            
            for img_filter in self.filters:
                filter_for_img = getattr(Photoshop, img_filter)
                if img_filter in self.sliders.keys():
                    continue
                else:
                    filter_for_img(self)

    def light(self, value):
        step = (value - 25) / 40
        if not self.args:
            pixmap_bytes = self.get_bytes_image(QPixmap(self.curr_image))
            img_for_label = io.BytesIO(pixmap_bytes)
        else:
            img_for_label = self.args[0]
            
        with Image.open(img_for_label) as image:
            enhancer = ImageEnhance.Brightness(image)
            im_output = enhancer.enhance(1 + step)
            im_output.save('light.png')

            self.pix_map = QPixmap("light.png")
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)

            self.imgLabel.setPixmap(scaled)
        if "light" not in self.filters:
            self.filters.append("light")
        os.remove("light.png")

    def contrast(self, value):
        step = (value - 25) / 35
        if not self.args:
            pixmap_bytes = self.get_bytes_image(QPixmap(self.curr_image))
            img_for_label = io.BytesIO(pixmap_bytes)
        else:
            img_for_label = self.args[0]
        
        with Image.open(img_for_label) as image:
            enhancer = ImageEnhance.Contrast(image)
            im_output = enhancer.enhance(1 + step)
            im_output.save('contrast.png')

            self.pix_map = QPixmap("contrast.png")
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)

            self.imgLabel.setPixmap(scaled)
        if "contrast" not in self.filters:
            self.filters.append("contrast")
        os.remove("contrast.png")

    def sharpness(self, value):
        step = (value - 25) / 7
        if not self.args:
            pixmap_bytes = self.get_bytes_image(QPixmap(self.curr_image))
            img_for_label = io.BytesIO(pixmap_bytes)
        else:
            img_for_label = self.args[0]
        
        with Image.open(img_for_label) as image:
            enhancer = ImageEnhance.Sharpness(image)
            im_output = enhancer.enhance(1 + step)
            im_output.save('sharpness.png')

            self.pix_map = QPixmap("sharpness.png")
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)

            self.imgLabel.setPixmap(scaled)
        if "sharpness" not in self.filters:
            self.filters.append("sharpness")
        os.remove("sharpness.png")

    def transparency(self, value):
        if not self.args:
            pixmap_bytes = self.get_bytes_image(QPixmap(self.curr_image))
            img_for_label = io.BytesIO(pixmap_bytes)
        else:
            img_for_label = self.args[0]
        
        with Image.open(img_for_label) as image:
            im_output = image.convert("RGBA")
            im_output.putalpha(value * 8)
            im_output.save("transparency.png")
            
            self.pix_map = QPixmap("transparency.png")
            scaled = self.pix_map.scaled(self.imgLabel.size(), QtCore.Qt.KeepAspectRatio)

            self.imgLabel.setPixmap(scaled)
        if "transparency" not in self.filters:
            self.filters.append("transparency")
        os.remove("transparency.png")

    def mouseMoveEvent(self, event):
        self.coordsLabel.setText(f"Координаты: {event.x()}, {event.y()}")
   
    def save(self):
        self.save_dialog = SaveFile(self.imgLabel, self.login)
        self.save_dialog.show()

    def share(self):
        self.img_from_label = self.imgLabel.pixmap()
        pixmap_bytes = self.get_bytes_image(self.img_from_label)
        self.share = Share(pixmap_bytes)
        self.share.show()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plan = Photoshop()
    plan.show()
    sys.exit(app.exec_())