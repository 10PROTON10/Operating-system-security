import socket
import mysql.connector


# Создания подключения между клиентом и сервером
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 11827))
sock.listen(10)


# Создание подключения к базе данных
def create_connection(host_name, user_name, user_password, name_database):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=name_database
        )
        print('Подключение к базе данных прошло успешно')
        return connection
    except mysql.connector.Error as error:
        print(f"Произошла ошибка '{error}'")
        return None


# Вход в аккаунт базы данных
connect = create_connection("localhost", "root", "GOLF380", "bos_laba_two")


# Проверка правильности логина и пароля пользователя
def authenticate(connection):
    login = connection.recv(32).decode()
    cur = connect.cursor()
    cur.execute(f"SELECT * FROM `account` WHERE `User_name` LIKE '{login}'")
    result = cur.fetchall()
    if len(result) == 0:
        connection.send('Неправильный логин пользователя. Аутентификация провалена, доступ запрещён!'.encode())
    else:
        login_bd, hash_bd, salt_bd = result[0][1], result[0][2], result[0][3]
        connection.sendall(salt_bd.encode())
        hash_key = connection.recv(256).decode()
        if login == login_bd and hash_key == hash_bd:
            print('Login: ', login, '\nHashkey: ', hash_key)
            connection.send('Аутентификация успешна, доступ получен!'.encode())
        elif login != login_bd:
            connection.send('Неправильный логин пользователя. Аутентификация провалена, доступ запрещён!'.encode())
        elif hash_key != hash_bd:
            connection.send('Неправильный пароль пользователя. Аутентификация провалена, доступ запрещён!'.encode())


# Регистрация нового аккаунта
def register_new_account(connect, login, hash_key, sal):
    try:
        cur = connect.cursor()
        query = "INSERT INTO account (User_name, Hash, Salt) VALUES (%s, %s, %s)"
        values = (login, hash_key, sal)
        cur.execute(query, values)
        connect.commit()
        connection.send(
            'Данные успешно получены\nДоступ в сессию получен\nЧтобы пользоваться возможностями, переподключитесь'.encode())
    except mysql.connector.Error as error:
        print(f"Произошла ошибка '{error}'")
        connection.send(f'Произошла ошибка: {error}'.encode())
        connection.send('Такой пользователь уже существует'.encode())


# Бесконечный цикл работы сервера
while True:
    connection, addr = sock.accept()
    print('Подключился пользователь', addr)
    connection.send('Выберите тип: \n 1-Вход, \n 2-Регистрация'.encode())
    choice = connection.recv(4)
    if choice.decode() == '1':
        print('Получен тип Вход')
        authenticate(connection)
    elif choice.decode() == '2':
        connection.send('Введите login\nВведите пароль'.encode())
        print('Получен тип Регистрация')
        login, hash_key, sal = connection.recv(16).decode(), connection.recv(256).decode(), connection.recv(256).decode()
        print('Login: ', login, '\nHash key: ', hash_key, '\nSalt: ', sal)
        register_new_account(connect, login, hash_key, sal)