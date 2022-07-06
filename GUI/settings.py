
# Опис мудуля settings.py
# Form implementation generated from reading ui file 'settings.ui'
# Created by: PyQt5 UI code generator 5.15.4
#



from PyQt5 import QtCore, QtGui, QtWidgets

# Клас з описом обєктів вікна налаштувань
class Ui_Settings_win(object):

    def setupUi(self, Settings_win):
        """
        Ініціалізація обєктів вікна
        :param CT_main_win: Вікно
        :return:
        """
        Settings_win.setObjectName("Settings_win")
        Settings_win.resize(410, 220)
        Settings_win.setWindowIcon(QtGui.QIcon('Icon/setting_ico.png'))
        self.centralwidget = QtWidgets.QWidget(Settings_win)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.doubleSpinBox_Blur = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_Blur.setProperty("value", 1.0)
        self.doubleSpinBox_Blur.setObjectName("doubleSpinBox_Blur")
        self.gridLayout.addWidget(self.doubleSpinBox_Blur, 0, 1, 1, 1)
        self.doubleSpinBox_Blur.setValue(5.0)
        self.doubleSpinBox_Blur.setSingleStep(2)
        self.doubleSpinBox_Blur.setMinimum(1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.spinBox_thresholdValue = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_thresholdValue.setMaximum(255)
        self.spinBox_thresholdValue.setProperty("value", 50)
        self.spinBox_thresholdValue.setObjectName("spinBox_thresholdValue")
        self.gridLayout.addWidget(self.spinBox_thresholdValue, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.settings_pixmap = QtWidgets.QLabel(self.centralwidget)
        self.settings_pixmap.setObjectName("settings_pixmap")
        self.horizontalLayout.addWidget(self.settings_pixmap)
        self.settings_pixmap_ori = QtWidgets.QLabel(self.centralwidget)
        self.settings_pixmap_ori.setObjectName("settings_pixmap_ori")
        self.horizontalLayout.addWidget(self.settings_pixmap_ori)

        self.horizontalLayout.setStretch(1, 3)
        Settings_win.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Settings_win)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 821, 21))
        self.menubar.setObjectName("menubar")
        Settings_win.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Settings_win)
        self.statusbar.setObjectName("statusbar")
        Settings_win.setStatusBar(self.statusbar)

        self.retranslateUi(Settings_win)
        QtCore.QMetaObject.connectSlotsByName(Settings_win)

    def retranslateUi(self, Settings_win):
        _translate = QtCore.QCoreApplication.translate
        Settings_win.setWindowTitle(_translate("Settings_win", "Settings"))
        self.label_2.setText(_translate("Settings_win", "G Blur "))
        self.label_3.setText(_translate("Settings_win", "thresholdValue"))
        self.settings_pixmap.setText(_translate("Settings_win", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Settings_win = QtWidgets.QMainWindow()
    File = open("Theme/Darkeum.qss", 'r')
    with File:
        qss = File.read()
        app.setStyleSheet(qss)

    ui = Ui_Settings_win()
    ui.setupUi(Settings_win)
    Settings_win.show()
    sys.exit(app.exec_())
