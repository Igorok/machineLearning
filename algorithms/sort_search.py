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

'''
alist = [54,26,93,17,77,31,44,55,20]
insertionSort(alist)
print(alist)
'''

'''
Сортировка Шелла
Она улучшает сортировку вставками, разбивая первоначальный список на несколько подсписков, каждый из которых сортируется по отдельности. Вместо того, чтобы выделять подсписки из стоящих рядом элементов, сортировка Шелла использует инкремент i (приращение), чтобы создавать подсписки из значений, отстоящих на расстоянии i друг от друга.
'''
def shellSort(alist):
    sublistcount = len(alist) // 2
    while sublistcount > 0:
        for startposition in range(sublistcount):
            gapInsertionSort(alist, startposition, sublistcount)
        print("After increments of size", sublistcount, "The list is", alist)
        sublistcount = sublistcount // 2

# сортировка вставкой, дополнительно принимает начало и шаг
# смещают не соседние элементы а разделенные шагом, который каждый раз уменьшается
# в последнем вызове шагом окажется 1 а началом 0 и произойдет стандартная сортировка вставками
def gapInsertionSort(alist, start, gap):
    # список от начала + шаг, до последнего элемента, с интервалом в шагом
    for i in range(start + gap, len(alist), gap):
        currentvalue = alist[i]
        position = i
        
        # пока позиция больше либо равна шагу и значение отстающее на шаг больше текущего
        # элементы списка смещаются вперед и позиция уменьшается на шаг,
        # как только это прекращается, 
        # последнему элементу попавшему под смещение присваивается текущее значение
        while position >= gap and alist[position - gap] > currentvalue:
            alist[position] = alist[position - gap]
            position = position - gap

        alist[position] = currentvalue

'''
alist = [54,26,93,17,77,31,44,55,20]
shellSort(alist)
print(alist)
'''

'''
Сортировка слиянием
Это рекурсивный алгоритм, который постоянно разбивает список пополам. Если список пуст или состоит из одного элемента, то он отсортирован по определению (базовый случай). Если в списке больше, чем один элемент, мы разбиваем его и рекурсивно вызываем сортировку слиянием для каждой из половин. После того, как обе они уже отсортированы, выполняется основная операция, называемая слиянием. Слияние - это процесс комбинирования двух меньших сортированных списков в один новый, но тоже отсортированный.
'''

def mergeSort(alist):
    print("Splitting ", alist)

    # если длина массива больше 1
    if len(alist) > 1:
        # делим на 2 части
        mid = len(alist) // 2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        # рекурсивно запускаем для частей
        # пока не останутся массивы с единственным числом
        mergeSort(lefthalf)
        mergeSort(righthalf)

        i = 0
        j = 0
        k = 0

        # проходим по обоим частям, сравниваем их элементы
        # если элемент слева меньше то он помещается в начало списка, переходим к следующему
        # если меньше справа, помещаем в список переходим к следующему
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                alist[k] = lefthalf[i]
                i = i + 1
            else:
                alist[k] = righthalf[j]
                j = j + 1
            k = k + 1

        # в оставшихся частях остаются большие значения
        # т.к. они уже были отсортированы ранее
        # большие числа устанавливаются в конец массива
        while i < len(lefthalf):
            alist[k] = lefthalf[i]
            i = i + 1
            k = k + 1

        while j < len(righthalf):
            alist[k] = righthalf[j]
            j = j + 1
            k = k + 1

    print("Merging ", alist)

'''
alist = [54,26,93,17,77,31,44,55,20]
mergeSort(alist)
print(alist)
'''


'''
Быстрая сортировка
Сначала быстрая сортировка выбирает значение, которое называется опорным элементом, будем просто использовать первое значение в списке. Роль опорного элемента заключается в помощи при разбиении списка. Позиция, на которой он окажется в итоговом сортированном списке, обычно называемая точкой разбиения, будет использоваться для разделения списка при последующих вызовах быстрой сортировки.
'''

def quickSort(alist):
    quickSortHelper(alist, 0, len(alist) - 1)
 
def quickSortHelper(alist, first, last):
    if first < last:
        splitpoint = partition(alist, first, last)

        # рекурсивно проходит до начала массива
        quickSortHelper(alist, first, splitpoint - 1)
        # остается рекурсивно пройти от точки разделения до конца
        quickSortHelper(alist, splitpoint + 1, last)


def partition(alist, first, last):
    print('alist, first, last', alist, first, last)

    # определяем значение с которым будем сравнивать
    pivotvalue = alist[first]

    # левый индекс на 1 больше дефолтного, правый последний
    leftmark = first + 1
    rightmark = last

    done = False
    while not done:
        print('alist', alist)
        # пока левый индекс не пересечется с правым
        # и пока левое значение не окажется меньше дефолтного
        # увеличиваем левый индекс
        while (
            leftmark <= rightmark and
            alist[leftmark] <= pivotvalue
        ):
            leftmark = leftmark + 1

        # пока правый индекс не пересечется с левым
        # и пока правое значение больше дефолтного
        # уменьшаем правый индекс
        while (
            alist[rightmark] >= pivotvalue and
            rightmark >= leftmark
        ):
            rightmark = rightmark -1

        print(
            'left, right', leftmark, rightmark,
            'values', alist[leftmark], alist[rightmark]
        )
        # когда правый индекс меньше левого,
        # большие и меньшие элементы раскиданы по разные стороны от дефолтного
        # можно выходить
        if rightmark < leftmark:
            done = True
        # пока условие не выполнено, меняем правый элемент с левым
        else:
            alist[leftmark], alist[rightmark] =  alist[rightmark], alist[leftmark]

    # берем последнее значение справа, которое меньше дефолтного
    # и меняем с дефолтным
    # следующие рекурсии пройдут левую сторону до начала, 
    # потом начнут рекурсивно сортировать правую часть
    alist[first], alist[rightmark] = alist[rightmark], alist[first]
    return rightmark

'''
alist = [54,26,93,17,77,31,44,55,20]
quickSort(alist)
print(alist)
'''