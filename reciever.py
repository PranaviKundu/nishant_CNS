import socket

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
        print("Corrected Hamming Code:", ''.join(str(b) for b in bits))
    else:
        print("No error detected.")

    # Extract original 8 data bits from positions not in 1,2,4,8
    data_bits = []
    for i in range(1, 13):
        if i not in [1, 2, 4, 8]:
            data_bits.append(str(bits[i - 1]))

    ascii_char = chr(int(''.join(data_bits), 2))
    return ascii_char

# SOCKET SERVER
server = socket.socket()
server.bind(('127.0.0.39', 9999))
server.listen(1)
print("Receiver listening on 127.0.0.39:9999...")

conn, addr = server.accept()
print("Connected by", addr)

data = conn.recv(1024).decode()
print("Received Hamming Code:", data)

decoded_char = hamming_decode_12bit(data)
print("Decoded ASCII character:", decoded_char)

conn.close()
