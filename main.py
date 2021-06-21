import wave

#convert decimal to binary
def decimalToBinary(n):
    return bin(n).replace("0b", "")

#check if the list has even or odd number of 1s
def check_parity(value: list):
    countone = 0
    for i in value:
        if int(i) == 1:
            countone += 1
    if countone % 2 == 1:
        return 1
    else:
        return 0

#encode using lsb 1 bit
def encode_lsb_1_bit(filename):
    # read wave audio file
    song = wave.open(filename, mode='rb')
    # Read frames and convert to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    # The "secret" text message
    string = 'Peter Parker is the Spiderman!'
    # Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
    string = string + int((len(frame_bytes) - (len(string) * 8 * 8)) / 8) * '#'

    # Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))
    # Replace LSB of each byte of the audio data by one bit from the text bit array
    for i, bit in enumerate(bits):
        # print(frame_bytes[i])
        frame_bytes[i] = (frame_bytes[i] - (frame_bytes[i] % 2) + bit)
    frame_modified = bytes(frame_bytes)

    # Write bytes to a new wave audio file
    with wave.open('sampleStego.wav', 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    song.close()

#decode using lsb 1 bit
def decode_lsb_1_bit(filename):
    song = wave.open(filename, mode='rb')
    # Convert audio to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    # Extract the LSB of each byte
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]

    # Convert byte array back to string
    string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
    # Cut off at the filler characters
    decoded = string.split("###")[0]

    # Print the extracted text
    print("Sucessfully decoded: " + decoded)
    song.close()

#encode using lsb 2 bit
def encode_lsb_2_bit(filename):
    # read wave audio file
    song = wave.open(filename, mode='rb')
    # Read frames and convert to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    # The "secret" text message
    string = 'Peter Parker is the Spiderman!'

    # Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
    string = string + int((2 * len(frame_bytes) - (len(string) * 8 * 8)) / 8) * '#'

    # Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))
    # Replace LSB of each byte of the audio data by one bit from the text bit array
    j = 0
    for i in range(0, len(frame_bytes), 2):
        frame_bytes[j] = (frame_bytes[j] - (frame_bytes[j] % 4))
        if bits[i] == 0 and bits[i + 1] == 0:
            frame_bytes[j] += 0
        elif bits[i] == 0 and bits[i + 1] == 1:
            frame_bytes[j] += 1
        elif bits[i] == 1 and bits[i + 1] == 0:
            frame_bytes[j] += 2
        else:
            frame_bytes[j] += 3
        j = j + 1
    frame_modified = bytes(frame_bytes)

    # Write bytes to a new wave audio file
    with wave.open('sampleStego.wav', 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    song.close()

#decode using lsb 2 bit
def decode_lsb_2_bit(filename):
    song = wave.open(filename, mode='rb')

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

#encode using parity coding
def parity_encoding(filename):
    # read wave audio file
    song = wave.open(filename, mode='rb')
    # Read frames and convert to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    # The "secret" text message
    string = 'Peter Parker is the Spiderman!'
    binary = []
    for i in frame_bytes:
        binary.append(decimalToBinary(i))

    # Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))

    # split binary string to each individual 1 or 0

    split_individual_bit = []
    for i in binary:
        for j in i:
            split_individual_bit.append(j)
    len_bits = len(bits)
    length_split = len(split_individual_bit)
    j = 0
    n = 16

    #parity embedding
    for i in range(0, length_split, n):
        if check_parity(split_individual_bit[i:i + n]) == 1:
            if bits[j] == 0:
                if (split_individual_bit[i:i + n][-1] == '1'):

                    split_individual_bit[i + n - 1] = '0'
                else:
                    split_individual_bit[i + n - 1] = '1'
        elif check_parity(split_individual_bit[i:i + n]) == 0:
            if bits[j] == 1:
                if (split_individual_bit[i:i + n][-1] == '1'):
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

    # Write bytes to a new wave audio file
    with wave.open('sampleStegoo.wav', 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(final_byte)
    song.close()

def decoding_parity(filename):
    songg = wave.open(filename, mode='rb')
    # Convert audio to byte array
    frame_bytes = bytearray(list(songg.readframes(songg.getnframes())))
    binary = []
    for i in frame_bytes:
        binary.append(decimalToBinary(i))
    split_individual_bit = []
    for i in binary:
        for j in i:
            split_individual_bit.append(j)
    length_split = len(split_individual_bit)
    string_decode = []
    n = 16
    for i in range(0, length_split, n):
        if (i == 240 * n):
            break
        if check_parity(split_individual_bit[i:i + n]) == 1:
            string_decode.append('1')
        else:
            string_decode.append('0')

    # Convert byte array back to string
    string = "".join(chr(int("".join(map(str, string_decode[i:i + 8])), 2)) for i in range(0, len(string_decode), 8))
    # Print the extracted text
    print("Sucessfully decoded: " + string)
    songg.close()


if __name__ == "__main__":
    encode_lsb_1_bit("sample.wav")
    decode_lsb_1_bit("sampleStego.wav")
    encode_lsb_2_bit("sample.wav")
    decode_lsb_2_bit("sampleStego.wav")
    parity_encoding("sample.wav")
    decoding_parity("sampleStegoo.wav")