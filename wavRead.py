import scipy.io.wavfile as wavfile
from fftFunctions import *
import sounddevice as sd


rate, data = wavfile.read("wavFiles/ChillingMusic.wav")
dataChannel = data[:,0]
print(dataChannel)

sd.play(dataChannel, rate)
sd.wait()
wavClass = wav2data("wavFiles/ChillingMusic.wav")
print(wavClass.data)