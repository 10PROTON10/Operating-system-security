from psutil import disk_io_counters
from random import randint
from random import randrange


def is_prime(n, k=10):
    # 1 и 2 - простые числа
    if n in [1, 2]:
        return True

    # Проверяем, является ли n четным числом
    if n % 2 == 0:
        return False

    # Функция для разложения n-1 на степени двойки и нечетный множитель
    def decompose(n):
        s = 0
        while n % 2 == 0:
            s += 1
            n //= 2
        return s, n

    # Вычисляем s и d для n-1
    s, d = decompose(n - 1)

    # Проверяем свойство Ферма k раз
    for _ in range(k):
        a = randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

massiv = []
simple_numbers = []
def main():
    while len(simple_numbers) < 2:
        chislo = randrange(2**127, 2**128 - 1)
        if is_prime(chislo) == True:
            chislo = chislo * 4 + 3
            simple_numbers.append(chislo)
    p, q = simple_numbers[0], simple_numbers[1]
    # print('p = ', p)
    # print('q = ', q)
    M = p * q
    # Возвращает количество записанных байт из общей системной статистики дискового ввода-вывода.
    seed = disk_io_counters()[3]
    for i in range(0, 256):
        seed = pow(seed, 2) % M
        bit = bin(seed % 2)
        massiv.append(bit[2:])
    otvet = [''.join(massiv)]
    otvet_string = ''.join(otvet)
    otvets = bytearray(otvet_string.encode())
    return otvets


