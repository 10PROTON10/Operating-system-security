import sympy
import socket


def connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip_address, port)
    client_socket.connect(server_address)
    return client_socket


def secret_key():
    secret_key = sympy.randprime(2 ** 15, 2 ** 16 - 1)
    print(f'Generated a secret key -> {secret_key}')
    return secret_key


def open_key(n):
    open_key = sympy.randprime(1, n)
    print(f'Generated a public key -> {open_key}')
    return open_key


def create_part_key(public_key, public_key_b, secret_key):
    part_key = public_key ** secret_key % public_key_b
    print(f'Generated a partial key -> {part_key}')
    return part_key


def create_full_key(part_key_b, secret_key, public_key_b):
    full_key = part_key_b ** secret_key % public_key_b
    print(f'Generated full key -> {full_key}')
    return full_key


def encrypt(key):
    encrypted_message = ""
    message = 'Diffie-Hellman protocol'
    for symbol in message:
        encrypted_message += chr(ord(symbol) + key)
    print(f'Encrypted this message -> {message}')
    return encrypted_message


def decipher(key, decipher_message):
    message = ""
    print(f"Deciphering this message -> {decipher_message}")
    for symbol in decipher_message:
        message += chr(ord(symbol) - key)
    print(f"Decrypted message -> {message}")
    return message


if __name__ == "__main__":
    ip_address = 'localhost'
    port = 6670
    client_socket = connect()

    secret_key = secret_key()
    public_key = open_key(secret_key)

    client_socket.send(str(public_key).encode())
    print(f"Sent -> {public_key}")

    public_key_B = int(client_socket.recv(2048).decode())
    print(f"Receive -> {public_key_B}")

    part_key_A = create_part_key(public_key, public_key_B, secret_key)
    client_socket.send(str(part_key_A).encode())
    print(f"Sent -> {part_key_A}")

    part_key_B = int(client_socket.recv(2048).decode())
    print(f"Receive -> {part_key_B}")

    full_key = create_full_key(part_key_B, secret_key, public_key_B)
    encrypted_message = encrypt(full_key)
    client_socket.send(str(encrypted_message).encode())
    print(f"Sent -> {encrypted_message}")

    decipher_message = client_socket.recv(2048).decode()
    print(f"Receive -> {decipher_message}")

    decrypted_message = decipher(full_key, decipher_message)


