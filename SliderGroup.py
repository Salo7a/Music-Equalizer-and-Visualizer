import numpy as np
# import wavio        # https://github.com/WarrenWeckesser/wavio/blob/master/wavio.py
from PyQt5.QtCore import QTimer
from scipy.fftpack import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt
from Graph import *
import sys


class SlidersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        for i in range(10):
            slider = QSlider()
            slider.setOrientation(Qt.Vertical)
            slider.setTickPosition(QSlider.TicksBelow)
            slider.setValue(10)

            slider.setTickInterval(10)
            slider.setMinimum(0)
            slider.setMaximum(100)
            self.setSliderFunction(slider, i)
            self.layout.addWidget(slider)
        self.setLayout(self.layout)
        self.show()

    def setSliderFunction(self, slider, index):
        slider.valueChanged.connect(lambda: self.sliderMoved(index))

    def sliderMoved(self, index):
        print("Slider {} is moving".format(index))
        

app = QApplication(sys.argv)
window = SlidersWindow()
sys.exit(app.exec_())


