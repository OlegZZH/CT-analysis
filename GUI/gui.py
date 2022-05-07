import os
import sys

import cv2
import ffmpeg
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QFrame, QFileDialog
from tensorflow import keras

from GUI.perfectGUI import Ui_CT_main_win
from GUI.qtimeline import VideoSample
from GUI.settings import Ui_Settings_win
import pydicom


class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_CT_main_win()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.openFile)
        self.ui.pushButton_3.clicked.connect(self.play)
        self.ui.actionOpen.triggered.connect(self.openFile)
        self.ui.actionSettings.triggered.connect(lambda: self.Settings_win.show())
        self.ui.actionClose.triggered.connect(self.close)
        self.ui.actionClose_File.triggered.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.select))
        self.ui.pushButton_2.clicked.connect(self.cutVideo)
        self.ui.pushButton_4.clicked.connect(self.learn)
        self.ui.pushButton_5.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.select))
        self.ui.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.ui.mediaPlayer.setNotifyInterval(30)

        self.frame_bin = []
        self.video = []
        self.frames = []

        self.model_loaded = None
        self.open_settings(False)

    def openFile(self):

        self.fileName, _ = QFileDialog.getOpenFileNames(self, "Open Movie", "", "Images (*.png *.jpg);;Video (*.mp4);;Dicom (*.dcm)")
        if len(self.fileName) > 1:
            print(self.fileName)
            frames=[]
            out = cv2.VideoWriter(r'Temp\comp_video.mp4', cv2.VideoWriter_fourcc(*'h263'), 10,(512, 512))
            for i in self.fileName:
                name=os.path.basename(i)
                n, e = os.path.splitext(name)
                if e==".jpg" or e==".png":
                    img = cv2.imread(i)
                    img = cv2.resize(img, (512,512))
                    out.write(img)
                if e==".mp4":
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
                if e==".dcm":
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
            for i in image_2d_scaled :
                out.write(i)

            out.release()
            self.fileName="Temp\comp_video.mp4"
        elif len(self.fileName) == 1 :
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
        if self.ui.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.ui.mediaPlayer.pause()
        else:
            self.ui.mediaPlayer.play()

    def exitCall(self):
        sys.exit(app.exec_())

    def positionChanged(self, position):

        x = self.ui.qtimeline.x()
        self.ui.qtimeline.pointerPos = x
        self.ui.qtimeline.positionChanged.emit(x)

        self.ui.qtimeline.pointerTimePos = position / 1000
        self.ui.qtimeline.checkSelection(x)
        self.ui.qtimeline.update()
        # self.ui.qtimeline.clicking = True

    def setPosition(self, position):
        self.ui.mediaPlayer.setPosition(position)

    def mousePressEvent(self, e):
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

        if e.button() == Qt.LeftButton:
            self.ui.mediaPlayer.setPosition(int(self.ui.qtimeline.pointerTimePos * 1000))
            self.ui.qtimeline.clicking = False

    def handleError(self):
        self.ui.pushButton_3.setEnabled(False)
        self.ui.label_2.setText("Error: " + self.ui.mediaPlayer.errorString())

    def video_to_pixmap(self, fileName):

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

    def open_settings(self, show=True):
        self.Settings_win = QtWidgets.QMainWindow()

        File = open("Theme/ElegantDark.qss", 'r')
        with File:
            qss = File.read()
            app.setStyleSheet(qss)

        self.ui_settings = Ui_Settings_win()
        self.ui_settings.setupUi(self.Settings_win)
        self.ui_settings.doubleSpinBox_Blur.valueChanged.connect(self.draw_preview)
        self.ui_settings.spinBox_thresholdValue.valueChanged.connect(self.draw_preview)

        self.Settings_win.closeEvent = lambda e: self.Settings_win.hide()

        self.draw_preview()

        if show:
            self.show_set(self.Settings_win)

    def draw_preview(self):
        if len(self.frames) == 0:
            im = cv2.imread('Icon/PngItem_320012.png')

        else:
            im = self.frames[int(len(self.frames) / 2)]

        im = cv2.resize(im, (256, 256), interpolation=cv2.INTER_AREA)
        im = im[:-40, :]

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

    def show_set(self, win):
        win.show()

    def cutVideo(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.cheking)

        cut_start, cut_end = self.ui.range_slider.value()

        out, _ = (
            ffmpeg
                .input(self.fileName)
                .trim(start_frame=int(cut_start / 100 * self.frame_count),
                      end_frame=int(cut_end / 100 * self.frame_count))
                .setpts('PTS-STARTPTS')
                .filter('scale', 256, 256)
                .output('pipe:', format='rawvideo', pix_fmt='rgb24')
                .run(capture_stdout=True)
        )
        self.video = (
            np
                .frombuffer(out, np.uint8)
                .reshape([-1, 256, 256, 3])
        )

        for i in self.video:
            im_g = i[:-40, :]
            im_g = cv2.cvtColor(im_g, cv2.COLOR_RGB2GRAY)

            im_g = cv2.GaussianBlur(im_g, (
                int(self.ui_settings.doubleSpinBox_Blur.value()), int(self.ui_settings.doubleSpinBox_Blur.value())), 5,
                                    cv2.BORDER_DEFAULT)

            ret, thresh1 = cv2.threshold(im_g, int(self.ui_settings.spinBox_thresholdValue.value()), 255,
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
        self.model_loaded = keras.models.load_model(os.path.abspath('../') + r"\DNN\lung_model15000_25000V2")
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



app = QtWidgets.QApplication([])
application = mywindow()
File = open("Theme/ElegantDark.qss", 'r')
with File:
    qss = File.read()
    app.setStyleSheet(qss)
application.show()

sys.exit(app.exec())
