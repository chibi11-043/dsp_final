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



# Replace LSB of each byte of the audio data by one bit from the text bit array
songg = wave.open("sampleStego.wav", mode='rb')
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

print(string_decode)
print(len(string_decode))
# Convert byte array back to string
string = "".join(chr(int("".join(map(str, string_decode[i:i + 8])), 2)) for i in range(0, len(string_decode), 8))
decoded = string.split("###")[0]
# Print the extracted text
print("Sucessfully decoded: " + decoded)
songg.close()
