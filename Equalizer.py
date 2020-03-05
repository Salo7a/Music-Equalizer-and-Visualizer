# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Equalizer.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Sliders(QtWidgets.QWidget):
    def setupUi(self, Sliders):
        Sliders.setObjectName("Sliders")
        Sliders.resize(400, 300)
        self.sliders = list()
        self.widget = QtWidgets.QWidget(Sliders)
        self.widget.setGeometry(QtCore.QRect(0, 10, 391, 281))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sliders.append(QtWidgets.QSlider(self.widget))
        self.sliders[0].setMinimum(-3)
        self.sliders[0].setMaximum(3)
        self.sliders[0].setOrientation(QtCore.Qt.Vertical)
        self.sliders[0].setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sliders[0].setTickInterval(4)
        self.sliders[0].setObjectName("Slide1")
        self.horizontalLayout.addWidget(self.sliders[0])
        self.sliders.append(QtWidgets.QSlider(self.widget))
        self.sliders[1].setMinimum(-3)
        self.sliders[1].setMaximum(3)
        self.sliders[1].setOrientation(QtCore.Qt.Vertical)
        self.sliders[1].setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sliders[1].setTickInterval(4)
        self.sliders[1].setObjectName("Slide2")
        self.horizontalLayout.addWidget(self.sliders[1])
        self.sliders.append(QtWidgets.QSlider(self.widget))
        self.sliders[2].setMinimum(-3)
        self.sliders[2].setMaximum(3)
        self.sliders[2].setOrientation(QtCore.Qt.Vertical)
        self.sliders[2].setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sliders[2].setTickInterval(4)
        self.sliders[2].setObjectName("Slide3")
        self.horizontalLayout.addWidget(self.sliders[2])
        self.sliders.append(QtWidgets.QSlider(self.widget))
        self.sliders[3].setMinimum(-3)
        self.sliders[3].setMaximum(3)
        self.sliders[3].setOrientation(QtCore.Qt.Vertical)
        self.sliders[3].setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sliders[3].setTickInterval(4)
        self.sliders[3].setObjectName("Slide4")
        self.horizontalLayout.addWidget(self.sliders[3])
        self.sliders.append(QtWidgets.QSlider(self.widget))
        self.sliders[4].setMinimum(-3)
        self.sliders[4].setMaximum(3)
        self.sliders[4].setProperty("value", 0)
        self.sliders[4].setSliderPosition(0)
        self.sliders[4].setTracking(True)
        self.sliders[4].setOrientation(QtCore.Qt.Vertical)
        self.sliders[4].setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sliders[4].setTickInterval(4)
        self.sliders[4].setObjectName("Slide5")
        self.horizontalLayout.addWidget(self.sliders[4])

        self.retranslateUi(Sliders)
        QtCore.QMetaObject.connectSlotsByName(Sliders)

    def retranslateUi(self, Sliders):
        _translate = QtCore.QCoreApplication.translate
        Sliders.setWindowTitle(_translate("Sliders", "Equalizer"))
