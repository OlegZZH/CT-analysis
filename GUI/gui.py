# Опис модуля gui.py
import os
import sys

import cv2
import ffmpeg
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QFrame, QFileDialog
from tensorflow import keras

from perfectGUI import Ui_CT_main_win
from qtimeline import VideoSample
from settings import Ui_Settings_win
import pydicom


# Головний клас який збирає в себе весь функціонал програми
class MediaPlayer(QtWidgets.QWidget):

    def openFile(self):
        """
        Метод відповідає за відкриття файлу. Якщо файлів декілька вони будуть склені в один
        :return:
        """

        self.fileName, _ = QFileDialog.getOpenFileNames(self, "Open Movie", "",
                                                        "Images (*.png *.jpg);;Video (*.mp4);;Dicom (*.dcm)")
        if len(self.fileName) > 1:
            print(self.fileName)
            frames = []
            out = cv2.VideoWriter(r'Temp\comp_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (512, 512))
            for i in self.fileName:
                name = os.path.basename(i)
                n, e = os.path.splitext(name)
                if e == ".jpg" or e == ".png" or e == ".PNG" or e == ".JPG":
                    img = cv2.imdecode(np.fromfile(i, dtype=np.uint8), cv2.IMREAD_COLOR)
                    img = cv2.resize(img, (512, 512))
                    out.write(img)
                if e == ".mp4":
                    cap = cv2.VideoCapture(i)
                    r = True
                    while r:
                        r, img = cap.read()
                        if r:
                            img = cv2.resize(img, (512, 512))
                            out.write(img)
                        else:
                            break
                    cap.release()
                if e == ".dcm":
                    frames.append(pydicom.dcmread(i))
            slices = []
            for f in frames:
                if hasattr(f, 'SliceLocation'):
                    slices.append(f)
            slices = sorted(slices, key=lambda s: s.SliceLocation)
            image_2d_scaled = []
            for s in slices:
                img = (s.pixel_array.astype(float))
                image_2d_scaled.append((np.maximum(img, 0) / img.max()) * 255.0)
            image_2d_scaled = np.uint8(image_2d_scaled)

            for i in image_2d_scaled[:]:
                im = cv2.cvtColor(i, cv2.COLOR_GRAY2RGB)
                out.write(im)

            out.release()
            self.fileName = "Temp\comp_video.mp4"
        elif len(self.fileName) == 1:
            self.fileName = self.fileName[0]

        self.frame_bin = []
        print(self.fileName)
        if self.fileName != []:
            self.ui.mediaPlayer.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(self.fileName)))
            self.video_to_pixmap(self.fileName)
            self.ui.label_2.setText(self.fileName)
            self.ui.stackedWidget.setCurrentWidget(self.ui.cut)
            for i in reversed(range(self.ui.cheking_grid.count())):
                self.ui.cheking_grid.itemAt(i).widget().setParent(None)

    def play(self):
        """
        Метод який починає та зупиняє відео
        :return:
        """
        if self.ui.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.ui.mediaPlayer.pause()
        else:
            self.ui.mediaPlayer.play()

    def positionChanged(self, position):
        """
        Метод для вибору часу на слайдері
        :param position: Час
        :return:
        """
        x = self.ui.qtimeline.x()
        self.ui.qtimeline.pointerPos = x
        self.ui.qtimeline.positionChanged.emit(x)

        self.ui.qtimeline.pointerTimePos = position / 1000
        self.ui.qtimeline.checkSelection(x)
        self.ui.qtimeline.update()
        # self.ui.qtimeline.clicking = True

    def setPosition(self, position):
        """
        Метод який рухає повзунок з часом
        :param position: Час
        :return:
        """
        self.ui.mediaPlayer.setPosition(position)

    def mousePressEvent(self, e):
        """
        Евент кліку миші по віджету
        :param e: Евент
        :return:
        """
        if e.button() == Qt.LeftButton:
            self.ui.mediaPlayer.pause()
            x = e.pos().x() - self.ui.pushButton_2.width() - 12
            self.ui.qtimeline.pointerPos = x
            self.ui.qtimeline.positionChanged.emit(x)
            self.ui.qtimeline.pointerTimePos = self.ui.qtimeline.pointerPos * self.ui.qtimeline.getScale()
            self.ui.qtimeline.checkSelection(x)
            self.ui.qtimeline.update()
            self.ui.qtimeline.clicking = True

    def mouseReleaseEvent(self, e):
        """
        Евент відпускання миші
        :param e: Евент
        :return:
        """
        if e.button() == Qt.LeftButton:
            self.ui.mediaPlayer.setPosition(int(self.ui.qtimeline.pointerTimePos * 1000))
            self.ui.qtimeline.clicking = False

    def handleError(self):
        """
        Обробка помилок
        :return:
        """
        self.ui.pushButton_3.setEnabled(False)
        self.ui.label_2.setText("Error: " + self.ui.mediaPlayer.errorString())

