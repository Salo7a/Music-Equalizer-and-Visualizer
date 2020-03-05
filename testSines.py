# from fftFunctions import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import  *
import wavio



def sin(amp, freq, timeArray, phase=0):
    return amp * np.sin(2 * np.pi * freq * timeArray + phase)


def cos(amp, freq, phase, timeArray):
    return amp * np.cos(2 * np.pi * freq * timeArray + phase)


rate = 44100
t = np.linspace(0, 10, 10*44100)
wave = sin(4, 10000000000000, t)
# plt.figure(1)
# plt.plot(t, wave)

data = wavio.read("TEST.wav")
print(wave)
print(data.data)
print(6119297/1.13980790e-02)
print(12238544/2.27960655e-02)


wavio.write("TEST.wav", wave, rate, sampwidth=4)
# freq = np.linspace(0, rate/2, 5*44100)
# abs = fft(wave)
# absAbs =(np.abs(abs) * 2 / (10*44100))[:5*44100]
#
#
# org = ifft(abs)
#
# print(wave)
# print(np.real(org))
#



