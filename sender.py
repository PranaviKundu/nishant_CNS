import socket
import random

def hamming_encode_8bit(char):
    data_bits = [int(b) for b in format(ord(char), '08b')]
    hamming = ['x'] * 12

    j = 0
    for i in range(1, 13):
        if i in [1, 2, 4, 8]:
            continue
        hamming[i - 1] = data_bits[j]
        j += 1

    for i in [1, 2, 4, 8]:
        parity = 0
        for j in range(1, 13):
            if j & i:
                if hamming[j - 1] != 'x':
                    parity ^= int(hamming[j - 1])
        hamming[i - 1] = parity

    return ''.join(str(b) for b in hamming)

def introduce_error(encoded):
    pos = random.randint(0, 11)
    print("Introducing error at bit position (1-indexed):", pos + 1)
    corrupted = list(encoded)
    corrupted[pos] = '1' if corrupted[pos] == '0' else '0'
    return ''.join(corrupted)

# SOCKET CLIENT
client = socket.socket()
client.connect(('127.0.0.39', 9999))

letter = input("Enter a single ASCII character to send: ")
encoded = hamming_encode_8bit(letter)
print("Hamming Encoded:", encoded)

# Simulate error
simulate = input("Simulate 1-bit error? (y/n): ")
if simulate.lower() == 'y':
    encoded = introduce_error(encoded)

client.send(encoded.encode())
print("Sent Hamming Code:", encoded)

client.close()
