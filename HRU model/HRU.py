import json
import os
from pathlib import Path


db_path = Path("database.json")


def load_db():
    if os.path.exists(db_path):
        with open(db_path, "r") as f:
            return json.load(f)
    else:
        return {
            "subjects": {},
            "objects": {},
            "access_matrix": {}
        }


def save_db(db):
    with open(db_path, "w") as f:
        json.dump(db, f)


def create_subject(db, subj):
    if subj not in db["subjects"]:
        db["subjects"][subj] = {}
        db["access_matrix"][subj] = {}
        print("Субъект создан.")
    else:
        print("Субъект уже существует.")


def create_object(db, obj):
    if obj not in db["objects"]:
        db["objects"][obj] = {}
        for subj in db["access_matrix"]:
            db["access_matrix"][subj][obj] = []
        print("Объект создан.")
    else:
        print("Объект уже существует.")


def delete_subject(db, subj):
    if subj not in db["subjects"]:
        print("Субъект не существует.")
        return
    for obj in db["objects"]:
        if subj in db["access_matrix"] and obj in db["access_matrix"][subj]:
            del db["access_matrix"][subj]
            del db["subjects"][subj]
    print("Субъект удалён.")


def delete_object(db, obj):
    if obj not in db["objects"]:
        print("Объект не существует.")
        return
    for subj in db["access_matrix"]:
        if obj in db["access_matrix"][subj]:
            del db["access_matrix"][subj][obj]
    del db["objects"][obj]
    print("Объект удалён.")


def add_right(db, subj, obj, right):
    if subj not in db["subjects"]:
        print("Субъект не существует.")
        return
    if obj not in db["objects"]:
        print("Объект не существует.")
        return
    if right not in ["r", "w", "x", "o"]:
        print("Недействительное право.")
        return
    if subj not in db["access_matrix"]:
        db["access_matrix"][subj] = {}
    if obj not in db["access_matrix"][subj]:
        db["access_matrix"][subj][obj] = []
    if right not in db["access_matrix"][subj][obj]:
        db["access_matrix"][subj][obj].append(right)
    print("Право добавлено.")


def delete_right(db, subj, obj, right):
    if subj not in db["subjects"]:
        print("Субъект не существует.")
        return
    if obj not in db["objects"]:
        print("Объект не существует.")
        return
    if right not in ["r", "w", "x", "o"]:
        print("Недействительное право.")
        return
    if subj in db["access_matrix"] and obj in db["access_matrix"][subj] and right in db["access_matrix"][subj][obj]:
        db["access_matrix"][subj][obj].remove(right)
        print("Право удалено.")
    else:
        print("Субъект не имеет указанного права на объект.")


def create_file(db, subj, obj, current_user):
    if obj in db["objects"]:
        print("Объект уже существует.")
        return
    if subj not in db["subjects"]:
        print("Субъект не существует.")
        return
    if current_user != subj:
        print("Вы можете создать файл только для себя.")
        return

    create_subject(db, subj)
    create_object(db, obj)

    rights = ["r", "w", "x", "o"]
    for right in rights:
        add_right(db, subj, obj, right)

    print("Файл создан.")


def delete_file(db, subj, obj, current_user):
    if obj not in db["objects"]:
        print("Объект не существует.")
        return
    if subj not in db["access_matrix"]:
        print("Субъекта нет в матрице доступа.")
        return
    if obj not in db["access_matrix"][subj]:
        print("Объекта нет в матрице доступа.")
        return
    if subj != current_user:
        print("Вы можете удалить только свои собственные файлы.")
        return

    delete_subject(db, obj)
    delete_object(db, obj)

    if subj in db["access_matrix"] and obj in db["access_matrix"][subj]:
        subj_rights = db["access_matrix"][subj][obj]
        for right in ["r", "w", "x", "o"]:
            if right in subj_rights:
                delete_right(db, subj, obj, right)

    print("Файл удален.")


def grant_right(db, s1, s2, obj, right, current_user):
    if s1 not in db["subjects"]:
        print("Субъект не существует.")
        return
    if s2 not in db["subjects"]:
        print("Субъект не существует.")
        return
    if obj not in db["objects"]:
        print("Объект не существует.")
        return
    if right not in ["r", "w", "x", "o"]:
        print("Недействительное право.")
        return
    if right not in db["access_matrix"][s1][obj]:
        print("Субъект не имеет указанного права на объект.")
        return
    if obj not in db["access_matrix"][s2]:
        print("Субъект не имеет доступа к объекту.")
        return
    if current_user != s1:
        print("Вы можете предоставлять права только от себя.")
        return

    if right == "o":
        add_right(db, s2, obj, right)
    else:
        add_right(db, s2, obj, right)
        db["access_matrix"][s1][obj].remove(right)
    print("Право передано от {} к {} на {} с правом {}".format(s1, s2, obj, right))


