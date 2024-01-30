import hashlib
import socket
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

def open_server(ip_address, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_address, port))
    server_socket.listen(1)
    client_socket, client_address = server_socket.accept()
    print(f"Connected with client: {client_address}")
    return client_socket

def hash_n_times(p, n, A):
    p_bytes = p.to_bytes((p.bit_length() + 7) // 8, byteorder='big')
    for _ in range(n - A + 1):
        p_bytes = hashlib.sha256(p_bytes).digest()
    return int.from_bytes(p_bytes, byteorder='big')

def set_value(file_path, section, key, value):
    config = configparser.RawConfigParser()
    config.read(file_path)
    config[section][key] = value
    with open(file_path, 'w') as cfgfile:
        config.write(cfgfile)

def process_verification(client_socket, hash_reg, secret, N_times, accounts):
    max_attempts = 5
    login_attempts = 1

    while login_attempts <= max_attempts:
        A = accounts[str(config['database']['login'])]
        old_A = None

        if old_A != A:
            old_A = A
            client_socket.send(str(A).encode())
            hashed = int(client_socket.recv(1024).decode())
            hashed = hash_n_times(hashed, 0, 0)
            if hashed == secret:
                print(hashed, secret, A)
                msg = 'Success'
                client_socket.send(msg.encode())
                print(accounts)
                A += 1
                set_value('config.ini', 'database', 'A_number', str(A))
                set_value('config.ini', 'database', 'hashed', str(hashed))
                secret = hash_n_times(hash_reg, N_times, A)
                login_attempts = 1
                return True
            else:
                msg = 'Fail'
                print(msg)
                client_socket.send(msg.encode())
                login_attempts += 1

    print('Количество попыток закончилось')
    return False

if __name__ == "__main__":
    client_socket = open_server("localhost", 12225)
    hash_reg = int(client_socket.recv(1024).decode())
    N_times = 100000
    accounts = {str(config['database']['login']): int(config['database']['a_number'])}
    secret = hash_n_times(hash_reg, N_times, accounts[str(config['database']['login'])])

    if process_verification(client_socket, hash_reg, secret, N_times, accounts):
        print('Аутентификация успешна')
    else:
        print('Аутентификация не удалась')




