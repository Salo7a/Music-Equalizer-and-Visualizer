import itertools
import sys
from copy import copy

import simpleaudio as sa
from PyQt5.Qt import Qt
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGroupBox, QPushButton, QVBoxLayout, QSlider, QLabel, QComboBox, \
    QApplication

from Graph import *
from fftFunctions import *
from subBands import subBands, FWHM


class WindowingWidget(QWidget):
    def __init__(self, player):

        super().__init__()
        self.resize(QtCore.QSize(1000, 700))
        self.player = player
        self.path = self.player.currentMedia().canonicalUrl().path()
        # Set configurations of the widget
        self.bandsNumber = 10
        self.slidersList = []
        self.gainLabels = []
        self.windowComboBoxes = []
        self.selectedWindows = ["Rectangular"] * self.bandsNumber
        self.threadPool = QThreadPool()

        # Setting original data graph
        self.originalLayout = QHBoxLayout()
        self.originalTime = GraphWidget()
        self.originalFreq = GraphWidget()
        self.originalLayout.addWidget(self.originalTime)
        self.originalLayout.addWidget(self.originalFreq)
        self.orignalBox = QGroupBox()
        self.orignalBox.setLayout(self.originalLayout)
        # Setting the sliders

        self.slidersLayout = self.SlidersLayout(self.bandsNumber)
        self.slidersGroupBox = QGroupBox()
        self.slidersGroupBox.setLayout(self.slidersLayout)

        # Reading the data from .wav file and plotting the data
        self.wavClass = wav2data(self.path)
        self.originalTime.setPlot(self.wavClass.time, self.wavClass.data)
        self.originalFreq.setPlot(self.wavClass.freq, self.wavClass.fftPlotting)
        self.freqBands = subBands(self.wavClass.freq, self.bandsNumber)
        self.amplitudeBands = subBands(self.wavClass.fftPlotting, self.bandsNumber)
        self.pfftBands = subBands(self.wavClass.fftArrayPositive, self.bandsNumber)
        self.nfftBands = subBands(self.wavClass.fftArrayNegative, self.bandsNumber)

        # Edited data plotting
        self.editedLayout = QHBoxLayout()
        self.editedBox = QGroupBox()
        self.editedFreq = GraphWidget()
        self.editedTime = GraphWidget()
        self.editedTime.YRange(np.min(self.wavClass.data), np.max(self.wavClass.data))
        self.editedFreq.YRange(0, 6 * np.max(self.wavClass.fftPlotting))
        self.editedFreq.setPlot(self.wavClass.freq, self.wavClass.fftPlotting, pen='r')
        self.editedTime.setPlot(self.wavClass.time, self.wavClass.data, pen='r')
        self.editedData = copy(self.amplitudeBands)
        self.editedpFFTData = copy(self.pfftBands)
        self.editednFFTData = copy(self.nfftBands)
        self.editedLayout.addWidget(self.editedTime)
        self.editedLayout.addWidget(self.editedFreq)
        self.editedBox.setLayout(self.editedLayout)

        self.submit = QPushButton("Submit")
        # list(itertools.chain.from_iterable(list2d))
        self.submit.clicked.connect(lambda: self.createNewSong(
            np.append(np.array(list(itertools.chain.from_iterable(self.editedpFFTData))),
                      np.flip(np.array(list(itertools.chain.from_iterable(self.editednFFTData))))), "e321s.wav"))
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.orignalBox)
        self.mainLayout.addWidget(self.slidersGroupBox)
        self.mainLayout.addWidget(self.submit)
        self.mainLayout.addWidget(self.editedBox)
     

        self.setLayout(self.mainLayout)
        self.show()

    def SlidersLayout(self, number=10):
        layout = QHBoxLayout()
        for index in range(number):
            sliderBox = QVBoxLayout()
            sliderGroup = QGroupBox()
            slider = QSlider()
            slider.setOrientation(Qt.Vertical)
            slider.setTickPosition(QSlider.TicksBelow)
            slider.setTickInterval(1)
            slider.setValue(0)
            slider.setMinimum(-30)
            slider.setMaximum(30)
            label = QLabel()
            label.setText("0  dB")
            self.gainLabels.append(label)
            windowCombo = QComboBox()
            windowCombo.addItem("Rectangular")
            windowCombo.addItem("Hamming")
            windowCombo.addItem("Hanning")
            self.setComboFunction(windowCombo, index)
            self.windowComboBoxes.append(windowCombo)
            self.setSliderFunction(slider, index, label)
            self.slidersList.append(slider)
            sliderBox.addWidget(slider)
            sliderBox.addWidget(label)
            sliderBox.addWidget(windowCombo)
            sliderBox.setAlignment(Qt.AlignCenter)
            sliderGroup.setLayout(sliderBox)
            sliderGroup.setMinimumHeight(300)
            layout.addWidget(sliderGroup)

        return layout

    def setSliderFunction(self, slider, index, label):
        slider.sliderReleased.connect(lambda: self.sliderMoved(index, label))

    def setComboFunction(self, windowCombo, index):
        windowCombo.activated[str].connect(lambda: self.windowSelected(index))

    def windowSelected(self, index):
        self.selectedWindows[index] = self.windowComboBoxes[index].currentText()
        # print(self.selectedWindows[index], index)
        self.sliderMoved(index, self.gainLabels[index])

    def sliderMoved(self, index, label):
        gainDB = self.slidersList[index].value()
        label.setText(str(gainDB) + "dB")
        gain = self.getGain(gainDB)
        self.applyWindow(gain, index)

    def getGain(self, db):
        return 10 ** (db / 20)

    def applyWindow(self, gain, index):
        factorFFT = 1
        factorAmp = 1
        pfactorData = 1
        nfactorData = 1
        windowType = self.selectedWindows[index]

        if windowType == "Rectangular":
            factorAmp = [gain] * len(self.amplitudeBands[index])

        elif windowType == "Hanning":
            factorAmp = np.hanning(len(self.amplitudeBands[index])) * gain

        elif windowType == "Hamming":
            factorAmp = np.hamming(len(self.amplitudeBands[index])) * gain


        factorFWHM = FWHM(factorAmp, len(self.amplitudeBands[index]))

        self.editedData[index] = self.amplitudeBands[index] * factorFWHM.middle
        self.editedpFFTData[index] = self.pfftBands[index] * factorFWHM.middle


        if index == self.bandsNumber-1:
            self.editednFFTData[index] = self.nfftBands[index] * np.append(factorFWHM.middle, [0.5])

        else:
            self.editednFFTData[index] = self.nfftBands[index] * factorFWHM.middle


        if index != 0:
            self.editedData[index - 1][-factorFWHM.beforeLength:] = self.editedData[index - 1][-factorFWHM.beforeLength:] * factorFWHM.before
            self.editedpFFTData[index - 1][-factorFWHM.beforeLength:] = self.editedpFFTData[index - 1][-factorFWHM.beforeLength:] * factorFWHM.before
            self.editednFFTData[index - 1][-factorFWHM.beforeLength:] = self.editednFFTData[index - 1][-factorFWHM.beforeLength:] * factorFWHM.before

        if index != self.bandsNumber - 1:
            self.editedData[index + 1][:factorFWHM.afterLength] = self.editedData[index + 1][:factorFWHM.afterLength] * factorFWHM.after
            self.editedpFFTData[index + 1][:factorFWHM.afterLength] = self.editedpFFTData[index + 1][:factorFWHM.afterLength] * factorFWHM.after
            self.editednFFTData[index + 1][:factorFWHM.afterLength] = self.editednFFTData[index + 1][:factorFWHM.afterLength] * factorFWHM.after

        compressedTime = np.append(np.array(list(itertools.chain.from_iterable(self.editedpFFTData))),
                                   np.flip(np.array(list(itertools.chain.from_iterable(self.editednFFTData)))))

        timePlotter = TimePlotter(lambda: self.plotTime(compressedTime))
        self.threadPool.start(timePlotter)
        freqPlotter = FreqPlotter(self.plotFreq)
        self.threadPool.start(freqPlotter)


    def createNewSong(self, data, name):
        dataAudio = data2wav(data)
        print(self.wavClass.rate)
        wavio.write(name, dataAudio.astype(np.int32), self.wavClass.rate, sampwidth=self.wavClass.width)
        print("COMPLETE!!!")

    def playArray(self, arr):
        dataAudio = data2wav(arr)
        self.play_obj = sa.play_buffer(dataAudio, 1, 4, 44100)
        self.play_obj.wait_done()
        QApplication.processEvents()

    def stopArray(self):
        try:
            self.play_obj.stop()
        except:
            pass

    def plotTime(self, data):
        self.editedTime.UpdatePlot(self.wavClass.time, data2wav(data))

    def plotFreq(self):
        compressedData = list(itertools.chain.from_iterable(self.editedData))
        self.editedFreq.UpdatePlot(self.wavClass.freq, compressedData)


class TimePlotter(QRunnable):
    def __init__(self, plot):
        super().__init__()
        self.plot = plot

    @pyqtSlot()
    def run(self):
        self.plot()


class FreqPlotter(QRunnable):
    def __init__(self, plot):
        super().__init__()
        self.plot = plot

    @pyqtSlot()
    def run(self):
        self.plot()




app = QApplication(sys.argv)
window = WindowingWidget("wavFiles/cello.wav")
sys.exit(app.exec_())
