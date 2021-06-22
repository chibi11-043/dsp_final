import wave


def decode_lsb_2_bit(wavfile):
    song = wave.open(wavfile, mode='rb')

    # Convert audio to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    extracted = []
    for i in range(len(frame_bytes)):
        frame_bytes[i] = frame_bytes[i] % 4
        if frame_bytes[i] == 0:
            extracted.append(0)
            extracted.append(0)
        elif frame_bytes[i] == 1:
            extracted.append(0)
            extracted.append(1)
        elif frame_bytes[i] == 2:
            extracted.append(1)
            extracted.append(0)
        elif frame_bytes[i] == 3:
            extracted.append(1)
            extracted.append(1)
    string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))

    # Cut off at the filler characters
    decoded = string.split("###")[0]

    # Print the extracted text
    print("Sucessfully decoded: " + decoded)
    song.close()
    return decoded


# decode_lsb_2_bit('LSB1Bit.wav')
