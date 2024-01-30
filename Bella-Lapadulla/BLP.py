import configparser
import csv
import json


def load_object_secrecy_levels(filename):
    object_secrecy_levels = {}
    with open(filename, 'r') as file:
        section = None
        for line in file:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1]
            else:
                parts = line.split('=')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                key = key.strip()
                value = value.strip()
                if section not in object_secrecy_levels:
                    object_secrecy_levels[section] = {}
                object_secrecy_levels[section][key] = value
    return object_secrecy_levels


def load_subject_secrecy_levels(filename):
    subject_secrecy_levels = {}
    with open(filename, 'r') as file:
        section = None
        for line in file:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1]
            else:
                parts = line.split('=')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if section not in subject_secrecy_levels:
                        subject_secrecy_levels[section] = {}
                    subject_secrecy_levels[section][key] = value
    return subject_secrecy_levels



def subjects_info(subject_secrecy_levels):
    with open('subjects.ini', 'w') as file:
        for subject, levels in subject_secrecy_levels.items():
            file.write(f"[{subject}]\n")
            for key, value in levels.items():
                file.write(f"{key} = {value}\n")


def register_user(login, password):
    if login in subject_secrecy_levels:
        print("Пользователь с таким логином уже зарегистрирован.")
    else:
        subject_secrecy_levels[login] = {
            'secrecyLevel': 'null',
            'tempSecrecyLevel': 'null',
            'password': password
        }
        subjects_info(subject_secrecy_levels)
        access_matrix[login] = {}
        for object_name in object_secrecy_levels:
            access_matrix[login][object_name] = []
        with open('database.json', 'r') as file:
            data = json.load(file)
        data['matrix'][login] = access_matrix[login]
        with open('database.json', 'w') as file:
            json.dump(data, file)
        print(f"Пользователь {login} зарегистрирован.")


def login(username, password):
    if username in subject_secrecy_levels:
        if subject_secrecy_levels[username]['password'] == password:
            print(f"Пользователь {username} успешно вошел в аккаунт.")
        else:
            print("Неверный пароль.")
    else:
        print("Пользователь с таким логином не зарегистрирован.")

def save_subject_secrecy_levels(filename, subject_secrecy_levels):
    with open(filename, 'w') as file:
        for subject, levels in subject_secrecy_levels.items():
            file.write(f"[{subject}]\n")
            for key, value in levels.items():
                file.write(f"{key} = {value}\n")


object_secrecy_levels = load_object_secrecy_levels('objects.ini')
subject_secrecy_levels = load_subject_secrecy_levels('subjects.ini')



def load_access_matrix(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        return data.get('matrix', {})


def display_access_matrix(access_matrix):
    subjects = list(access_matrix.keys())
    objects = list(access_matrix[subjects[0]].keys())

    # Вывод заголовка с названиями объектов
    header = "Subject/Object"
    for object_name in objects:
        header += f"\t{object_name}"
    print(header)

    # Вывод матрицы доступа
    for subject in subjects:
        row = f"{subject}"
        for object_name in objects:
            permission = access_matrix[subject].get(object_name, "null")
            row += f"\t{permission}"
        print(row)


access_matrix = load_access_matrix('database.json')


def update_subject_tempSecrecyLevel(subject_name, new_tempSecrecyLevel):
    with open('subjects.ini', 'r') as file:
        lines = file.readlines()

    with open('subjects.ini', 'w') as file:
        section = None
        for line in lines:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1]
            elif section == subject_name:
                parts = line.split('=')
                if len(parts) == 2:
                    key = parts[0].strip()
                    if key == 'secrecyLevel':
                        line = f'{key} = {new_tempSecrecyLevel}'
            file.write(line + '\n')

    subject_secrecy_levels[subject_name]['tempSecrecyLevel'] = new_tempSecrecyLevel
    save_subject_secrecy_levels('subjects.ini', subject_secrecy_levels)