def display_db(db):
    users = db['subjects'].keys()
    objects = db['objects'].keys()

    print('Access Matrix:\n')
    print('\t', end='')
    print('\t'.join(objects))

    for user in users:
        print(user, '\t', end='')
        for obj in objects:
            rights = db['access_matrix'].get(user, {}).get(obj, '-')
            print(rights, '\t', end='')
        print()


# def get_user_files(db, current_user):
#     user_files = []
#     if current_user in db["access_matrix"]:
#         for obj in db["objects"]:
#             if obj in db["access_matrix"][current_user]:
#                 user_files.append(obj)
#     return user_files
def get_user_files(db, current_user):
    user_files = []
    if current_user in db["access_matrix"]:
        for obj in db["objects"]:
            if obj in db["access_matrix"][current_user] and "o" in db["access_matrix"][current_user][obj]:
                user_files.append(obj)
    return user_files


def help():
    print("Commands:\n"
          "help - Отображение доступных команд для ввода\n"
          "print - Отображение матрицы доступа\n"
          "exit - Выход\n"
          "register - Регистрация\n"
          "login - Вход\n"
          "logout - Выход из аккаунта\n"
          "create_file subj obj - Создание персонального файла для субъекта на объект со всеми правами\n"
          "delete_file subj obj - Удаление персонального файла для субъекта на объект со всеми правами\n"
          "grant_right s1 s2 obj right - Передача права от одного субъекта к другому\n"
          "user_files - Просмотр файлов, к которым у вас есть доступ\n"
          )


def register(db):
    username = input("Введите логин: ")
    if username in db["subjects"]:
        print("Имя пользователя уже существует.")
        return
    password = input("Введите пароль: ")
    db["subjects"][username] = {"password": password}
    db["access_matrix"][username] = {}
    print("Регистрация успешна.")


def login(db):
    username = input("Введите логин: ")
    if username not in db["subjects"]:
        print("Логин не найден.")
        return
    password = input("Введите пароль: ")
    if db["subjects"][username]["password"] == password:
        print("Авторизация успешна.")
        return username
    else:
        print("Не корректный пароль.")


def logout(current_user):
    if current_user is None:
        print("В данный момент ни один пользователь не вошел в систему.")
    else:
        print("Успешно вышел из системы.")
    return None


def command_executor(db, command, current_user):
    if command == "help":
        help()
    elif command == "print":
        display_db(db)
    elif command == "user_files":
        if current_user is None:
            print("Пожалуйста, сначала войдите в систему.")
        else:
            user_files = get_user_files(db, current_user)
            print("Файлы, к которым у вас есть доступ:")
            for file in user_files:
                print(file)
    elif command == "register":
        register(db)
    elif command == "login":
        current_user = login(db)
    elif command == "logout":
        current_user = logout(current_user)
    elif command == "grant_right":
        if current_user is None:
            print("Пожалуйста, сначала войдите в систему.")
        else:
            s1 = str(input("Напишите имя субъекта, от которого нужно передать права: "))
            s2 = str(input("Напишите имя субъекта, которому нужно передать права: "))
            print('Объекты, к которым у вас есть доступ', get_user_files(db, current_user))
            obj = str(input("Напишите название объекта: "))
            if obj in get_user_files(db, current_user):
                right = str(input("Напишите право: "))
                grant_right(db, s1, s2, obj, right, current_user)
            else:
                print("У вас нет доступа к данному объекту.")
    elif command == "create_file":
        if current_user is None:
            print("Пожалуйста, сначала войдите в систему.")
        else:
            subj = str(input("Напишите имя субъекта: "))
            obj = str(input("Напишите имя объекта: "))
            create_file(db, subj, obj, current_user)
    elif command == "delete_file":
        if current_user is None:
            print("Пожалуйста, сначала войдите в систему.")
        else:
            subj = str(input("Напишите имя субъекта: "))
            obj = str(input("Напишите имя объекта: "))
            delete_file(db, subj, obj, current_user)
    else:
        print("Команда не найдена. Введите help для получения списка доступных команд.")

    return current_user


def main():
    db = load_db()
    current_user = None

    print("Введите help для получения списка доступных команд.")

    while True:
        command = input(">> ")
        save_db(db)
        if command == "exit":
            break
        else:
            current_user = command_executor(db, command, current_user)


if __name__ == "__main__":
    main()