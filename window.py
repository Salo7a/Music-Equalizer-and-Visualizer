import numpy as np
import wavio        # https://github.com/WarrenWeckesser/wavio/blob/master/wavio.py
from PyQt5.QtCore import QTimer
from scipy.fftpack import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import *
from subBands import subBands
from Graph import *
from fftFunctions import *
from copy import copy, deepcopy
import itertools
import sys



class WindowingWidget(QWidget):
    def __init__(self, path):
        super().__init__()
        self.original = GraphWidget()

        self.slidersLayout = self.SlidersLayout(3)
        self.slidersGroupBox = QGroupBox()
        self.slidersGroupBox.setLayout(self.slidersLayout)
        self.wavClass = wav2data(path)
        self.original.setPlot(self.wavClass.freq, self.wavClass.fftArrayNormalized)
        self.freqBands = subBands(self.wavClass.freq, 3)
        self.amplitudeBands = subBands(self.wavClass.fftArrayNormalized, 3)
        self.fftBands = subBands(self.wavClass.fftArray, 3)
        self.edited = GraphWidget()
        self.edited.YRange(0, 6*np.max(self.wavClass.fftArrayNormalized))
        self.edited.setPlot(self.wavClass.freq, self.wavClass.fftArrayNormalized)
        self.editedData = copy(self.amplitudeBands)
        self.editedFFT = copy(self.fftBands)



        self.submit = QPushButton("Submit")
        self.submit.clicked.connect(lambda: self.createNewSong(np.array(list(itertools.chain.from_iterable(self.editedFFT))), "wew.wav"))


        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.original)
        self.mainLayout.addWidget(self.slidersGroupBox)
        self.mainLayout.addWidget(self.submit)
        self.mainLayout.addWidget(self.edited)



        self.setLayout(self.mainLayout)
        self.show()


    def SlidersLayout(self, number=10):
        self.layout = QHBoxLayout()
        self.slidersList = []
        for index in range(number):
            sliderBox = QVBoxLayout()
            sliderGroup = QGroupBox()
            slider = QSlider()
            slider.setOrientation(Qt.Vertical)
            slider.setTickPosition(QSlider.TicksBelow)
            slider.setTickInterval(1)
            slider.setValue(0)
            slider.setMinimum(-15)
            slider.setMaximum(15)
            label = QLabel()
            label.setText("0  dB")
            self.setSliderFunction(slider, index, label)
            self.slidersList.append(slider)
            sliderBox.addWidget(slider)
            sliderBox.addWidget(label)
            sliderBox.setAlignment(Qt.AlignCenter)
            sliderGroup.setLayout(sliderBox)
            sliderGroup.setMinimumHeight(200)
            self.layout.addWidget(sliderGroup)

        return self.layout


    def setSliderFunction(self, slider, index, label):
        slider.valueChanged.connect(lambda: self.sliderMoved(index, label))


    def sliderMoved(self, index, label):
        gainDB = self.slidersList[index].value()
        label.setText(str(gainDB) + "dB")
        gain = self.getGain(gainDB)
        #print(index)
        self.applyWindow(gain, "rect", index)


    def getGain(self, db):
        return 10**(db/20)



    def applyWindow(self, gain, windowType, index):
        if windowType == "rect":
            self.editedFFT[index] = self.fftBands[index] * gain
            self.editedData[index] = self.amplitudeBands[index] * gain
            print(self.editedData[index])
            compressedData = list(itertools.chain.from_iterable(self.editedData))
            self.edited.UpdatePlot(self.wavClass.freq, compressedData)
            QApplication.processEvents()


        elif windowType == "hann":
            pass

        elif windowType == "hamm":
            pass

    def showNewSignal(self):
        pass


    def createNewSong(self, data, name):
        dataAudio = data2wav(data)
        print(self.wavClass.data)
        print(dataAudio)
        wavio.write(name, dataAudio, self.wavClass.rate, sampwidth=self.wavClass.width)
        print("COMPLETE!!!")



app = QApplication(sys.argv)
window = WindowingWidget("wavFiles/ChillingMusic.wav")
sys.exit(app.exec_())