def getting_access(subj, obj, right):
    mand_subj = subject_secrecy_levels[subj]['secrecyLevel']
    cur_mand_subj = subject_secrecy_levels[subj]['tempSecrecyLevel']
    mand_obj = object_secrecy_levels[obj]['secrecylevel']

    # ss
    if right == 'execute' or right == 'append':
        print('ss выполняется')
    elif right == 'read' or right == 'write':
        if mand_subj >= mand_obj:
            print('ss выполняется')
        else:
            print('ss не выполняется')
            return False

    #*
    if right == 'execute':
        access_matrix[subj][obj] += [right]
        print('* выполняется')
        return True

    elif right == 'append':
        if mand_obj > cur_mand_subj:
            access_matrix[subj][obj] += [right]
            print('* выполняется')
            return True
        cur_mand_subj = mand_obj
        if mand_obj > mand_subj:
            update_subject_tempSecrecyLevel(subj, mand_subj)
        else:
            update_subject_tempSecrecyLevel(subj, mand_obj)
        access_matrix[subj][obj].append(right)

        remove_(subj)

        print('* выполняется')
        return True

    elif right == 'read':
        if cur_mand_subj >= mand_obj:
            access_matrix[subj][obj] += [right]
            print('* выполняется')
            return True
        elif mand_subj >= mand_obj:
            cur_mand_subj = mand_obj
            update_subject_tempSecrecyLevel(subj, mand_obj)
            access_matrix[subj][obj].append(right)

            remove_(subj)

            print('* выполняется')
            return True
        else:
            return False
    elif right == 'write':
        if cur_mand_subj == mand_obj:
            access_matrix[subj][obj].append(right)
            print('* выполняется')
            return True
        if mand_subj >= mand_obj:
            update_subject_tempSecrecyLevel(subj, mand_obj)
            cur_mand_subj = mand_obj
            access_matrix[subj][obj].append(right)

            remove_(subj)

            print('* выполняется')
            return True
    else:
        return False


def remove_(subj):
    objs = list(access_matrix[subj].keys())
    for i in range(len(objs)):
        if 'read' in access_matrix[subj][objs[i]] and subject_secrecy_levels[subj]['tempSecrecyLevel'] < object_secrecy_levels[objs[i]]['secrecylevel']:
            access_matrix[subj][objs[i]].remove('read')
        if 'append' in access_matrix[subj][objs[i]] and subject_secrecy_levels[subj]['tempSecrecyLevel'] < object_secrecy_levels[objs[i]]['secrecylevel']:
            access_matrix[subj][objs[i]].remove('append')
        if 'write' in access_matrix[subj][objs[i]] and subject_secrecy_levels[subj]['tempSecrecyLevel'] != object_secrecy_levels[objs[i]]['secrecylevel']:
            access_matrix[subj][objs[i]].remove('write')
    save_access_matrix('database.json', access_matrix)

def command_read(current_user, object_name):
    if getting_access(current_user, object_name, 'read'):
        material = object_secrecy_levels.get(object_name, {}).get('material')
        print(material)
    else:
        print("Недостаточно прав для чтения объекта.")


def command_write(current_user, object_name, new_text):
    if getting_access(current_user, object_name, 'write'):
        config = configparser.ConfigParser()
        config.read('objects.ini')
        config.set(object_name, 'material', new_text)

        with open('objects.ini', 'w') as configfile:
            config.write(configfile)

        print('* Выполняется (write)')
        return True
    elif getting_access(current_user, object_name, 'append'):
            config = configparser.ConfigParser()
            config.read('objects.ini')
            current_text = config.get(object_name, 'material')
            new_material = current_text + new_text
            config.set(object_name, 'material', new_material)

            with open('objects.ini', 'w') as configfile:
                config.write(configfile)

            print('* Выполняется (append)')
            return True
    else:
        print('Не удалось выполнить операцию')
        return False


def command_execute(current_user, object_name):
    if getting_access(current_user, object_name, 'execute'):
        print("Объект выполнен.")
    else:
        print("Недостаточно прав для выполнения объекта.")


def save_access_matrix(filename, access_matrix):
    data = {'matrix': access_matrix}
    with open(filename, 'w') as file:
        json.dump(data, file)


while True:
    print('(например, read(subject1,file1,r) или write(subject2,object1,w), register(login,password))')
    command = input("Введите команду: ")


    if command.startswith("register"):
        username = str(input("Напишите логин субъекта: "))
        password = str(input("Напишите пароль субъекта: "))
        register_user(username, password)
    elif command.startswith("login"):
        username = input("Введите логин пользователя: ")
        password = input("Введите пароль пользователя: ")
        login(username, password)
    elif command.startswith('print'):
        display_access_matrix(access_matrix)
    elif command.startswith("read"):
        current_user = input("Введите логин пользователя: ")
        object_name = input("Введите название объекта: ")
        command_read(current_user, object_name)
        save_access_matrix('database.json', access_matrix)
        save_subject_secrecy_levels('subjects.ini', subject_secrecy_levels)
    elif command.startswith("write"):
        current_user = input("Введите логин пользователя: ")
        object_name = input("Введите название объекта: ")
        text = input("Введите текст: ")
        command_write(current_user, object_name, text)
        save_access_matrix('database.json', access_matrix)
        save_subject_secrecy_levels('subjects.ini', subject_secrecy_levels)
    elif command.startswith("execute"):
        current_user = input("Введите логин пользователя: ")
        object_name = input("Введите название объекта: ")
        command_execute(current_user, object_name)
        save_access_matrix('database.json', access_matrix)
        save_subject_secrecy_levels('subjects.ini', subject_secrecy_levels)
    elif command == "exit":
        break
    else:
        print("Неверная команда.")


