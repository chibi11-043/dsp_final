import numpy as np
from scipy.io import wavfile

def encode(text, audioData, rate):

    # DIVIDE AUDIO INTO -blockNumber- CONSECUTIVE BLOCKS, 
    # EACH OF LENGTH -blockLength: ~~~~~
    textLength = 8*len(text)
  
    blockLength = int(2 * 2**np.ceil(np.log2(2*textLength)))
    blockNumber = int(np.ceil(audioData.shape[0]/blockLength))
  
    if len(audioData.shape) == 1:
        audioData.resize(blockNumber*blockLength, refcheck=False)  
        audioData = audioData[np.newaxis]
    else:
        audioData.resize((blockNumber*blockLength, audioData.shape[1]), refcheck=False)
        audioData = audioData.T

    blocks = audioData[0].reshape((blockNumber, blockLength))
  
    # COMPUTE THE DISCRETE FOURIER TRANSFORM (DFT) 
    # WITH THE EFFICIENT OF FAST FOURIER TRANSFORM ALGORITHM: ~~~~~
    blocks = np.fft.fft(blocks)

    # COMPUTE MAGNITUDE VALUES: ~~~~~
    magnitudes = np.abs(blocks)
  
    # COMPUTE PHASES MATRIX: ~~~~~
    phases = np.angle(blocks)
    
    # COMPUTE PHASE DIFFERENCES: ~~~~~
    phaseDiffs = np.diff(phases, axis=0)
       
    # CONVERT EACH CHAR IN -text- TO BINARY FORMAT OF WIDTH 8 
    # & STORE ALL IN 1 ARRAY: ~~~~~
    textInBinary = np.ravel([[int(y) for y in format(ord(x), "08b")] for x in text])

    # CONVERT TEXT OF BINARY FORMAT TO PHASE FORMAT,
    # REPLACE 0 BY PI/2 & 1 BY -PI/2: ~~~~~
    textInPi = textInBinary.copy()
    textInPi[textInPi == 0] = -1
    textInPi = textInPi * -np.pi/2


    blockMid = blockLength // 2
   
    # PLACE TEXT IN PHASE FORMAT INTO PHASE VECTOR OF FIRST BLOCK
    # WHILE MAINTAIN ODD SYMMETRIC PROPERTY OF DFT: ~~~~~
    phases[0, blockMid - textLength : blockMid] = textInPi
    phases[0, blockMid+1 : blockMid+1 + textLength]  = -textInPi[::-1]

    # RECOMPUTE PHASES MATRIX: ~~~~~
    for i in range(1, len(phases)): 
        phases[i] = phases[i-1] + phaseDiffs[i-1]

    # APPLY INVERSE DFT TO EACH BLOCK: ~~~~~
    blocks = (magnitudes * np.exp(1j * phases))
    blocks = np.fft.ifft(blocks).real

    # JOINING ALL BLOCKS TOGETHER TO RECONSTRUCT AUDIO: ~~~~~
    audioData[0] = blocks.ravel().astype(np.int16)

    wavfile.write("encoded_audio.wav", rate, audioData.T)
