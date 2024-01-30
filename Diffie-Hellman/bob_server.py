import sympy
import socket


def open_server(ip_address, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_address, port))
    server_socket.listen(1)
    return server_socket


def generate_secret_key():
    secret_key = sympy.randprime(2 ** 15, 2 ** 16 - 1)
    print(f'Generated a secret key -> {secret_key}')
    return secret_key


def generate_open_key(n):
    open_key = sympy.randprime(1, n)
    print(f'Generated a public key -> {open_key}')
    return open_key


def create_part_key(public_key_a, public_key, secret_key):
    part_key = public_key_a ** secret_key % public_key
    print(f'Generated a partial key -> {part_key}')
    return part_key


def create_full_key(part_key_a, secret_key, public_key):
    full_key = part_key_a ** secret_key % public_key
    print(f'Generated full key -> {full_key}')
    return full_key


def encrypt(key):
    encrypted_message = ""
    message = 'Operating system security - protocol Diffie-Hellman'
    for symbol in message:
        encrypted_message += chr(ord(symbol) + key)
    print(f'Encrypted this message -> {message}')
    return encrypted_message


def decipher(encrypted_message, key):
    message = ""
    print(f"Deciphering this message -> {encrypted_message}")
    for symbol in encrypted_message:
        message += chr(ord(symbol) - key)
    print(f"Decrypted message -> {message}")
    return message


if __name__ == "__main__":
    ip_address = 'localhost'
    port = 6670
    server_socket = open_server(ip_address, port)
    client_socket, client_address = server_socket.accept()

    secret_key = generate_secret_key()
    public_key = generate_open_key(secret_key)

    public_key_A = int(client_socket.recv(2048).decode())
    print(f"Receive -> {public_key_A}")

    client_socket.send(str(public_key).encode())
    print(f"Sent -> {public_key}")

    part_key_B = create_part_key(public_key_A, public_key, secret_key)
    client_socket.send(str(part_key_B).encode())
    print(f"Sent -> {part_key_B}")

    part_key_A = int(client_socket.recv(2048).decode())
    print(f"Receive -> {part_key_A}")

    full_key_B = create_full_key(part_key_A, secret_key, public_key)
    encrypted_message = encrypt(full_key_B)
    client_socket.send(str(encrypted_message).encode())
    print(f"Sent -> {encrypted_message}")

    encrypted_message_A = client_socket.recv(2048).decode()
    print(f"Received -> {encrypted_message_A}")

    decrypted_message_A = decipher(encrypted_message_A, full_key_B)
