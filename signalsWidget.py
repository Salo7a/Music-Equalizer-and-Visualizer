import numpy as np
import wavio        # https://github.com/WarrenWeckesser/wavio/blob/master/wavio.py
from PyQt5.QtCore import QTimer
from scipy.fftpack import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Graph import *
from fftFunctions import wav2data
import sys


class SignalsWidget(QWidget):
    def __init__(self, filePath):
        super().__init__()
        self.wavClass = wav2data(filePath)
        self.createSignals(self.wavClass)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.timeDomainSignal)
        self.layout.addWidget(self.freqDomainSignal)
        self.setLayout(self.layout)
        self.show()
        
    
    def createSignals(self, wav):
        self.timeDomainSignal = GraphWidget()
        self.timeDomainSignal.setPlot(wav.time, wav.data)
        self.freqDomainSignal = GraphWidget()
        self.freqDomainSignal.setPlot(wav.freq, wav.fftArrayNormalized)
        



if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = SignalsWidget("wavFiles/ChillingMusic.wav")
    sys.exit(app.exec_())
    