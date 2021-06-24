import os
import scipy.io
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pylab

myAudioFilename = 'sample.wav'  # plot this wav file     ~/audio/aaa.wav
myDecodeFileName = 'decode.wav'


def read_wav_file(x):
    # Read wavfile using scipy wavfile.read
    _, wav = scipy.io.wavfile.read(x)
    # Normalize
    wav = wav.astype(np.float32) / np.iinfo(np.int16).max

    return wav


sampleRate, audioBuffer = scipy.io.wavfile.read(myAudioFilename)
duration = len(audioBuffer) / sampleRate

time = np.arange(0, duration, 1 / sampleRate)
fig = plt.figure(figsize=(14, 8))
wav = read_wav_file(myAudioFilename)
ax = fig.add_subplot(2, 2, 1)
ax.set_title('Ratio wave of ' + myAudioFilename)
ax.set_ylabel('Amplitude')
ax.plot(np.linspace(0, audioBuffer.shape[0] / len(wav), audioBuffer.shape[0]), wav)

ax1 = fig.add_subplot(2, 2, 2)
ax1.plot(time, audioBuffer)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Amplitude')
ax1.set_title('Raw wave of ' + myAudioFilename)

sampleRateDecode, audioBufferDecode = scipy.io.wavfile.read(myDecodeFileName)
durationDecode = len(audioBufferDecode) / sampleRateDecode

timeDecode = np.arange(0, durationDecode, 1 / sampleRateDecode)
wav = read_wav_file(myDecodeFileName)
ax2 = fig.add_subplot(2, 2, 3)
ax2.set_title('Ratio wave of ' + myDecodeFileName)
ax2.set_ylabel('Amplitude')
ax2.plot(np.linspace(0, audioBufferDecode.shape[0] / len(wav), audioBufferDecode.shape[0]), wav)

ax3 = fig.add_subplot(2, 2, 4)
ax3.plot(timeDecode, audioBufferDecode)
ax3.set_xlabel('Time [s]')
ax3.set_ylabel('Amplitude')
ax3.set_title('Raw wave of ' + myDecodeFileName)

fig.tight_layout()

plt.show()
