from psutil import disk_io_counters
from random import randint, randrange
from sympy import isprime

def is_prime(n, k=100):
    if n == 2:
        return True
    if n == 1 or n % 2 == 0:
        return False

    # Проверяем свойство Миллера-Рабина k раз
    for _ in range(k):
        a = randint(2, n - 2)
        if not isprime(a):
            continue

        d, s = n - 1, 0
        while d % 2 == 0:
            d //= 2
            s += 1

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

def numbers_simple():
    simple_numbers = []
    while len(simple_numbers) < 2:
        chislo = randrange(2 ** 1023, 2 ** 1024 - 1)
        if is_prime(chislo) == True:
            chislo = chislo * 4 + 3
            simple_numbers.append(chislo)
    return simple_numbers


def generate_e():
    M = numbers_simple()[0] * numbers_simple()[1]
    seed = disk_io_counters()[1]
    for i in range(0, 1):
        seed = pow(seed, 2) % M
        bit = bin(seed % 2)
    return bit[2:]


generate_e()

