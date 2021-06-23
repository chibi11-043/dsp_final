import wave
import os
import time


def decimalToBinary(n):
    return format(n, '08b')


def check_parity(value: list):
    countOne = 0
    for i in value:
        if int(i) == 1:
            countOne += 1
    if countOne % 2 == 1:
        return 1
    else:
        return 0


def encode_parity(wavfile, textfile, save_path, file_name):
    start = time.time()
    # read wave audio file
    song = wave.open(wavfile, mode='rb')
    # Read frames and convert to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    # convert the byte array to binary
    binary = []
    for i in frame_bytes:
        binary.append(decimalToBinary(i))

    # Split the binary list to 0 or 1
    split_individual_bit = []
    for i in binary:
        for j in i:
            split_individual_bit.append(j)
    length_split = len(split_individual_bit)

    f = open(textfile, "r")
    string = f.read()
    f.close()
    string1 = ""

    # Padding preprocess
    total = int(len(split_individual_bit) / 1600)
    string = string + int(total - len(string)) * "#"

    # Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))
    len_bits = len(bits)
    j = 0
    n = 200

    for i in range(0, length_split, n):
        if check_parity(split_individual_bit[i:i + n]) == 1:
            if bits[j] == 0:
                if split_individual_bit[i:i + n][-1] == '1':
                    split_individual_bit[i + n - 1] = '0'
                else:
                    split_individual_bit[i + n - 1] = '1'
        elif check_parity(split_individual_bit[i:i + n]) == 0:
            if bits[j] == 1:
                if split_individual_bit[i:i + n][-1] == '1':
                    split_individual_bit[i + n - 1] = '0'
                else:
                    split_individual_bit[i + n - 1] = '1'
        j += 1
        if j == len_bits:
            break

    convert_back_binary = []
    convert_binary = []
    for i in range(0, length_split, 8):
        list_bit = split_individual_bit[i:i + 8]
        string = ''
        for j in list_bit:
            string += j
        convert_back_binary.append(string)
    for i in convert_back_binary:
        convert_binary.append(int(i, 2))
    final_byte = bytes(bytearray(convert_binary))

    complete_name = os.path.join(save_path, file_name)
    print(complete_name)
    # Write bytes to a new wave audio file
    with wave.open(complete_name + ".wav", 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(final_byte)
    song.close()

    print("it took", time.time() - start, "seconds to encode")

# encode_parity('sample.wav', 'text.txt')