class Settings(QtWidgets.QMainWindow):
    def __init__(self):
        super(Settings, self).__init__()


        self.ui_settings = Ui_Settings_win()
        self.ui_settings.setupUi(self)


    def open_settings(self,frames, show=True):
        """
        Відкриття вікна налаштувань
        :param show: Від цого параметру залежить чи буде показуватись вікно
        :return:
        """
        self.ui_settings.doubleSpinBox_Blur.valueChanged.connect(lambda : self.draw_preview(frames))
        self.ui_settings.spinBox_thresholdValue.valueChanged.connect(lambda : self.draw_preview(frames))
        self.draw_preview(frames)

        if show:
            self.show()

    def draw_preview(self,frames):
        """
        Попередній перегляд у вікні налаштувань
        :return:
        """
        if len(frames) == 0:
            im = cv2.imread('Icon/PngItem_320012.png')

        else:
            im = frames[int(len(frames) / 2)]

        im = cv2.resize(im, (128, 128), interpolation=cv2.INTER_AREA)
        im = im[:-20, :]

        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im = cv2.GaussianBlur(im, (
            int(self.ui_settings.doubleSpinBox_Blur.value()), int(self.ui_settings.doubleSpinBox_Blur.value())), 5,
                              cv2.BORDER_DEFAULT)
        self.ui_settings.settings_pixmap_ori.setPixmap(
            QPixmap(QImage(im, im.shape[1], im.shape[0], QImage.Format_Indexed8)))
        _, im = cv2.threshold(im, int(self.ui_settings.spinBox_thresholdValue.value()), 255, cv2.THRESH_BINARY)

        im = np.array(im)

        im = np.uint8(im)

        self.ui_settings.settings_pixmap.setPixmap(
            QPixmap(QImage(im, im.shape[1], im.shape[0], QImage.Format_Indexed8)))


