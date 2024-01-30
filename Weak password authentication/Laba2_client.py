import socket
import hashlib
import configparser
from salt import main


config = configparser.ConfigParser()
config.read('Laba2_config.ini')

# Выбор операции
choice = config['selection']['choice_operation']

# Для подключения существующего пользователя с правильными данными
# login = config['valid_user']['correct_login']
# password = config['valid_user']['correct_password']

# Для подключения существующего пользователя с неправильным логином
login = config['invalid_login']['invalid_login']
password = config['invalid_login']['correct_password']

# Для подключения существующего пользователя с неправильным паролем
# login = config['invalid_password']['correct_login']
# password = config['invalid_password']['invalid_password']

# Регистрация нового пользователя с новыми данными
# register_login = config['registration_of_a_nonexistent_name']['new_correct_login']
# register_password = config['registration_of_a_nonexistent_name']['new_correct_password']

# Регистрация пользователя с существующим логином
register_login = config['registering_an_existing_login']['old_login']
register_password = config['registering_an_existing_login']['new_correct_password']

# Регистрация пользователя с существующим паролем
# register_login = config['registering_an_existing_password']['new_correct_login']
# register_password = config['registering_an_existing_password']['old_password']

# Создания подключения между клиентом и сервером
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 11827))


flag = False
while True:
    data = sock.recv(512).decode()
    sock.send(choice.encode())
    print(data)
    if choice == '1' and not flag:
        print('Мой выбор:', choice)
        sock.send(login.encode())
        sal = bytearray(sock.recv(512))
        hash_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), sal, 100000).hex()
        sock.send(hash_key.encode())
        print('Login', login, '\nPassword', password, '\nHash:', hash_key)
        flag = True

    elif choice == '2' and not flag:
        print('Мой выбор: ', choice)
        data = sock.recv(512)
        print(data.decode())
        new_login, new_password = register_login, register_password
        print('Login: ', new_login)
        print('Password: ', new_password)
        sol = main()
        new_hash_key = hashlib.pbkdf2_hmac('sha256', new_password.encode('utf-8'), sol, 100000).hex()
        sock.send(new_login.encode())
        sock.send(new_hash_key.encode())
        sock.send(sol)
        flag = True


