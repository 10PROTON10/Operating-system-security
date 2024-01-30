import hashlib
import configparser
import socket

config = configparser.ConfigParser()
config.read("config.ini")

def hash_password(login, password):
    P_hex = hashlib.sha256((login + password).encode()).hexdigest()
    p = int(P_hex, 16)
    return p

def hash_n_times(p, n):
    p_bytes = p.to_bytes((p.bit_length() + 7) // 8, byteorder='big')
    for _ in range(n):
        p_bytes = hashlib.sha256(p_bytes).digest()
    return int.from_bytes(p_bytes, byteorder='big')

def conn_server(ip_address, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip_address, port)
    client_socket.connect(server_address)
    return client_socket

def main():
    N_times = 100000
    max_attempts = 5
    counter_ident = max_attempts
    cnt = 1
    A = None

    while cnt <= counter_ident:
        received_message = client_socket.recv(1024).decode()
        A = int(received_message)

        enter_login, enter_password = input('Enter login >>> '), input('Enter password >>> ')
        hashed = hash_password(enter_login, enter_password)

        if A is not None:
            na_times = N_times - A
            hashed = hash_n_times(hashed, na_times)
            client_socket.send(str(hashed).encode())

            answer = client_socket.recv(64).decode()
            print(f"Попытка номер {cnt} - {answer}")

            if answer == 'Success':
                cnt = 1
                break
            else:
                cnt += 1
                print(f'Попыток осталось: {counter_ident - cnt + 1}')

    if cnt > counter_ident:
        print('Количество попыток закончилось')

if __name__ == '__main__':
    login = str(config['database']['login'])
    password = str(config['database']['password'])
    p = hash_password(login, password)

    client_socket = conn_server("localhost", 12225)
    client_socket.send(str(p).encode())
    main()




