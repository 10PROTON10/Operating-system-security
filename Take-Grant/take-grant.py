import csv
from subject import Subject
from document import Document


def unpacking_graph(file):
    global documents, subjects, access_graph
    with open(file, "r") as file_reader:
        line = file_reader.readline().strip().split(";")
        documents = {doc: Document(doc) for doc in line}

        line = file_reader.readline().strip().split(";")
        subjects = {sub: Subject(sub) for sub in line}

        access_graph = []
        entity = None
        ver = None


        for line in file_reader:
            line = line.strip().split(";")
            access_graph.append(documents[line[0]] if line[0] in documents else subjects[line[0]])

            for i in range(1, len(line)):
                ver = line[i].split(":")
                entity = documents[ver[0]] if ver[0] in documents else subjects[ver[0]]
                access_graph[-1].add_to_links(entity, ver[1])


def graph_backup():
    with open("Graph1.csv", mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(list(documents.keys()))
        writer.writerow(list(subjects.keys()))
        for entity in access_graph:
            if entity:
                line = [entity.get_id()]
                for link, value in entity.get_links().items():
                    line.append(f"{link.get_id()}:{value}")
                writer.writerow(line)


def command_create(rule, from_entity, to_entity, type, current_user):
    if current_user == 'admin':
        if rule in rules:
            if to_entity not in documents and to_entity not in subjects:
                if from_entity in documents:
                    if type == "s":
                        subject = Subject(to_entity)
                        subjects[to_entity] = subject
                        documents[from_entity].add_to_links(subject, rule)
                        print("создание такого субъекта завершено\n")
                    elif type == "d":
                        document = Document(to_entity)
                        documents[to_entity] = document
                        documents[from_entity].add_to_links(Document(to_entity), rule)
                        print("создание такого документа завершено\n")
                    else:
                        print("неправильный тип сущности\n")
                elif from_entity in subjects:
                    if type == "s":
                        subject = Subject(to_entity)
                        subjects[to_entity] = subject
                        subjects[from_entity].add_to_links(subject, rule)
                        print("создание такого субъекта завершено\n")
                    elif type == "d":
                        document = Document(to_entity)
                        documents[to_entity] = document
                        subjects[from_entity].add_to_links(Document(to_entity), rule)
                        print("создание такого документа завершено\n")
                    else:
                        print("неправильный тип сущности\n")
                else:
                    print("такая сущность не существует\n")
            else:
                print("такая сущность существует\n")
        else:
            print("такого правила не существует\n")
    else:
        print("данная команда доступна только admin\n")
    graph_backup()


def command_take(rule, from_entity, to_entity, on_entity):
    if rule in rules:
        if from_entity in documents or from_entity in subjects:
            if to_entity in documents or to_entity in subjects:
                if on_entity in documents or on_entity in subjects:
                    if find_path(from_entity, on_entity, to_entity, "t", rule):
                        print("да, эта сущность может это сделать\n")
                    else:
                        print("нет, эта сущность не может этого сделать\n")
                else:
                    print("четвёртый аргумент неверен\n")
            else:
                print("третий аргумент неверен\n")
        else:
            print("второй аргумент неверен\n")
    else:
        print("первый аргумент неверен\n")
    graph_backup()


def command_grant(rule, from_entity, to_entity, on_entity):
    if rule in rules:
        if from_entity in documents or from_entity in subjects:
            if from_entity in documents:
                from_whom = documents.get(from_entity)
            else:
                from_whom = subjects.get(from_entity)
            if to_entity in documents or to_entity in subjects:
                if to_entity in documents:
                    to_whom = documents.get(to_entity)
                else:
                    to_whom = subjects.get(to_entity)
                if on_entity in documents or on_entity in subjects:
                    if on_entity in documents:
                        on_what = documents.get(on_entity)
                    else:
                        on_what = subjects.get(on_entity)
                    if (from_whom.get_link(to_whom) == "g" or from_whom.get_link(to_whom) == "a") and find_ver(from_whom, on_what, rule):
                        print("да, эта сущность может это сделать\n")
                    else:
                        print("нет, эта сущность не может этого сделать\n")
                else:
                    print("четвёртый аргумент неверен\n")
            else:
                print("третий аргумент неверен\n")
        else:
            print("второй аргумент неверен\n")
    else:
        print("первый аргумент неверен\n")
    graph_backup()


def command_delete(from_entity, to_entity):
    if from_entity in documents:
        if to_entity in documents:
            d = documents[to_entity]
            if documents[from_entity].get_link(d) == "a":
                remove_entity(from_entity, to_entity)
                print("Удаление такого субъекта завершено\n")
            else:
                print("Нет привилегий для этого действия\n")
        elif to_entity in subjects:
            s = subjects[to_entity]
            if documents[from_entity].get_link(s) == "a":
                remove_entity(from_entity, to_entity)
                print("Удаление такого субъекта завершено\n")
            else:
                print("Нет привилегий для этого действия\n")
        else:
            print("У вас нет такой сущности для удаления\n")
    elif from_entity in subjects:
        if to_entity in documents:
            d = documents[to_entity]
            if subjects[from_entity].get_link(d) == "a":
                remove_entity(from_entity, to_entity)
                print("Удаление такого документа завершено\n")
            else:
                print("Нет привилегий для этого действия\n")
        elif to_entity in subjects:
            s = subjects[to_entity]
            if subjects[from_entity].get_link(s) == "a":
                remove_entity(from_entity, to_entity)
                print("Удаление такого субъекта завершено\n")
            else:
                print("Нет привилегий для этого действия\n")
        else:
            print("У вас нет такой сущности для удаления\n")
    else:
        print("Нет такой сущности\n")


def remove_entity(client, file_name):
    lines = []
    contents = ''

    with open("Graph1.csv", mode='r') as f:
        reader = csv.reader(f, delimiter=';')
        lines = list(reader)

    for i in range(2, len(lines)):
        row = lines[i]
        if len(row) > 1 and row[0] == client:
            for j in range(1, len(row)):
                if row[j].startswith(file_name) and ':a' in row[j]:
                    row[j] = ''

    for line in lines:
        contents += ';'.join(line) + '\n'

    # Проверка наличия ';;' и замена на ';'
    if ';;' in contents:
        contents = contents.replace(';;', ';')

    with open("Graph1.csv", mode='w', newline='') as f:
        f.write(contents)


def find_path(first, last, penultimate, f_rule, s_rule):
    run_usl = True
    if first in documents:
        first_ver = documents[first]
    else:
        first_ver = subjects[first]
    if penultimate in documents:
        penultimate_ver = documents[penultimate]
    else:
        penultimate_ver = subjects[penultimate]
    if last in documents:
        last_ver = documents[last]
    else:
        last_ver = subjects[last]
    if penultimate_ver.get_link(last_ver) == s_rule:
        if len(first_ver.links) == 0:
            return False
        else:
            ver = first_ver
            while len(ver.links) == 1:
                if list(ver.links.values())[0] == f_rule:
                    if list(ver.links.keys())[0] == penultimate_ver:
                        return True
                    else:
                        ver = list(ver.links.keys())[0]
                else:
                    return False
            return find_ver(ver, penultimate_ver, f_rule)
    else:
        return False


def find_ver(n_ver, e_ver, rule):
    for ver in n_ver.links.keys():
        if ver.id == e_ver.id:
            if n_ver.get_link(ver) == rule or n_ver.get_link(ver) == "a":
                return True
            else:
                return False
        else:
            if len(ver.links) != 0:
                if find_ver(ver, e_ver, rule):
                    return True
    return False


def user_registration():
    with open("subjects.ini", "w") as file:
        while True:
            print("Пожалуйста введите ваш логин (или 'exit' для выхода):")
            login = input()
            if login == "exit":
                break
            print("Пожалуйста введите ваш пароль:")
            password = input()
            file.write(f"[{login}]\n")
            file.write(f"login = {login}\n")
            file.write(f"password = {password}\n")
            print("Регистрация завершена!")


def user_login():
    print("Пожалуйста введите ваш логин:")
    login = input()
    print("Пожалуйста введите ваш пароль:")
    password = input()
    with open("subjects.ini", "r") as file:
        data = file.readlines()

    for i in range(len(data)):
        line = data[i].strip()
        if line.startswith("[") and line.endswith("]"):
            user_login = line[1:-1]
            if user_login == login and f"password = {password}" in data[i + 2].strip():
                print("Вход в систему успешен!")
                return login

    print("Неправильный логин или пароль.")
    return None


def logout(current_user):
    if current_user is None:
        print("В данный момент ни один пользователь не вошел в систему.")
    else:
        print("Успешно вышел из системы.")
    return None


def get_entity_links(entity):
    if entity in documents:
        print(f"Entity: {entity} (Document)")
    elif entity in subjects:
        print(f"Entity: {entity} (Subject)")
    else:
        print("Сущность не найдена.")

    if entity in documents:
        entity_obj = documents[entity]
    elif entity in subjects:
        entity_obj = subjects[entity]
    else:
        return

    links = entity_obj.get_links()
    print("Links:")
    for linked_entity, access in links.items():
        print(f"  {linked_entity.get_id()} (Access: {access})")


def help():
    commands = [
        ("help", "Показать список доступных команд."),
        ("register", "Зарегистрировать нового пользователя."),
        ("login", "Войти в систему."),
        ("logout", "Выйти из системы."),
        ("links", "Получить список связей для заданной сущности."),
        ("create", "Создать связь между сущностями."),
        ("take", "Проверить возможность выполнения действия."),
        ("grant", "Проверить возможность выполнения привилегированного действия."),
        ("delete", "Удалить связь между сущностями.")
    ]

    print("Список доступных команд:")
    for command, description in commands:
        print(f"{command}: {description}")


def command_executor(current_user, command):
    if command == "help":
        help()
    elif command == "register":
        user_registration()
    elif command == "login":
        current_user = user_login()
    elif command == "logout":
        current_user = logout(current_user)
    elif command == "links":
        if current_user is None:
            print("Пожалуйста, сначала войдите в систему.")
        else:
            entity = input("Введите название сущности: ")
            get_entity_links(entity)
    elif command == "create":
        if current_user is None:
            print("Пожалуйста, сначала войдите в систему.")
        else:
            rule = input("Введите роль: ")
            from_entity = input("Введите название сущности, от которой будет установлена связь: ")
            to_entity = input("Введите название сущности, до которой будет установлена связь: ")
            type = input("Введите тип: ")
            command_create(rule, from_entity, to_entity, type, current_user)
    elif command == "take":
        if current_user is None:
            print("Пожалуйста, сначала войдите в систему.")
        else:
            rule = input("Введите роль: ")
            from_entity = input("Введите название сущности, от которой будет установлена связь: ")
            to_entity = input("Введите название сущности, до которой будет установлена связь: ")
            on_entity = input("Введите промежуточную сущность: ")
            command_take(rule, from_entity, to_entity, on_entity)
    elif command == "grant":
        if current_user is None:
            print("Пожалуйста, сначала войдите в систему.")
        else:
            rule = input("Введите роль: ")
            from_entity = input("Введите название сущности, от которой будет установлена связь: ")
            to_entity = input("Введите название сущности, до которой будет установлена связь: ")
            on_entity = input("Введите промежуточную сущность: ")
            command_grant(rule, from_entity, to_entity, on_entity)
    elif command == "delete":
        if current_user is None:
            print("Пожалуйста, сначала войдите в систему.")
        else:
            from_entity = input("Введите название сущности, от которой будет установлена связь: ")
            to_entity = input("Введите название сущности, до которой будет установлена связь: ")
            command_delete(from_entity, to_entity)
    else:
        print("Команда не найдена. Введите help для получения списка доступных команд.")

    return current_user


def main():
    unpacking_graph("Graph.csv")
    current_user = None

    print("Введите help для получения списка доступных команд.")

    while True:
        command = input(">> ")
        if command == "exit":
            break
        else:
            current_user = command_executor(current_user, command)


if __name__ == "__main__":
    rules = ["t", "g", "a"]
    documents = {}
    subjects = {}
    access_graph = []
    run_usl = True
    main()

