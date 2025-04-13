# Алгоритм решета для поиска простых чисел и факторизации на промежутке [x<sup>2</sup>; (x+1)<sup>2</sup>), и потенциальное доказательство гипотезы Twin primes conjecture
## Описание проблематики
Обычно для понимания поиска простых чисел и факторизации (разложение на составные числа) используется решето Эратосфена как интуитивно понятное. Остальные методы факторизации целых чисел используют более быстрые подходы, но все они работают на пространстве [2; N), то есть всегда учитываются какие-то произвольные натуральные числа, меньшие N.

## Новое решето факторизации на локальном блоке данных
Предлагается новый подход к факторизации. Суть его простыми словами в следующем:

- Выделяем блок данных между двумя соседними квадратами целых чисел x^2 <= n < (x+1)^2 -это простая операция с квадратным корнем n.
- Число n представляем в виде n = n^2 + k, где 0 <= k <= 2 * x (очевидно)
- Для каждого числа проводим операцию перебора множителей - но только не начиная с 2, а начиная с x. Если фиксируем, что остаток k=0, добавляем в массив значение инкремента (x - c), с меняется с 0 до (x-2). Следовательно, по перечню всех значений в массиве можно восстановить значение одного из множителей.
PROFIT!!!
Пример кода - для понимания как это работает
```python
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
        # begin factorization from base X^2 plus some k: min((k-n^2))
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
```
Если посмотреть результат работы на любом блоке, сразу бросается в глаза закономерность - два цикла, начинающихся с 0, один с самого низа вверх с нарастающим шагом, второй - с середины чуть меньшим шагом, пример на одном блоке межку последовательными квадратами 29^2 и 30^2:
```
Base=[ 841 ,  900 )
841 0, 
842 27, 
843 26, 
844 25, 27, 
845 16, 24, 
846 11, 20, 23, 26, 27, 
847 18, 22, 
848 13, 21, 25, 27, 
849 26, 
850 4, 12, 19, 24, 27, 
851 6, 
852 17, 23, 25, 26, 27, 
853 28
854 15, 22, 27, 
855 10, 14, 20, 24, 26, 
856 21, 25, 27, 
857 28
858 3, 7, 16, 18, 23, 26, 27, 
859 28
860 9, 19, 24, 25, 27, 
861 8, 22, 26, 
862 27, 
863 28
864 2, 5, 11, 13, 17, 20, 21, 23, 25, 26, 27, 
865 24, 
866 27, 
867 12, 26, 
868 1, 15, 22, 25, 27, 
869 18, 
870 0, 14, 19, 23, 24, 26, 27, 
871 16, 
872 21, 25, 27, 
873 20, 26, 
874 6, 10, 27, 
875 4, 22, 24, 
876 17, 23, 25, 26, 27, 
877 28
878 27, 
879 26, 
880 7, 9, 13, 18, 19, 21, 24, 25, 27, 
881 28
882 8, 11, 15, 20, 22, 23, 26, 27, 
883 28
884 3, 12, 16, 25, 27, 
885 14, 24, 26, 
886 27, 
887 28
888 5, 17, 21, 23, 25, 26, 27, 
889 22, 
890 19, 24, 27, 
891 2, 18, 20, 26, 
892 25, 27, 
893 10, 
894 23, 26, 27, 
895 24, 
896 1, 13, 15, 21, 22, 25, 27, 
897 6, 16, 26, 
898 27, 
899 0,
``` 
Disclaimer - обратите внимание на то, что простые числа точно маркируются значением 28, это ровно x-1

На самом деле это такое же решето, как и решето Эратосфена, но только работающее:

