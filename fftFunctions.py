import numpy as np
from numpy.fft import fft, ifft
from pydub import AudioSegment


class wavData():

    def __init__(self, path):
        self.audio = AudioSegment.from_file(path).set_channels(1)
        self.rate, self.data = self.audio.frame_rate, np.array(self.audio.get_array_of_samples())
        self.length = len(self.data)
        self.duration = self.audio.duration_seconds

        # For Ahmed Salah,
        # Hat3'yar self.data [ et2kd ta5od awerl channel bs [:,0], self.rate, self.duration
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
