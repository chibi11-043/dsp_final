import numpy as np
import scipy as sp
from scipy.io import wavfile
import os


def encode_phase(wavfile, textfile, save_path, file_name):
    rate, audioData = sp.io.wavfile.read(wavfile)
    audioData = audioData.copy()

    f = open(textfile, "r")
    string = f.read()
    f.close()

    string = string + (500 - len(string)) * " "

    # DIVIDE AUDIO INTO -blockNumber- CONSECUTIVE BLOCKS,
    # EACH OF LENGTH -blockLength: ~~~~~
    textLength = 8 * len(string)
    print(len(string))

    blockLength = int(2 * 2 ** np.ceil(np.log2(2 * textLength)))
    blockNumber = int(audioData.shape[0] // blockLength)
    # just take the first channel of audio and divides it into many segments, length of segments
    # based on bock length 2^v>2*v
    audioData = np.array([audioData])
    audioData = audioData[:, 1]
    audioData = audioData[0:blockLength * blockNumber]
    blocks = audioData.reshape((blockNumber, blockLength))

    # COMPUTE THE DISCRETE FOURIER TRANSFORM (DFT)
    blocks = np.fft.fft(blocks)

    # COMPUTE MAGNITUDE VALUES: ~~~~~
    magnitudes = np.abs(blocks)

    # COMPUTE PHASES MATRIX: ~~~~~
    phases = np.angle(blocks)

    # COMPUTE PHASE DIFFERENCES: ~~~~~
    phaseDiffs = np.diff(phases, axis=0)

    # CONVERT EACH CHAR IN -text- TO BINARY FORMAT OF WIDTH 8
    # & STORE ALL IN 1 ARRAY: ~~~~~
    textInBinary = np.ravel([[int(y) for y in format(ord(x), "08b")] for x in string])

    # CONVERT TEXT OF BINARY FORMAT TO PHASE FORMAT,
    # REPLACE 0 BY PI/2 & 1 BY -PI/2: ~~~~~
    textInPi = textInBinary.copy()
    textInPi[textInPi == 0] = -1
    textInPi = textInPi * -np.pi / 2

    blockMid = blockLength // 2

    # PLACE TEXT IN PHASE FORMAT INTO PHASE VECTOR OF FIRST BLOCK
    # WHILE MAINTAIN ODD SYMMETRIC PROPERTY OF DFT: ~~~~~
    phases[0, blockMid - textLength: blockMid] = textInPi
    phases[0, blockMid + 1: blockMid + 1 + textLength] = -textInPi[::-1]

    # RECOMPUTE PHASES MATRIX: ~~~~~
    for i in range(1, len(phases)):
        phases[i] = phases[i - 1] + phaseDiffs[i - 1]

    # APPLY INVERSE DFT TO EACH BLOCK: ~~~~~
    blocks = (magnitudes * np.exp(1j * phases))
    blocks = np.fft.ifft(blocks).real

    # JOINING ALL BLOCKS TOGETHER TO RECONSTRUCT AUDIO: ~~~~~
    audioData[0] = blocks.ravel().astype(np.int16)

    complete_name = os.path.join(save_path, file_name)
    sp.io.wavfile.write(complete_name + ".wav", rate, audioData.T)

# encode_phase('sample.wav', 'text.txt')