по изолированному блоку, то есть сложность реализации снижается до O(sqrt(N)), что неплохо,
работающее сверху вниз (от большего к меньшему), а не снизу вверх как в решете Эратосфена (снизу вверх),
поиск чисел идет от середины (оба составных числа равны x), далее левое число снижается до 2, правое число пропорционально увеличивается большим шагом.
Паттерн этого шаблона очень простой, его можно представить в виде кода:
```python
# let's recreate pattern from only from block size

for k in range(29, 30, 1):
    hops2 = [''] * 1000
    bsize = 2 * k + 1
    pos = 0
    step = k

    hops2[bsize - 1] = '0, '  # Mark last zero (x^2), because this is exception. Other numbers is shifting fast forward

    for i in range(0, k-1):
        p1 = pos # starting position is the lowest (biggest number)
        p2 = pos + step # mark next position on dynamic sieve
        if p2 >= 0 or p2 < bsize: # for first numbers (highest one) we mark one position forward, but always check bounds of block
            hops2[p2] += str(i) + ", "
        for j in range(p1, -1, -step): # That's the main sieve - the mark lowest number, and going down with fixed steps until we hit the border of block
            if j >= 0 or j < bsize:
                hops2[j] += str(i) + ", "

        # This is dynamic calculating of next step
        step -= 1 # decrement step of sieve by 1, and this is same as Sieve of Eratosphenes (SoE)
        pos = pos + 3 + i * 2 # This is idiocrazy of local sieve, because it is starting from different point than SoE

    print (inRed("Sieve of Oleg"))
    for i in range(0, bsize):
        s = hops2[bsize-i-1]
        if s == '':
            print (f"{inRed(k*k+i)}: {k-1}")
        else:
            print (f"{k*k+i}: {s}")
```
Можно убедиться на любом блоке и даже доказать, что алгоритм разложения сверху и снизу идентичны по результатам, и в результате мы можем выявить в выбранном блоке сразу все составные и простые числа.

Очень важно, что алгоритм на вход получает только размер блока, и по нему полностью восстанавливает раскладку простых и составных чисел, при этом совершенно не важно значение каждого числа в блоке. Получается, что факторизация носит локальный, а не глобальный характер по пространству натуральных чисел!

Вывод массива со значением чисел сделан для красоты, выше в алгоритма решета сами числа в блоке не участвуют в расчетах

# Выводы
Помимо оптимизации алгоритма решета, напрашиваются интересные выводы:

можно разложить любое число по алгоритму, которому не важно значение этого числа, а только блок последовательных кввдратов натуральных чисел, в котором находится это число и его положение в нем (более ничего!)
оказывается, что простые и составные числа не зависят ни от каких других чисел вне блока последовательных квадратов чисел - решето Эратосфена является последовательным по сути, простота чисел и их разложение зависит от чисел ниже его. Из этого следует пересмотр глобальности влияния простых и составных чисел друг на друга.
оказывается, что сложность алгоритмов факторизации, поиска простых чисел и доказательства простоты числа можно понизить на квадратный корень.
# Гипотеза
Предположим, что алгоритм факторизации верен и действует для блока между последовательными квадратами натуральных чисел. Мы видим, что переходе от блока 2 .. n к блоку x^2<= n <(x+1)^2 принцип решета остается, но меняются правила и шаг решета, Следовательно, стоит ожидать, что если мы возьмем квадрат от числа x, то есть уменьшим блок еще на квадратный корень, мы перейдем к еще одному, более сложному варианту решета, которое действует на более локальном диапазоне,

- если эта гипотеза верна, то рекурсивно можно снизить диапазон вплоть до нескольких чисел, что приведет к сложности поиска и факторизации одного числа до O(log (N))
- Теорема простых чисел-близнецов - если исследовать алгоритм локальной факторизации и доказать, что существует бесконечное количество размеров блоков, при которых такие близнецы возникают, то автоматически отсюда доказывается, что количество простых чисел-близнецов бесконечно, так как количество блоков также бесконечно.

# Как алгоритм с поиском между соседними квадратами натуральных с комплексностью _O(sqrt N)_ чисел может быть превращен в алгоритм c комплексностью _O(log N)_
Как ранее отмечалось, каждое натуральное число n (n>1) можно представить в виде:
_n = x^2^ + k_, где x, k - натуральные числа и n < (x+1)^2^
Легко заметить, что алгоритм факторизации и поиска простых чисел имеет комплексность _O(sqrt N)_.Каждый блок чисел размером x можно разложить отдельно, так как он начинается с 0 (делится на х) и имеет детерминированный шаг решетки.
Доказательство, что разложение является единственным и других вариантов нет, достаточно просто, так как в алгоритме перебираются все факторы от от x до 2, и, если n фактуризуется с фактором больше x, то второй фактор будет меньше x и точно будет отвловлен при переборе алгоритма.
Однако легко заметить, что, применяя алгоритм, мы просто вводим новый тип составных чисел, при этом не меняя понятие простого числа - наши составные числа образуются не простой решеткой Эратосфена, а немного более сложной решеткой, зависимой от блока.
Следовательно, существует аналогичный алгоритму выше новый алгоритм, который берет новый блок чисел и раскладывает их на другой тип составных чисел, в этом случае число n представляется более сложным образом:
_n = x^2^ + (y^2^ + z)_, где x,  y, z - натуральные числа и n< (x+1)^2^, а y < (x+1)^2^ - x^2^
Если продолжить далее рекурсивно, то постепенно мы придем к числу 2 и диапазону блока 2.
