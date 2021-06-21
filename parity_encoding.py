import wave


def decimalToBinary(n):
    return format(n, '08b')


def check_parity(value: list):
    countone = 0
    for i in value:
        if int(i) == 1:
            countone += 1
    if countone % 2 == 1:
        return 1
    else:
        return 0


# read wave audio file
song = wave.open("sample.wav", mode='rb')
# Read frames and convert to byte array
frame_bytes = bytearray(list(song.readframes(song.getnframes())))
# The "secret" text message
string = 'Peter Parker is the Spiderman!'
print(len(string))
binary = []
for i in frame_bytes:
    binary.append(decimalToBinary(i))

# Convert text to bit array
bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))
print(bits)
# Replace LSB of each byte of the audio data by one bit from the text bit array
split_individual_bit = []
for i in binary:
    for j in i:
        split_individual_bit.append(j)
print(len(frame_bytes))
print(len(split_individual_bit))
len_bits = len(bits)
length_split = len(split_individual_bit)
j = 0
n = 16

# print("begin", split_individual_bit[16:32][-1])
# split_individual_bit[31] = '1'
# print("change", split_individual_bit[16:32][-1])
# print(split_individual_bit[16:32])
# print(bits[0])
# print(bits[1])
print("check", check_parity(split_individual_bit[96:112]))
print("check1", check_parity(split_individual_bit[112:128]))
print(split_individual_bit[96:112])
print(split_individual_bit[112:128])
print(bits[6])
print(bits[7])
for i in range(0, length_split, n):
    if check_parity(split_individual_bit[i:i + n]) == 1:
        if bits[j] == 0:
            if (split_individual_bit[i:i + n][-1] == '1'):

                split_individual_bit[i + n - 1] = '0'
            else:
                print("yes", i + n)
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
print("after")
print(split_individual_bit[96:112])
print(split_individual_bit[112:128])
convert_back_binary = []
convert_binary = []
for i in range(0, length_split, 8):
    list_bit = split_individual_bit[i:i + 8]
    string = ''
    for j in list_bit:
        string += j
    convert_back_binary.append(string)
print(len(convert_back_binary))
for i in convert_back_binary:
    convert_binary.append(int(i, 2))

print(convert_binary[0:20])
print(binary[0:20])
final_byte = bytes(bytearray(convert_binary))
print(final_byte[0:50])
print(frame_bytes[0:50])
# Write bytes to a new wave audio file
with wave.open('sampleStegoo.wav', 'wb') as fd:
    fd.setparams(song.getparams())
    fd.writeframes(final_byte)
song.close()
