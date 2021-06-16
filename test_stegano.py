import wave

# read wave audio file
song = wave.open("sample.wav", mode='rb')
# Read frames and convert to byte array
frame_bytes = bytearray(list(song.readframes(song.getnframes())))
print(frame_bytes[2]&243)
# The "secret" text message
string = 'Peter Parker is the Spiderman!'
string1 = 'Peter Parker is the Spiderman!'
print(len(string))
# Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
string = string + int((len(frame_bytes) - (len(string) * 8 * 8)) / 8) * '#'

# Convert text to bit array
bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))

print("Len String", len(string))
print("Len frame", len(frame_bytes))
print("Len bits", len(bits))
print(''.join([bin(ord(i)).lstrip('0b') for i in string1]))
print(''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string1]))
print("bits", bits[0:100])

print("frame_bytes 0", (frame_bytes[0] & 254) | bits[0])
print("frame_bytes 1", (frame_bytes[1] & 254) | bits[1])
print("frame_bytes 2", (frame_bytes[2] & 254) | bits[2])
print("frame_bytes 3", (frame_bytes[3] & 254) | bits[3])
print("frame_bytes 4", (frame_bytes[4] & 254) | bits[4])
# Replace LSB of each byte of the audio data by one bit from the text bit array
for i, bit in enumerate(bits):
    frame_bytes[i] = (frame_bytes[i] & 254) | bit
# print(frame_bytes[3] & 254)
# print((frame_bytes[0] & 254) | 0)
# print((frame_bytes[1] & 254) | 1)
# print((frame_bytes[2] & 254) | 0)
# print((frame_bytes[3] & 254) | 1)
# print((frame_bytes[4] & 254) | 0)
#
# print(bytes((frame_bytes[0] & 254) | 0))
# print(bytes((frame_bytes[1] & 254) | 1))
# print(bytes((frame_bytes[2] & 254) | 0))
# print(bytes((frame_bytes[3] & 254) | 1))
# print(bytes((frame_bytes[4] & 254) | 0))

# Get the modified bytes
frame_modified = bytes(frame_bytes)
print(frame_modified)

# Write bytes to a new wave audio file
with wave.open('sampleStego.wav', 'wb') as fd:
    fd.setparams(song.getparams())
    fd.writeframes(frame_modified)
song.close()
