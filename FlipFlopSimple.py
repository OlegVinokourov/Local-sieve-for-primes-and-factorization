
def primeTest(num):
# Negative numbers, 0 and 1 are not primes
    if num < 1:
        return False
    # Iterate from 2 to n // 2
    for i in range(2, (num // 2) + 1):
            # If num is divisible by any number between
            # 2 and n / 2, it is not prime
            if (num % i) == 0:
                return False
    return True

def inRed(prt):
    return f"\033[91m{prt}\033[00m"

def inGreen(prt):
    return f"\033[92m{prt}\033[00m"

def checkBounds(size, x):
    if x < 0 or x >= size:
        return False
    return True

import math

hops = [1000]

for n in range(29, 30, 1):
    # Calculating base square number n^2
    base_sqr = n * n
    # Calculating next square number (n+1)^2
    sqr_next = (n+1) * (n+1)
    print(inGreen("Base=["), base_sqr, ", ", sqr_next, ")")
    for k in range(base_sqr, sqr_next):
        # начинаем разложение с базового квадрата min((k-n^2))
        x = n
        z = k % x
        h = 0
        lineage = f"({x}*{k//x}{z:+}) "
        hops = ""

        isPrimeNotFinded = True

        while(x > 1):
            if z == 0:
                hops += f"{h}, "
                isPrimeNotFinded = False
            x -= 1
            z = k % x
            lineage += f"({x}*{k//x}{z:+}) "
            h += 1

        if isPrimeNotFinded:
            if not primeTest(k):
                raise Exception("Error - is not prime!")
            hops = str(h)
            # print(inRed(k), hops, "-> ", lineage) # verbose
            print(inRed(k), hops) # only pattern
        else:
            if primeTest(k):
                raise Exception("Error - is prime!")
            # print(k, hops, "-> ", lineage) # verbose
            print(k, hops) # only pattern

# let's recreate pattern from only from block size

for k in range(29, 30, 1):
    hops2 = [''] * 1000
    bsize = 2 * k + 1
    pos = 0
    step = k

    hops2[bsize - 1] = '0, '  # Последняя веха в самом верху, дальше ее не отмечаем, так как на 2x и более вперед больше не убежит никогда, только назад

    for i in range(0, k-1):
        p1 = pos # Отмечаем основную веху (в самом низу)
        p2 = pos + step # Отмечааем веху выше посередине
        if p2 >= 0 or p2 < bsize: # этот маркер работает с самого начала, пока не выходит за окно блока, потом уже не возвращается
            hops2[p2] += str(i) + ", "
        for j in range(p1, -1, -step): # А здесь ставим первую веху и уходим назад (в более высокие числа), пока не достигаем нижней границы блока
            if j >= 0 or j < bsize:
                hops2[j] += str(i) + ", "

        # После того, как проставили все маркеры на текущем цикле, обновляем шаг и позицию
        step -= 1
        pos = pos + 3 + i * 2

    print (inRed("Sieve of Oleg"))
    for i in range(0, bsize):
        s = hops2[bsize-i-1]
        if s == '':
            print (f"{inRed(k*k+i)}: {k-1}")
        else:
            print (f"{k*k+i}: {s}")