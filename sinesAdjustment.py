import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, ifft 
import wavio



t = np.linspace(0, 5, 44100*5)
x = 2*np.sin(2*np.pi*400*t) + np.sin(2*np.pi*10000*t) + np.sin(2*np.pi*16000*t)

f = np.linspace(0, 22050, len(x)//2)
X = fft(x, len(x))[:len(x)//2]
print(ifft(X, len(x)).real)
# cls = wavio.read("sine4003000.wav")
# print(x)
# print("WIDTH ={}".format(cls.sampwidth))
# print(cls.data[:, 0])

wavio.write("eds.wav", data=x.astype(np.int32), rate=44100, sampwidth=4)
data = wavio.read("eds.wav")
print(data.data)
