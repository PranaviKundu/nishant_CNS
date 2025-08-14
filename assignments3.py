def hamming_encode_8bit(data_byte):
    # Convert ASCII char to 8-bit binary
    data_bits = [int(b) for b in format(ord(data_byte), '08b')]

    # Set positions: parity bits at 1,2,4,8 (1-indexed)
    hamming = ['x'] * 12
    j = 0
    for i in range(1, 13):
        if i in [1, 2, 4, 8]:
            continue
        hamming[i - 1] = data_bits[j]
        j += 1

    # Calculate parity bits
    for i in [1, 2, 4, 8]:
        parity = 0
        for j in range(1, 13):
            if j & i and j != i:
                parity ^= int(hamming[j - 1])
        hamming[i - 1] = parity

    return ''.join(str(b) for b in hamming)


def hamming_decode_12bit(hamming_code):
    bits = [int(b) for b in hamming_code]
    error_pos = 0
    for i in [1, 2, 4, 8]:
        parity = 0
        for j in range(1, 13):
            if j & i:
                parity ^= bits[j - 1]
        if parity != 0:
            error_pos += i

    if error_pos != 0:
        print("Error detected at position:", error_pos)
        bits[error_pos - 1] ^= 1
        print("Corrected code:", ''.join(str(b) for b in bits))
    else:
        print("No error detected.")

    # Extract original 8 data bits
    data_bits = []
    for i in range(1, 13):
        if i not in [1, 2, 4, 8]:
            data_bits.append(bits[i - 1])

    char = chr(int(''.join(str(b) for b in data_bits), 2))
    return char


# Example usage
msg = "A"  # Single ASCII character
print("Original Character:", msg)

encoded = hamming_encode_8bit(msg)
print("Encoded with Hamming(12,8):", encoded)

# Simulate 1-bit error at position 5 (optional)
received = list(encoded)
received[4] = '1' if received[4] == '0' else '0'
received = ''.join(received)
print("Received (with error):", received)

decoded_char = hamming_decode_12bit(received)
print("Decoded Character:", decoded_char)
