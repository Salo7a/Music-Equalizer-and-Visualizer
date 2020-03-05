import numpy as np
import wavio
import matplotlib.pyplot as plt
from numpy.fft import fft, ifft

t = np.linspace(0, 5, 44100*5)
x = (np.sin(2*np.pi*500*t+np.pi/4) + 3*np.sin(2*np.pi*5000*t+np.pi/8)).astype(np.int32)
FFT = np.abs(fft(x, len(x))).astype(np.float32)
f = np.linspace(0, 22050, 22050*5)
wavio.write("sine.wav", x, 44100, sampwidth=4)
data = wavio.read("sine.wav")
maxInt = (len(np.unique(data.data)) - 1)//2
factor = np.max(data.data) // maxInt
plt.plot(f, FFT[:5*22050])
# plt.plot(np.abs(np.flip(FFT[5*22050:])), 'o')
plt.show()