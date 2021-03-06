'''
Числа Фибоначчи — элементы числовой последовательности в которой первые два числа равны либо 1 и 1, либо 0 и 1, а каждое последующее число равно сумме двух предыдущих чисел. Названы в честь средневекового математика Леонардо Пизанского (известного как Фибоначчи)
'''

# циклично
def fib1(num):
    n1 = 1
    n2 = 1
    arr = [n1, n2]
    while num - 2 > 0:
        n1, n2 = n2, n2 + n1
        arr.append(n2)
        num = num - 1

    return (arr, n2)

print(1, fib1(10))

# рекурсивно
def fib2(num):
    if num == 1 or num == 2:
        return 1
    return fib2(num - 2) + fib2(num - 1)

print(2, fib2(10))
