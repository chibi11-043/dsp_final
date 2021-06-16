import wave

# read wave audio file
song = wave.open("sample.wav", mode='rb')
# Read frames and convert to byte array
frame_bytes = bytearray(list(song.readframes(song.getnframes())))
# The "secret" text message
string = 'Peter Parker is the Spiderman!'
string1 = 'Peter Parker is the Spiderman!'

# Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
string = string + int((2 * len(frame_bytes) - (len(string) * 8 * 8)) / 8) * '#'

# Convert text to bit array
bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))
print(len(string))
print(len(bits))
print(''.join([bin(ord(i)).lstrip('0b') for i in string1]))
print(''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string1]))
print("bits", bits[0:100])
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
print(frame_modified)

# Write bytes to a new wave audio file
with wave.open('sampleStego.wav', 'wb') as fd:
    fd.setparams(song.getparams())
    fd.writeframes(frame_modified)
song.close()
