from socket import socket, AF_INET, SOCK_STREAM
from BBS import numbers_simple
from BBS import generate_e


def open_server(ip_address, port):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((ip_address, port))
    server_socket.listen(1)
    print('Сервер работает корректно')
    connection, addr = server_socket.accept()
    print(f"Подключился >>> {addr}")
    return connection


def generation_n():
    p, q = numbers_simple()
    return p * q


def run():
    false = True
    count = 1
    while false:
        x = int(server_socket.recv(2048).decode())
        bit_e = generate_e()
        server_socket.send(str(bit_e).encode())
        y = int(server_socket.recv(2048).decode())
        verification = x * pow(v, int(bit_e)) % n
        if pow(y, 2, n) == verification:
            msg = 'Accept'
        else:
            msg = 'Fail'
        server_socket.send(str(msg).encode())
        count += 1
        if count == ROUNDS:
            print('Количество попыток израсходовано')
            break


if __name__ == "__main__":
    IP_ADDRESS = 'localhost'
    PORT = 12331
    server_socket = open_server(IP_ADDRESS, PORT)
    ROUNDS = int(server_socket.recv(2048).decode())
    n = generation_n()
    server_socket.send(str(n).encode())
    v = int(server_socket.recv(2048).decode())
    run()