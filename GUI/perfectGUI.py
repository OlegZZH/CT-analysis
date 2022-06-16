# -*- coding: utf-8 -*-
# Опис мудуля perfectGUI.py

# Form implementation generated from reading ui file 'perfectGUI.ui'



import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QSlider
from qtrangeslider import QLabeledRangeSlider

from qtimeline import QTimeLine
from settings import Ui_Settings_win




# Таблиці стилей для подвійного слайдера
QSS = """
QSlider {
    min-height: 20px;
}

QSlider::groove:horizontal {
    border: 0px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #888, stop:1 #ddd);
    height: 20px;
    border-radius: 10px;
}

QSlider::handle {
    background: qradialgradient(cx:0, cy:0, radius: 1.2, fx:0.35,
                                fy:0.3, stop:0 #eef, stop:1 #002);
    height: 20px;
    width: 20px;
    border-radius: 10px;
}

QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #227, stop:1 #77a);
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
}


"""

# Клас з описом обєктів головного вікна
class Ui_CT_main_win(object):

    def setupUi(self, CT_main_win):
        """
        Ініціалізація обєктів вікна
        :param CT_main_win: Вікно
        :return:
        """
        CT_main_win.setObjectName("CT_main_win")
        CT_main_win.resize(1280, 720)
        CT_main_win.setWindowIcon(QtGui.QIcon('Icon/PngItem_320012.png'))
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.centralwidget = QtWidgets.QWidget(CT_main_win)
        self.centralwidget.setAcceptDrops(False)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setEnabled(True)
        self.stackedWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.stackedWidget.setObjectName("stackedWidget")
        self.select = QtWidgets.QWidget()
        self.select.setObjectName("select")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.select)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.select)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.pushButton = QtWidgets.QPushButton(self.select)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(19)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.stackedWidget.addWidget(self.select)
        self.cut = QtWidgets.QWidget()
        self.cut.setObjectName("cut")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.cut)
        self.verticalLayout_4.setSpacing(9)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setObjectName("gridLayout")

        self.qtimeline = QTimeLine(24, 20)
        self.qtimeline.setObjectName("TimeLine")
        self.qtimeline.setMaximumHeight(120)

        self.gridLayout.addWidget(self.qtimeline, 1, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.cut)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 0, 1, 1)

        self.range_slider = QLabeledRangeSlider()
        self.range_slider.setOrientation(QtCore.Qt.Horizontal)
        self.range_slider.setObjectName("range_slider")
        self.range_slider.setTickPosition(QSlider.TicksBelow)
        self.range_slider.setTickInterval(5)
        self.range_slider.setMaximumHeight(120)
        self.range_slider.setStyleSheet(QSS)
        self.range_slider.setRange(0, 100)
        self.range_slider.setValue((20,55))

        self.gridLayout.addWidget(self.range_slider, 2, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.cut)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(videoWidget)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.cut)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 1, 1, 1)
        self.gridLayout.setRowStretch(0, 2)
        self.gridLayout.setRowStretch(1, 2)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.stackedWidget.addWidget(self.cut)
        self.cheking = QtWidgets.QWidget()
        self.cheking.setObjectName("cheking")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.cheking)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.scrollArea = QtWidgets.QScrollArea(self.cheking)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 168, 146))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_3.setSpacing(10)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_3.addWidget(self.pushButton_4, 4, 0, 1, 1)
        self.radioButton = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton.sizePolicy().hasHeightForWidth())
        self.radioButton.setSizePolicy(sizePolicy)
        self.radioButton.setChecked(True)
        self.radioButton.setAutoRepeat(False)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout_3.addWidget(self.radioButton, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet("color: rgb(0, 0, 0);")
        self.gridLayout_3.addWidget(self.label_3, 2, 0, 1, 1)
        self.cheking_grid = QtWidgets.QGridLayout()
        self.cheking_grid.setContentsMargins(10, 10, 10, 10)
        self.cheking_grid.setHorizontalSpacing(25)
        self.cheking_grid.setVerticalSpacing(10)
        self.cheking_grid.setObjectName("cheking_grid")

        self.cheking_grid.setColumnStretch(0, 5)
        self.gridLayout_3.addLayout(self.cheking_grid, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_5.addWidget(self.scrollArea)
        self.stackedWidget.addWidget(self.cheking)
        self.restart = QtWidgets.QWidget()
        self.restart.setObjectName("restart")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.restart)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.pushButton_5 = QtWidgets.QPushButton(self.restart)
        self.pushButton_5.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(31)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_4.addWidget(self.pushButton_5, 1, 0, 1, 2)
        self.stackedWidget.addWidget(self.restart)
        self.gridLayout_2.addWidget(self.stackedWidget, 0, 0, 1, 1)
        CT_main_win.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(CT_main_win)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 890, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        CT_main_win.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(CT_main_win)
        self.statusbar.setObjectName("statusbar")
        CT_main_win.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(CT_main_win)
        self.actionOpen.setObjectName("actionOpen")
        self.actionClose = QtWidgets.QAction(CT_main_win)
        self.actionClose.setObjectName("actionClose")
        self.actionSettings = QtWidgets.QAction(CT_main_win)
        self.actionSettings.setObjectName("actionSettings")

        self.actionClose_File = QtWidgets.QAction(CT_main_win)
        self.actionClose_File.setObjectName("actionClose_File")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionClose_File)
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.actionClose)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(CT_main_win)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CT_main_win)

    def retranslateUi(self, CT_main_win):
        _translate = QtCore.QCoreApplication.translate
        CT_main_win.setWindowTitle(_translate("CT_main_win", "CT analyzer"))
        self.label.setText(_translate("CT_main_win", "Select video image or DICOM file"))
        self.pushButton.setText(_translate("CT_main_win", "OPEN"))
        self.pushButton_2.setText(_translate("CT_main_win", "Cut"))
        self.pushButton_3.setText(_translate("CT_main_win", "   Play    "))
        self.label_2.setText(_translate("CT_main_win", "Cut out the desired segment"))
        self.pushButton_4.setText(_translate("CT_main_win", "Confirm"))
        self.radioButton.setText(_translate("CT_main_win", "Train the model"))
        self.label_3.setText(_translate("CT_main_win", "General diagnosis: "))

        self.pushButton_5.setText(_translate("CT_main_win", "Сomplete"))
        self.menuFile.setTitle(_translate("CT_main_win", "File"))
        self.actionOpen.setText(_translate("CT_main_win", "Open"))
        self.actionClose.setText(_translate("CT_main_win", "Close"))
        self.actionSettings.setText(_translate("CT_main_win", "Settings"))
        self.actionClose_File.setText(_translate("CT_main_win", "Close File"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    CT_main_win = QtWidgets.QMainWindow()
    File = open("Theme/Darkeum.qss", 'r')
    with File:
        qss = File.read()
        app.setStyleSheet(qss)
    ui = Ui_CT_main_win()
    ui.setupUi(CT_main_win)
    CT_main_win.show()
    sys.exit(app.exec_())