class mywindow(QtWidgets.QMainWindow,MediaPlayer):

    def __init__(self):

        super(mywindow, self).__init__()
        self.ui = Ui_CT_main_win()
        self.ui.setupUi(self)
        self.sett=Settings()

        self.ui.pushButton.clicked.connect(self.openFile)
        self.ui.pushButton_3.clicked.connect(self.play)
        self.ui.actionOpen.triggered.connect(self.openFile)
        self.ui.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.ui.mediaPlayer.setNotifyInterval(30)

        self.ui.actionSettings.triggered.connect(lambda: self.sett.open_settings(self.frames,True))
        self.ui.actionClose.triggered.connect(self.close)
        self.ui.actionClose_File.triggered.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.select))
        self.ui.pushButton_2.clicked.connect(self.cutVideo)
        self.ui.pushButton_4.clicked.connect(self.learn)
        self.ui.pushButton_5.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.select))

        self.frame_bin = []
        self.video = []
        self.frames = []

        self.model_loaded = None



    def video_to_pixmap(self, fileName):
        """
        Створення зображень для попереднього перегляду
        :param fileName: Назва файлу
        :return:
        """
        cap = cv2.VideoCapture(fileName)
        fps = cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frames = []
        r = True
        while r:
            r, img = cap.read(cv2.IMREAD_GRAYSCALE)
            if r:
                self.frames.append(img)
            else:
                break
        self.frames = np.array(self.frames)
        videoSample = []

        if self.frames.shape[0] > 30:
            step = self.frames.shape[0] // (self.geometry().width() // 52)
            m = self.frames.shape[0] / (self.geometry().width() // 52)
        else:
            step = 1
            m = 1
        print(self.frames.shape)
        for i in self.frames[::step]:
            im = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
            im = np.uint8(im)
            qimage = QImage(im, im.shape[0], im.shape[1], QImage.Format_Indexed8)
            videoSample.append(
                VideoSample(duration=((self.frame_count / fps) / self.frame_count) * (m), picture=QPixmap(qimage)))

        self.ui.qtimeline.duration = self.frame_count / fps
        self.ui.qtimeline.videoSamples = videoSample


    def cutVideo(self):
        """
        Цей метод обрізає відео виконує аналізує знімки та виводить їх на екран
        :return:
        """
        self.ui.stackedWidget.setCurrentWidget(self.ui.cheking)

        cut_start, cut_end = self.ui.range_slider.value()

        out, _ = (
            ffmpeg
            .input(self.fileName)
            .trim(start_frame=int(cut_start / 100 * self.frame_count),
                  end_frame=int(cut_end / 100 * self.frame_count))
            .setpts('PTS-STARTPTS')
            .filter('scale', 128, 128)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run(capture_stdout=True)
        )
        self.video = (
            np
            .frombuffer(out, np.uint8)
            .reshape([-1, 128, 128, 3])
        )

        for i in self.video:
            im_g = i[:-20, :]
            im_g = cv2.cvtColor(im_g, cv2.COLOR_RGB2GRAY)

            im_g = cv2.GaussianBlur(im_g, (
                int(self.sett.ui_settings.doubleSpinBox_Blur.value()), int(self.sett.ui_settings.doubleSpinBox_Blur.value())), 5,
                                    cv2.BORDER_DEFAULT)

            ret, thresh1 = cv2.threshold(im_g, int(self.sett.ui_settings.spinBox_thresholdValue.value()), 255,
                                         cv2.THRESH_BINARY)
            self.frame_bin.append(thresh1)
        self.frame_bin = np.array(self.frame_bin)
        self.dignoses = self.prediction_diagnos(self.frame_bin)

        # DRAW RESULTS

        for n, i in enumerate(self.frame_bin):
            img = QtWidgets.QLabel(self.ui.scrollAreaWidgetContents)
            img.setObjectName("IMG{0}".format(n))
            img.setStyleSheet("color: rgb(0, 0, 0);")

            self.ui.cheking_grid.addWidget(img, n, 0, 1, 1)
            im = np.uint8(i)
            qpixmap = QPixmap(QImage(im, im.shape[1], im.shape[0], QImage.Format_Indexed8))
            img.setPixmap(qpixmap)
            img.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum))

            diagnos_label = QtWidgets.QLabel(self.ui.scrollAreaWidgetContents)
            diagnos_label.setObjectName("Diagnos{}".format(n))
            diagnos_label.setFrameShape(QFrame.StyledPanel)
            font = QtGui.QFont()
            font.setPointSize(21)
            diagnos_label.setFont(font)
            if all(self.dignoses[n] == [1, 0]):
                diagnos_label.setStyleSheet("color: rgb(180, 221, 99);")
                diagnos_label.setText("Diagnos : healthy")

            elif all(self.dignoses[n] == [0, 1]):
                diagnos_label.setText("Diagnos : ill")
                diagnos_label.setStyleSheet(" color: rgb(228, 102, 102);")
            else:
                diagnos_label.setText(r"Diagnos : ¯\_(ツ)_/¯")
                diagnos_label.setStyleSheet("color: rgb(0, 0, 0);")
            self.ui.cheking_grid.addWidget(diagnos_label, n, 1, 1, 1)
            checkBox = QtWidgets.QCheckBox(self.ui.scrollAreaWidgetContents)
            checkBox.setText("Use in learning")
            checkBox.setObjectName("checkBox{}".format(n))
            checkBox.setChecked(True)
            checkBox.setStyleSheet(" color:rgb(82,82,82);")
            self.ui.cheking_grid.addWidget(checkBox, n, 2, 1, 1)

    def prediction_diagnos(self, frame):
        """
        Метод який завантажує модель та робить передбачення
        :param frame:
        :return:
        """
        self.model_loaded = keras.models.load_model(os.path.abspath('../') + r"\DNN\lung_model30000_50000")
        frame = frame / 255
        d = self.model_loaded.predict(np.expand_dims(frame, axis=3))
        d = np.around(d)
        # print(d)
        il = 1
        hl = 1
        for i in d:
            if all(i == [0, 1]):
                il += 1
            elif all(i == [1, 0]):
                hl += 1
        if il / hl >= 0.1:
            self.ui.label_3.setText("General diagnosis: ill")
        else:
            self.ui.label_3.setText("General diagnosis: healthy")
        return d

    def learn(self):
        """
        Медод який навчає модель
        :return:
        """
        use = []
        for i in range(self.ui.cheking_grid.count()):
            if isinstance(self.ui.cheking_grid.itemAt(i).widget(), QtWidgets.QCheckBox):
                use.append(self.ui.cheking_grid.itemAt(i).widget().isChecked())
        use_frame = []
        for n, i in enumerate(use):
            if i:
                use_frame.append(self.frame_bin[n])
        use_frame = np.array(use_frame)
        print(use_frame.shape)
        if self.ui.radioButton.isChecked():
            self.model_loaded.fit(np.expand_dims(use_frame, axis=3), self.dignoses, batch_size=4, epochs=3,
                                  validation_split=0.1)
            self.ui.pushButton_5.setEnabled(True)

        self.ui.stackedWidget.setCurrentWidget(self.ui.restart)
        self.ui.pushButton_5.setEnabled(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = mywindow()
    File = open("Theme/ElegantDark.qss", 'r')
    with File:
        qss = File.read()
        app.setStyleSheet(qss)
    application.show()

    sys.exit(app.exec())
