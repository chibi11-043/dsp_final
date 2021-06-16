import wave

# read wave audio file
song = wave.open("sample.wav", mode='rb')
# Read frames and convert to byte array
frame_bytes = bytearray(list(song.readframes(song.getnframes())))
print(frame_bytes[2] & 243)
# The "secret" text message
string = 'Peter Parker is the Spiderman!'
string1 = 'Peter Parker is the Spiderman!'
print(len(string))
# Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
string = string + int((len(frame_bytes) - (len(string) * 8 * 8)) / 8) * '#'


# Convert text to bit array
bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))
print(len(string))
print(len(bits))
print(''.join([bin(ord(i)).lstrip('0b') for i in string1]))
print(''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string1]))
print("bits", bits[0:100])

# Replace LSB of each byte of the audio data by one bit from the text bit array
for i, bit in enumerate(bits):
    # print(frame_bytes[i])
    frame_bytes[i] = (frame_bytes[i] - (frame_bytes[i] % 2) + bit)
frame_modified = bytes(frame_bytes)
print(frame_modified)

# Write bytes to a new wave audio file
with wave.open('sampleStego.wav', 'wb') as fd:
    fd.setparams(song.getparams())
    fd.writeframes(frame_modified)
song.close()
