# Example 11.13
# pip install sounddevice soundfile
import sounddevice as sd
import soundfile as sf
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from scipy import signal
fs=44100
duration = 5 # seconds
myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,
dtype='float64')
print ("Grabando ...")
sd.wait()
print ("Reproduciendo Audio ...")
sd.play(myrecording, fs)
sd.wait()
print ("Guardando Audio: test.wav")
filename = "test.wav"
sf.write(filename, myrecording, fs)
# plot wave by audio frames
plt.figure(figsize=(10, 5))
plt.subplot(2,1,1)
plt.plot(myrecording[:,0], 'r-',
label='Left');
plt.legend()
plt.subplot(2,1,2)
plt.plot(myrecording[:,1], 'g-',
label='Right');
plt.legend()
plt.show()

path = 'test.wav'
data, rate = sf.read(path)
# Plot the signal read from wav file
plt.figure(figsize=(10, 6))
plt.subplot(211)
plt.title('Espectograma de Sonido')
plt.plot(data[:,0])

plt.xlabel('Prueba')
plt.ylabel('Amplitud')
plt.subplot(212)
plt.specgram(data[:,0],Fs=rate)
plt.xlabel('Tiempo')
plt.ylabel('Frecuencia')
plt.show()