# STEGANOGRAPHY: HIDING TEXT (.TXT) INTO AUDIO (.WAV) FILE
# ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~
from scipy.io import wavfile
from encode import encode
from decode import decode

def phaseEncoding():

    # PREPARE AUDIO DATA AND SAMPLING RATE: ~~~~~~~~~~
    rate, audioData = wavfile.read("audio.wav")
    audioData = audioData.copy()

    # PREPARE TEXT: ~~~~~~~~~~
    f = open("text.txt", "r")
    text = f.read()
    textLength = len(text)
    f.close()

    # ENCODE TEXT INTO AUDIO & WRITE RESULT TO -encoded_audio.wav-: ~~~~~~~~~~
    encode(text, audioData, rate)

    # RETURN LENGTH OF TEXT, WHICH IS NEEDED FOR EXTRACTING BACK THE TEXT
    # FROM ENCODED AUDIO FILE: ~~~~~
    return textLength

def revertPhaseEncoding(filePath, textLength):
    # DECODE TEXT FROM ENCODED AUDIO: ~~~~~~~~~~
    rate, encodedAudio = wavfile.read(filePath)
    return decode(encodedAudio, textLength)


if __name__ == "__main__":
    # Example text link:
    # textUrl = "https://drive.google.com/uc?export=download&id=1Gc0wtK3Hbceb7P80fZRBDN1D0ZH50fjR"   
    # Example audio link:
    # audioUrl = "https://drive.google.com/uc?export=download&id=1yWbMcSOrToiMkhzc7thqVlm1gO1fWgFy"
    
    # textUrl = input("Enter url to the text (.txt) source:\n")
    # audioUrl = input("Enter url to the audio (.wav) source:\n")

    #ENCODE & RETURN LENGTH OF TEXT: ~~~~~
    textLength = phaseEncoding()

    #DECODE & PRINT EXTRACTED TEXT: ~~~~~
    text = revertPhaseEncoding("encoded_audio.wav", textLength)
    print("Decoded text is:", text)