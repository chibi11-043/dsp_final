import wave
import os


def encode_lsb_1_bit(wavfile, textfile, save_path, file_name):
    # read wave audio file
    song = wave.open(wavfile, mode='rb')
    # Read frames and convert to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    f = open(textfile, "r")
    string = f.read()
    f.close()
    # Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
    string = string + int((len(frame_bytes) - (len(string) * 8 * 8)) / 8) * "#"

    # Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))
    # Replace LSB of each byte of the audio data by one bit from the text bit array
    for i, bit in enumerate(bits):
        # print(frame_bytes[i])
        frame_bytes[i] = (frame_bytes[i] - (frame_bytes[i] % 2) + bit)
    frame_modified = bytes(frame_bytes)

    complete_name = os.path.join(save_path, file_name)
    print(complete_name)
    # Write bytes to a new wave audio file
    with wave.open(complete_name + ".wav", 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    song.close()


# encode_lsb_1_bit('sample.wav', 'text.txt')

