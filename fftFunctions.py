import numpy as np
import wavio        # https://github.com/WarrenWeckesser/wavio/blob/master/wavio.py
from  numpy.fft import fft, ifft
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write


class wavData():


    def __init__(self, path):
        self.wavClass = wavio.read(path)
        self.width = self.wavClass.sampwidth
        # print(self.width)
        # print(self.wavClass.data)
        self.data = self.wavClass.data[:, 0]

        maxInt = (len(np.unique(self.data)) - 1) // 2
        factor = np.max(self.data) // maxInt
        self.data = self.data / factor


        self.length = len(self.data)

        self.rate = self.wavClass.rate
        self.duration = int(self.length / self.rate)
        self.time = np.linspace(0, self.duration, self.length)
        self.freq = np.linspace(0, self.rate / 2, int(self.length / 2))
        self.fftArray = fft(self.data)
        self.fftArrayPositive = self.fftArray[:self.length//2]
        self.fftArrayNegative = np.flip(self.fftArray[self.length//2:])
        self.fftArrayAbs = np.abs(self.fftArray)
        self.fftPlotting = self.fftArrayAbs[: self.length//2]



def wav2data(path):
    wavClass = wavData(path)
    return wavClass


def data2wav(arr):
    #print(arr)
    data = ifft(arr, len(arr)).real
    return data



path = "wavFiles/cello.wav"
data = wav2data(path)
print(data.data)