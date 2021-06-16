import os
import scipy.io
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pylab

myAudioFilename = 'sample.wav'  # plot this wav file     ~/audio/aaa.wav
SAMPLE_RATE = 268237


def read_wav_file(x):
    # Read wavfile using scipy wavfile.read
    _, wav = scipy.io.wavfile.read(x)
    # Normalize
    wav = wav.astype(np.float32) / np.iinfo(np.int16).max

    return wav


sampleRate, audioBuffer = scipy.io.wavfile.read(myAudioFilename)
duration = len(audioBuffer) / sampleRate

time = np.arange(0, duration, 1 / sampleRate)  # time vector
fig = plt.figure(figsize=(14, 8))
wav = read_wav_file(myAudioFilename)
ax = fig.add_subplot(2, 2, 1)
ax.set_title('Raw wave of ' + myAudioFilename)
ax.set_ylabel('Amplitude')
ax.plot(np.linspace(0, SAMPLE_RATE / len(wav), SAMPLE_RATE), wav)

ax1 = fig.add_subplot(2, 2, 2)
ax1.plot(time, audioBuffer)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Amplitude')
ax1.set_title(myAudioFilename)
fig.tight_layout()

plt.show()
