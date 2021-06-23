import wave


def decode_lsb_1_bit(wavfile):
    song = wave.open(wavfile, mode='rb')
    # Convert audio to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    # Extract the LSB of each byte
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]

    # Convert byte array back to string
    string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
    # Cut off at the filler characters
    decoded = string.split("###")[0]

    # Print the extracted text
    print("Sucessfully decoded using LSB 1 bit: " + decoded)
    song.close()
    return decoded


# decode_lsb_1_bit('sampleStego.wav')
