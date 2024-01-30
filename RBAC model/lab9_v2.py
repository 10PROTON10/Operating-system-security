import json


def load_data():
    with open("roles.json") as json_file:
        data = json.load(json_file)
        return data


def save_data(data):
    with open("roles_out.json", "w") as json_file:
        json.dump(data, json_file, indent=2)


def create_role(data):
    role_name = input("Введите название роли: ")
    if role_name in data["roles"]:
        print("Ошибка: такая роль уже создана.")
        return

    role = {
        "subjects": [],
        "objects": []
    }
    parent_roles = input("Введите родительские роли через запятую: ").split(",")
    parent_subjects = set()
    for parent_role in parent_roles:
        if parent_role in data["roles"]:
            parent_subjects.update(data["roles"][parent_role]["subjects"])
        else:
            print(f"Ошибка: родительская роль '{parent_role}'  не существует.")
            return
    print("Общие субъекты из родительских ролей:", parent_subjects)

    subjects = input("Введите субъекты через запятую: ").split(",")
    for subject in subjects:
        if subject not in data["subjects"]:
            print(f"Ошибка: субъект '{subject}' не создан.")
            return
        if subject not in parent_subjects:
            print(f"Ошибка: субъект '{subject}' не является общим субъектом для родительских ролей.")
            return

    role["subjects"] = subjects
    objects = {}
    while True:
        object_name = input("Введите имя объекта или 'exit' для выхода: ")
        if object_name == "exit":
            break
        if object_name not in data["objects"]:
            print(f"Ошибка: объект '{object_name}' не создан.")
            return

        parent_permissions = set()
        for parent_role in parent_roles:
            if parent_role in data["roles"]:
                permissions = data["roles"][parent_role]["objects"].get(object_name, [])
                parent_permissions.update(set(permissions))
        end_permissions = list(parent_permissions)
        if len(end_permissions) < 3:
            available_permissions = list(set(data["objects"][object_name]["permissions"]) - set(end_permissions))
            print("Доступные права:", available_permissions)
            enter_permissions = input("Введите права через запятую: ").split(",")
            for permission in enter_permissions:
                if permission.strip() in available_permissions:
                    end_permissions.append(permission.strip())
                else:
                    print(f"Ошибка: право '{permission.strip()}' не доступно для объекта '{object_name}'.")
                    return
        print("Итоговые права: ", end_permissions)
        objects[object_name] = end_permissions
    role["objects"] = objects
    data["roles"][role_name] = role
    save_data(data)
    print("Выполнено успешно")


def display_role_matrix(data):
    subjects = data["subjects"]
    objects = list(data["objects"].keys())

    role_matrix = []
    for subject in subjects:
        row = []
        for obj in objects:
            available_roles = []
            for role, role_data in data["roles"].items():
                if subject in role_data["subjects"] and obj in role_data["objects"]:
                    available_roles.append(role)
            row.append(available_roles)
        role_matrix.append(row)

    print("Матрица ролей:")
    print("Subjects/Objects", end="\t\t")
    for obj in objects:
        print(obj, end="\t\t")
    print()

    for i, subject in enumerate(subjects):
        print(subject, end="\t\t\t")
        for j, obj in enumerate(objects):
            roles = role_matrix[i][j]
            print(roles, end="\t\t")
        print()


def command_executor(data):
    while True:
        command = input("Введите команду: ")

        if command == "create":
            create_role(data)
        elif command == "help":
            help()
        elif command == "matrix":
            display_role_matrix(data)
        elif command == "exit":
            break
        else:
            print("Ошибка: не правильная комманда.")

    print("Выход из программы.")


def help():
    print("Доступные команды:")
    print("help - список доступных команд")
    print("create - Создать новую роль")
    print("matrix - Отображение матрицы ролей")
    print("exit - Выйти из программы")


def main():
    data = load_data()
    command_executor(data)


if __name__ == "__main__":
    main()
