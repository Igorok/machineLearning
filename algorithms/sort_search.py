# -*- coding: utf-8 -*-

'''
Когда элементы данных хранятся коллекцией в виде списка, мы говорим, что между ними линейные или последовательные отношения. Каждый элемент хранится на определённой позиции относительно прочих. В списках Python она задаётся индексом данного элемента. Поскольку значения индексов упорядочены, мы имеем возможность последовательно проходить по ним. Этот процесс приводит к нашей первой поисковой технике - последовательному поиску.
'''
def sequentialSearch(alist, item):
    pos = 0
    found = False

    while pos < len(alist) and not found:
        if alist[pos] == item:
            found = True
        else:
            pos = pos + 1
    
    return found

'''
testlist = [1, 2, 32, 8, 17, 19, 42, 13, 0]
print(sequentialSearch(testlist, 3))
print(sequentialSearch(testlist, 13))
'''

'''
Бинарный поиск - поиск в отсортированном списке, начинает проверять элементы с находящегося в середине.
'''
def binarySearch(alist, item):
    first = 0
    last = len(alist) - 1
    found = False

    while first <= last and not found:
        midpoint = (first + last) // 2
        if alist[midpoint] == item:
            found = True
        elif item < alist[midpoint]:
            last = midpoint - 1
        else:
            first = midpoint + 1

    return found

'''
testlist = [0, 1, 2, 8, 13, 17, 19, 32, 42,]
print(binarySearch(testlist, 3))
print(binarySearch(testlist, 13))
'''


'''
Пузырьковая сортировка делает по списку несколько проходов. Она сравнивает стоящие рядом элементы и меняет местами те из них, что находятся в неправильном порядке. Каждый проход по списку помещает следующее наибольшее значение на его правильную позицию. В сущности, каждый элемент “пузырьком” всплывает на своё место.
'''

def bubbleSort(alist):
    # если не было перестановок, значит список отсортирован и больше обходы не нужны
    replaced = True
    num = len(alist) - 1
    
    while num > 0 and replaced:
        replaced = False
        for i in range(num):
            if alist[i] > alist[i + 1]:
                replaced = True
                alist[i], alist[i + 1] =  alist[i + 1], alist[i]
        # т.к. больший элемент всплывет в конце, число проходов каждый раз можно уменьшать на 1
        num = num - 1

'''
alist=[54,26,93,17,77,31,44,55,20]
bubbleSort(alist)
print(alist)
'''

'''
Сортировка выбором улучшает пузырьковую сортировку, совершая всего один обмен за каждый проход по списку. Чтобы сделать это, она ищет наибольший элемент и помещает его на соответствующую позицию. Как и для пузырьковой сортировки, после первого прохода самый большой элемент находится на правильном месте. После второго - на своё место становится следующий наибольший элемент.
'''
def selectionSort(alist):
    # список от последнего до 1, с шагом -1
    for fillslot in range(len(alist) - 1, 0, -1):
        # позиция максимального элемента
        positionOfMax = 0
        # список от 1 до последнего
        for location in range(1, fillslot + 1):
            # ищем ключ большего значения
            if alist[location] > alist[positionOfMax]:
                positionOfMax = location
        # ставим большее значение в конец списка
        alist[fillslot], alist[positionOfMax] =  alist[positionOfMax], alist[fillslot]

'''
alist = [54,26,93,17,77,31,44,55,20]
selectionSort(alist)
print(alist)
'''

'''
Сортировка вставками, имея по-прежнему, работает несколько иначе. Она всегда поддерживает в сортированном виде подсписок на нижних индексах списка. Каждый новый элемент вставляется в упорядоченный на прошлой итерации подсписок так, чтобы тот остался сортированным и стал на один элемент больше.
'''

# начиная с первых двух элементов поддерживаем отсортированный массив
# если элементы массива больше попавшегося элемента то они поднимаются на его место 
# процесс продолжается пока большие элементы не прекратятся
# на эту позицию и устанавливается попавшееся значение
def insertionSort(alist):
    # список от 1 до последнего элемента
    for index in range(1, len(alist)):
        # значение первого элемента
        currentvalue = alist[index]
        position = index

        # если предыдущее значения больше текущего 
        # проходим до начала списка и смещаем значения из начала в конец
        while position > 0 and alist[position - 1] > currentvalue:
            alist[position] = alist[position - 1]
            position = position - 1
        # той позиции, на которой этот процесс останавливается устанавливаем текущее значение
        alist[position]=currentvalue

alist = [54,26,93,17,77,31,44,55,20]
insertionSort(alist)
print(alist)