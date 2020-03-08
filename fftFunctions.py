import numpy as np
import wavio  # https://github.com/WarrenWeckesser/wavio/blob/master/wavio.py
from numpy.fft import fft, ifft
import scipy.io.wavfile as wavfile


class wavData():

    def __init__(self, path):
        # self.wavClass = wavio.read(path)
        # self.width = self.wavClass.sampwidth
        # # print(self.width)
        # # print(self.wavClass.data)
        # self.data = self.wavClass.data[:, 0]
        #
        # maxInt = (len(np.unique(self.data)) - 1) // 2
        # factor = np.max(self.data) // maxInt
        # self.data = self.data / factor
        #
        # self.rate = self.wavClass.rate
        
        self.rate, data = wavfile.read(path)
        if data.ndim == 1:
            self.data = data
        elif data.ndim == 2:
            self.data = data[:, 0]

        self.length = len(self.data)
        self.duration = int(self.length / self.rate)

        # For Ahmed Salah,
        ## Hat3'yar self.data [ et2kd ta5od awerl channel bs [:,0], self.rate, self.duration
        # No need to change the code below


        self.time = np.linspace(0, self.duration, self.length)
        self.freq = np.linspace(0, self.rate / 2, int(self.length / 2))
        self.fftArray = fft(self.data)
        self.fftArrayPositive = self.fftArray[:self.length // 2]
        self.fftArrayNegative = np.flip(self.fftArray[self.length // 2:])
        self.fftArrayAbs = np.abs(self.fftArray)
        self.fftPlotting = self.fftArrayAbs[: self.length // 2]


def wav2data(path):
    wavClass = wavData(path)
    return wavClass


def data2wav(arr):
    # print(arr)
    data = ifft(arr, len(arr)).real
    return data.astype(np.int32)



path = "wavFiles/cello.wav"
data = wav2data(path)
print(data.data)