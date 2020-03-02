import numpy as np
import wavio        # https://github.com/WarrenWeckesser/wavio/blob/master/wavio.py
from scipy.fftpack import *


class wavData():
    def __init__(self, path):
        self.wavClass = wavio.read(path)
        self.data = self.wavClass.data[:, 0]
        self.rate = self.wavClass.rate
        self.width = self.wavClass.sampwidth
        self.length = len(self.data)
        self.duration = int(self.length / self.rate)
        self.time = np.linspace(0, self.duration, self.length)
        self.freq = np.linspace(0, self.rate / 2, int(self.length / 2))
        self.fftArray = fft(self.data)
        self.fftArrayAbs = np.abs(self.fftArray)
        self.fftNormalized = (self.fftArrayAbs * 2 / self.length)
        self.fftArrayNormalized = self.fftNormalized[:self.length // 2]


# class audioData():
#     def __init__(self, data):
#         


def wav2data(path):
    wavClass = wavData(path)
    return wavClass


def data2wav(arr):
    data = ifft(arr)
    realData = np.round(np.real(data))
    return realData



dataClass = wav2data("wavFiles/ChillingMusic.wav")
data = ifft(dataClass.fftArray)
print(dataClass.data)
print(data2wav(dataClass.fftArray))