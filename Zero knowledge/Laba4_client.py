from socket import socket, AF_INET, SOCK_STREAM
from random import randint
from math import gcd
from time import time


def connect_to_server(ip_address, port):
    client_socket = socket(AF_INET, SOCK_STREAM)
    server_address = (ip_address, port)
    client_socket.connect(server_address)
    return client_socket


def find_coprime(n):
    while True:
        x = randint(1, n - 1)
        if gcd(x, n) == 1:
            return x


def run():
    counter = 1
    while counter < ROUNDS:
        rand_r = randint(1, n - 1)
        x = pow(rand_r, 2, n)
        client_socket.send(str(x).encode())
        bit_e = int(client_socket.recv(2).decode())
        if bit_e == 0:
            y = rand_r
        elif bit_e == 1:
            y = rand_r * pow(secret, bit_e, n)
        client_socket.send(str(y).encode())
        msg = client_socket.recv(32).decode()
        print(f"Session #{counter} >>> " + msg)
        counter += 1
    print(f"Completed in {time() - startTime} seconds.")


if __name__ == "__main__":
    IP_ADDRESS = 'localhost'
    PORT = 12331
    ROUNDS = 21
    client_socket = connect_to_server(IP_ADDRESS, PORT)
    startTime = time()
    client_socket.send(str(ROUNDS).encode())
    n = int(client_socket.recv(2048).decode())
    secret = find_coprime(n)
    v = pow(secret, 2, n)
    client_socket.send(str(v).encode())
    run()