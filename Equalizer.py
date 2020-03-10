import itertools
import sys
from copy import copy

import sounddevice as sd
import wavio
from PyQt5.Qt import Qt
from PyQt5 import  QtCore
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGroupBox, QPushButton, QVBoxLayout, QSlider, QLabel, QComboBox, \
    QApplication, QFileDialog


from Graph import *
from fftFunctions import *
from subBands import subBands, FWHM



class WavClass:
    def __init__(self, path):
        self.bandsNumber = 10
        self.wavClass = wavData(path)
        self.timeData = self.wavClass.data
        self.fftPlotting = self.wavClass.fftPlotting
        self.freqBands = subBands(self.wavClass.freq, self.bandsNumber)
        self.amplitudeBands = subBands(self.wavClass.fftPlotting, self.bandsNumber)
        self.pfftBands = subBands(self.wavClass.fftArrayPositive, self.bandsNumber)
        self.nfftBands = subBands(self.wavClass.fftArrayNegative, self.bandsNumber)
        self.gains = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


class WindowingWidget(QWidget):
    SendPath = QtCore.pyqtSignal(str)

    def __init__(self, path):

        super().__init__()
        self.resize(QtCore.QSize(1000, 700))
        self.path = path[1:]
        # Set configurations of the widget
        self.bandsNumber = 10
        self.slidersList = []
        self.gainLabels = []
        self.windowComboBoxes = []
        self.selectedWindows = ["Rectangular"] * self.bandsNumber
        self.threadPool = QThreadPool()
        app.aboutToQuit.connect(self.closeEvent)

        self.selectedChannel = 0
        self.changeButton = QPushButton("Change to Channel 2")
        self.changeButton.clicked.connect(self.channelChanged)

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
        self.channels = [WavClass(self.path), WavClass(self.path)]
        self.originalTime.setPlot(self.channels[self.selectedChannel].wavClass.time, self.channels[self.selectedChannel].wavClass.data.astype(int))
        self.originalFreq.setPlot(self.channels[self.selectedChannel].wavClass.freq, self.channels[self.selectedChannel].wavClass.fftPlotting)




        # Edited data plotting
        self.editedLayout = QHBoxLayout()
        self.editedBox = QGroupBox()
        self.editedFreq = GraphWidget()
        self.editedTime = GraphWidget()
        self.editedTime.YRange(np.min(self.channels[self.selectedChannel].wavClass.data.astype(int)), np.max(self.channels[self.selectedChannel].wavClass.data.astype(int)))
        self.editedFreq.YRange(0, 6 * np.max(self.channels[self.selectedChannel].wavClass.fftPlotting))
        self.editedFreq.setPlot(self.channels[self.selectedChannel].wavClass.freq, self.channels[self.selectedChannel].wavClass.fftPlotting, pen='r')
        self.editedTime.setPlot(self.channels[self.selectedChannel].wavClass.time, self.channels[self.selectedChannel].wavClass.data.astype(int), pen='r')
        self.editedData = [copy(self.channels[0].amplitudeBands), copy(self.channels[1].amplitudeBands)]
        self.editedpFFTData = [copy(self.channels[0].pfftBands), copy(self.channels[1].pfftBands)]
        self.editednFFTData = [copy(self.channels[0].nfftBands), copy(self.channels[1].nfftBands)]
        self.editedLayout.addWidget(self.editedTime)
        self.editedLayout.addWidget(self.editedFreq)
        self.editedBox.setLayout(self.editedLayout)

        self.submit = QPushButton("Submit")
        # list(itertools.chain.from_iterable(list2d))
        self.submit.clicked.connect(lambda: self.createNewSong(
            np.append(np.array(list(itertools.chain.from_iterable(self.editedpFFTData[self.selectedChannel]))),
                      np.flip(np.array(list(itertools.chain.from_iterable(self.editednFFTData[self.selectedChannel]))))), "e321s.wav"))

        self.play = QPushButton("Play")
        self.play.clicked.connect(lambda: self.playSong(np.append(np.array(list(itertools.chain.from_iterable(self.editedpFFTData[self.selectedChannel]))),
                      np.flip(np.array(list(itertools.chain.from_iterable(self.editednFFTData[self.selectedChannel])))))))

        self.stop = QPushButton("Stop")
        self.stop.clicked.connect(lambda: sd.stop())

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.changeButton)
        self.mainLayout.addWidget(self.orignalBox)
        self.mainLayout.addWidget(self.slidersGroupBox)
        self.mainLayout.addWidget(self.submit)

        self.playPauseLayout = QHBoxLayout()
        self.playPauseLayout.addWidget(self.play)
        self.playPauseLayout.addWidget(self.stop)
        self.playPauseBox = QGroupBox()
        self.playPauseBox.setLayout(self.playPauseLayout)

        self.mainLayout.addWidget(self.playPauseBox)
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
            slider.setMinimum(-8)
            slider.setMaximum(8)
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


    def channelChanged(self):
        if self.selectedChannel == 0:
            self.selectedChannel = 1
            self.changeButton.setText("Change to Channel 1")
            pen = 'b'
        elif self.selectedChannel == 1:
            self.selectedChannel = 0
            self.changeButton.setText("Change to Channel 2")
            pen = 'r'
        for i in range(10):
            self.slidersList[i].setValue(self.channels[self.selectedChannel].gains[i])
            self.gainLabels[i].setText(str(self.channels[self.selectedChannel].gains[i]) +" dB")

        self.editedTime.UpdatePlot([], [])
        self.editedFreq.UpdatePlot([], [])
        self.editedTime.YRange(np.min(self.channels[self.selectedChannel].wavClass.data.astype(int)),
                               np.max(self.channels[self.selectedChannel].wavClass.data.astype(int)))
        compressedData = list(itertools.chain.from_iterable(self.editedData[self.selectedChannel]))
        self.editedFreq.YRange(0, 6 * np.max(self.channels[self.selectedChannel].wavClass.fftPlotting))
        self.editedFreq.setPlot(self.channels[self.selectedChannel].wavClass.freq,
                                compressedData, pen=pen)

        compressedTime = np.append(
            np.array(list(itertools.chain.from_iterable(self.editedpFFTData[self.selectedChannel]))),
            np.flip(np.array(list(itertools.chain.from_iterable(self.editednFFTData[self.selectedChannel])))))

        self.editedTime.setPlot(self.channels[self.selectedChannel].wavClass.time, data2wav(compressedTime), pen=pen)




    def windowSelected(self, index):
        self.selectedWindows[index] = self.windowComboBoxes[index].currentText()
        # print(self.selectedWindows[index], index)
        self.sliderMoved(index, self.gainLabels[index])

    def sliderMoved(self, index, label):
        gainDB = self.slidersList[index].value()
        self.channels[self.selectedChannel].gains[index] = gainDB
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
            factorAmp = [gain] * len(self.channels[self.selectedChannel].amplitudeBands[index])

        elif windowType == "Hanning":
            factorAmp = np.hanning(len(self.channels[self.selectedChannel].amplitudeBands[index])) * gain

        elif windowType == "Hamming":
            factorAmp = np.hamming(len(self.channels[self.selectedChannel].amplitudeBands[index])) * gain

        factorFWHM = FWHM(factorAmp, len(self.channels[self.selectedChannel].amplitudeBands[index]))

        self.editedData[self.selectedChannel][index] = self.channels[self.selectedChannel].amplitudeBands[index] * factorFWHM.middle
        self.editedpFFTData[self.selectedChannel][index] = self.channels[self.selectedChannel].pfftBands[index] * factorFWHM.middle

        if index == self.bandsNumber - 1:
            self.editednFFTData[self.selectedChannel][index] = self.channels[self.selectedChannel].nfftBands[index] * np.append(factorFWHM.middle, [0.5])

        else:
            self.editednFFTData[self.selectedChannel][index] = self.channels[self.selectedChannel].nfftBands[index] * factorFWHM.middle

        if index != 0:
            self.editedData[self.selectedChannel][index - 1][-factorFWHM.beforeLength:] = self.editedData[self.selectedChannel][index - 1][
                                                                    -factorFWHM.beforeLength:] * factorFWHM.before
            self.editedpFFTData[self.selectedChannel][index - 1][-factorFWHM.beforeLength:] = self.editedpFFTData[self.selectedChannel][index - 1][
                                                                        -factorFWHM.beforeLength:] * factorFWHM.before
            self.editednFFTData[self.selectedChannel][index - 1][-factorFWHM.beforeLength:] = self.editednFFTData[self.selectedChannel][index - 1][
                                                                        -factorFWHM.beforeLength:] * factorFWHM.before

        if index != self.bandsNumber - 1:
            self.editedData[self.selectedChannel][index + 1][:factorFWHM.afterLength] = self.editedData[self.selectedChannel][index + 1][
                                                                  :factorFWHM.afterLength] * factorFWHM.after
            self.editedpFFTData[self.selectedChannel][index + 1][:factorFWHM.afterLength] = self.editedpFFTData[self.selectedChannel][index + 1][
                                                                      :factorFWHM.afterLength] * factorFWHM.after
            self.editednFFTData[self.selectedChannel][index + 1][:factorFWHM.afterLength] = self.editednFFTData[self.selectedChannel][index + 1][
                                                                      :factorFWHM.afterLength] * factorFWHM.after

        compressedTime = np.append(np.array(list(itertools.chain.from_iterable(self.editedpFFTData[self.selectedChannel]))),
                                   np.flip(np.array(list(itertools.chain.from_iterable(self.editednFFTData[self.selectedChannel])))))

        timePlotter = TimePlotter(lambda: self.plotTime(compressedTime))
        self.threadPool.start(timePlotter)
        freqPlotter = FreqPlotter(self.plotFreq)
        self.threadPool.start(freqPlotter)

    def createNewSong(self, data, name):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog # Qt's builtin File Dialogue
        fileName, _ = QFileDialog.getSaveFileName(self, "Save", "", "All Files (*.*)", options=options)
        if fileName:
            dataAudio = data2wav(data)
            print(self.wavClass.rate)
            wavio.write(fileName, dataAudio.astype(np.int32), self.wavClass.rate, sampwidth=4)
            self.AddToPlaylist(fileName)


    def stopArray(self):
        try:
            self.play_obj.stop()
        except:
            pass

    def plotTime(self, data):
        self.editedTime.UpdatePlot(self.channels[self.selectedChannel].wavClass.time, data2wav(data))

    def plotFreq(self):
        compressedData = list(itertools.chain.from_iterable(self.editedData[self.selectedChannel]))
        self.editedFreq.UpdatePlot(self.channels[self.selectedChannel].wavClass.freq, compressedData)

    @QtCore.pyqtSlot()
    def AddToPlaylist(self, path):
        self.SendPath.emit(path)


    def playSong(self, array):
        dataAudio = data2wav(array)
        sd.play(dataAudio.astype(np.int16), self.channels[self.selectedChannel].wavClass.rate)

    def closeEvent(self, event=None):
        sd.stop()
        self.threadPool.releaseThread()
        if event:
            event.accept()


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
window = WindowingWidget("/wavFiles/march.wav")
sys.exit(app.exec_())
