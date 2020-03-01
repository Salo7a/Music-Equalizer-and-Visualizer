import numpy as np
import wavio        # https://github.com/WarrenWeckesser/wavio/blob/master/wavio.py
from PyQt5.QtCore import QTimer
from scipy.fftpack import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Graph import *
import sys


class SignalsWidget(QWidget):
    def __init__(self, filePath):
        super().__init__()
        self.wavClass = wavio.read("vignesh.wav")
        self.data = self.wavClass.data[:, 0]
        self.rate = self.wavClass.rate
        self.length = len(self.data)
        self.duration = int(self.length/self.rate)
        self.createSignals()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.timeDomainSignal)
        self.layout.addWidget(self.freqDomainSignal)
        self.setLayout(self.layout)
        self.show()
        
    
    def createSignals(self):
        self.time = np.linspace(0, self.duration, self.length)
        self.timeDomainSignal = GraphWidget()
        self.timeDomainSignal.setPlot(self.time, self.data)
        
        
        self.freq = np.linspace(0, self.rate/2, int(self.length/2))
        self.fftArray = fft(self.data)
        self.fftArrayAbs = np.abs(self.fftArray)
        self.fftArrayNormalized = (self.fftArrayAbs * 2 / self.length)
        self.fftArrayNormalized = self.fftArrayNormalized[:self.length//2]
        self.freqDomainSignal = GraphWidget()
        self.freqDomainSignal.setPlot(self.freq, self.fftArrayNormalized)
        



if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = SignalsWidget("ChillingMusic.wav")
    sys.exit(app.exec_())
    