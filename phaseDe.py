#delete
import numpy as np
import scipy as sp
from scipy.io import wavfile
import time


def decode_phase(wavfile):
    start = time.time()
    rate, audioData = sp.io.wavfile.read(wavfile)

    textLength = 8 * 500
    blockLength = 2 * int(2 ** np.ceil(np.log2(2 * textLength)))
    blockMid = blockLength // 2

    # EXTRACT EMBEDDED TEXT FROM ENCODED AUDIO: ~~~~~
    if len(audioData.shape) == 1:
        secret = audioData[:blockLength]
    else:
        secret = audioData[:blockLength, 0]

    # GET THE PHASE FORMAT OF TEXT & CONVERT BACK TO BINARY FORMAT: ~~~~~
    secretPhases = np.angle(np.fft.fft(secret))[blockMid - textLength:blockMid]
    secretInBinary = (secretPhases < 0).astype(np.int8)

    # RESHAPE & CONVERT CHARS TO FORMAT OF CODE POINT: ~~~~~
    secretInIntCode = secretInBinary.reshape((-1, 8)).dot(1 << np.arange(8 - 1, -1, -1))

    # CONVERT AND GATHER CHARS TO REFORM ORIGINAL TEXT: ~~~~~
    result = "".join(np.char.mod("%c", secretInIntCode))
    decodeTime = "Decode time: " + str(round(time.time() - start, 2)) + "seconds"
    print(decodeTime)

    return result, decodeTime

# print(decode_phase('sampleStego.wav', 16))
