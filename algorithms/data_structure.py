# -*- coding: utf-8 -*-

'''
O(n) — линейная сложность
Такой сложностью обладает, например, алгоритм поиска наибольшего элемента в не отсортированном массиве. Нам придётся пройтись по всем n элементам массива, чтобы понять, какой из них максимальный.

O(log n) — логарифмическая сложность
Простейший пример — бинарный поиск. Если массив отсортирован, мы можем проверить, есть ли в нём какое-то конкретное значение, методом деления пополам. Проверим средний элемент, если он больше искомого, то отбросим вторую половину массива — там его точно нет. Если же меньше, то наоборот — отбросим начальную половину. И так будем продолжать делить пополам, в итоге проверим log n элементов.

O(n2) — квадратичная сложность
Такую сложность имеет, например, алгоритм сортировки вставками. В канонической реализации он представляет из себя два вложенных цикла: один, чтобы проходить по всему массиву, а второй, чтобы находить место очередному элементу в уже отсортированной части. Таким образом, количество операций будет зависеть от размера массива как n * n, т. е. n2.


Структуры данных

Линейные структуры данных (или списки) – это упорядоченные структуры, в которых адрес данного однозначно определяется его номером (индексом). Примером может быть список учебной группы.

Табличные структуры данных – это упорядоченные структуры, в которых адрес данных однозначно определяется двумя числами – номером строки и номером столбца, на пересечении которых находится ячейка с искомым элементом. Структуры данных могут быть и трехмерными, тогда три числа характеризуют положение элемента и требуются три типа разделителей.

Иерархические структуры данных – это такие структуры, в которых адрес каждого элемента определяется путем (маршрутом доступа), идущим от вершины структуры к данному элементу. Нерегулярные данные, которые трудно представляются в виде списка или таблицы, могут быть представлены в иерархической структуре. Например, иерархическую структуру образуют почтовые адреса.

Единожды добавленный, элемент остаётся на одном и том же месте по отношению к остальным, пришедшим раньше и позже него. Коллекции такого рода часто называют линейными структурами данных. О линейных структурах можно думать, как об имеющих два конца. Иногда эти концы называют левым и правым, иногда - головой и хвостом.

Стек (иногда говорят "магазин" - по аналогии с магазином огнестрельного оружия) - это упорядоченная коллекция элементов, где добавление нового или удаление существующего всегда происходит только на одном из концов. Стопка книг, подносы в столовой, перемещение по вкладкам браузера кнопкой назад.
'''

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)


'''
Проверка открывающихся и закрывающихся скобок
Открывающиеся скобки добавляются в стек, а закрывающаяся сравнивается с последней открывшейся, при этом она удаляется из стека, не соответсвие открывшейся и закрывшейся скобки означает нарушение форматирования
'''
def parChecker(symbolString):
    s = Stack()
    balanced = True
    index = 0
    opens = "([{"
    closers = ")]}"

    def matches(open, close):
        return opens.index(open) == closers.index(close)

    while index < len(symbolString) and balanced:
        symbol = symbolString[index]
        # if this is opened bracket, add symbol to stack
        if symbol in opens:
            s.push(symbol)
        # if this is closed bracket
        elif symbol in closers:
            # if stack is empty- balance is broken
            if s.isEmpty():
                balanced = False
            else:
                # get last opened bracket
                top = s.pop()
                # if closed bracket is not fit to last opened bracket - balance is broken
                if opens.index(top) != closers.index(symbol):
                    balanced = False
        index = index + 1

    if balanced and s.isEmpty():
        return True
    else:
        return False

# print(parChecker('func({{([][])}()})'))
# print(parChecker('func([{()])'))

'''
Конвертирование десятичных чисел в двоичные
При это десятичное число разделяется на 2, затем остаток от деления добавляется в стек, а результат продолжает делиться. По завершению деления необходимо получить символы из стека, остатки от деления в обратном порядке составляют двоичное значение десятичного числа
'''

def divideBy2(decNumber):
    remstack = Stack()

    while decNumber > 0:
        rem = decNumber % 2
        remstack.push(rem)
        decNumber = decNumber // 2

    binString = ""
    while not remstack.isEmpty():
        binString = binString + str(remstack.pop())

    return binString

# print(divideBy2(42))

'''
Очередь - это упорядоченная коллекция элементов, в которой добавление новых происходит с одного конца, называемого “хвост очереди”, а удаление существующих - с другого, “головы очереди”. 
'''
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

'''
Задача Иосифа Флавия или считалка Джозефуса — математическая задача с историческим подтекстом.
Воины, в составе сорока человек, стали по кругу и договорились, что каждые два воина будут убивать третьего, пока не погибнут все. Иосиф Флавий, командовавший этим отрядом, якобы быстро рассчитал, где нужно встать ему и его товарищу, чтобы остаться последними и сдать крепость римлянам.
'''

soldiers = ['soldier ' + str(i + 1) for i in range(10)]
num = 2

def iosifFlavius (s, n):
    q = Queue()
    l = len(s)

    # заполняем очередь, каждый новый элемент добавляется в начало, а предыдущий продвигается вперед
    for i in range(len(s)):
        q.enqueue(s[i])

    # так исчисление идет с 1 а не 0
    i = 1
    # пока размер очереди больше чем 1
    while q.size() > 1:
        # удаляется первый из очереди (последний элемент списка)
        sold = q.dequeue()
        if i % n != 0:
            # если не кратно нужному числу, помещается в конец очереди (в начало списка)
            q.enqueue(sold)
            i = i + 1
        else:
            # кратно нужно числу, возобновляю отсчет
            i = 1

    # последний оставшийся
    return q.dequeue()


# print('iosifFlavius', iosifFlavius(soldiers, num))

'''
Дек имеет структуру упорядоченной коллекции элементов, которые могут добавляться и удаляться с любого конца - и с головы, и с хвоста.
'''
class Deque:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def addFront(self, item):
        self.items.append(item)

    def addRear(self, item):
        self.items.insert(0, item)

    def removeFront(self):
        return self.items.pop()

    def removeRear(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)

'''
Палиндромом называют строку, которая одинаково читается справа налево и слева направо. Например, radar, toot или madam. Мы хотим создать алгоритм, принимающий на вход строку символов и проверяющий, является ли она палиндромом.
'''

def palchecker(aString):
    chardeque = Deque()
    
    # превращаем строку в заполненый дек
    for ch in aString:
        chardeque.addRear(ch)

    # проверка соответствия
    stillEqual = True

    # если дек опустел или остался последний символ то условия для палиндрома соблюдены
    while chardeque.size() > 1 and stillEqual:
        # первый символ
        first = chardeque.removeFront()
        # последний символ
        last = chardeque.removeRear()
        # если символы не равны, условие нарушилось
        if first != last:
            stillEqual = False

    return stillEqual

# print(palchecker("lsdkjfskf"))
# print(palchecker("radar"))

'''
Граф — абстрактный математический объект, представляющий собой множество вершин графа и набор рёбер, то есть соединений между парами вершин. Например, за множество вершин можно взять множество аэропортов, обслуживаемых некоторой авиакомпанией, а за множество рёбер взять регулярные рейсы этой авиакомпании между городами.

Вершина (иногда её называют узел) - основная часть графа. Может иметь имя, которое называется ключ. Также вершина может обладать дополнительной информацией, которую мы будем называть полезной нагрузкой.

Ребро (или дуга) - другая фундаментальная часть графа. Ребро, соединяющее две вершины, показывает наличие между ними определённых отношений. Рёбра могут быть одно- и двунаправленными. Если все рёбра графа однонаправленные, то мы называем его направленным графом. 

Вес - рёбра могут иметь вес, показывающий стоимость перемещения от одной вершины к другой. Например, в графе дорог, связывающих города, вес ребра может отображать расстояние между двумя населёнными пунктами.

Путь в графе - это последовательность вершин, соединённых рёбрами.

Цикл в направленном графе начинается и заканчивается в одной и той же вершине.

Есть две широко известные реализации графа: матрица смежности и список смежности. 

Одним из простейших способов реализовать граф является использование двумерной матрицы. Таблица осями которой являются вершины графа, если они связаны то значением являются ребра.

Более пространственно-экономичным способом реализации разреженного графа является использование списка смежности. Список, внутри которого списки содержащие связаные вершины.

'''
# вершина
class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

# граф
class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    # вершины
    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    # ребра
    def addEdge(self, f, t, cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())
    
'''
Задача о словесной лестнице
В начале изучения алгоритмов для графов, давайте рассмотрим следующую головоломку, которая называется словесная лестница. Требуется преобразовать слово FOOL в слово SAGE. Изменения должны происходить постепенно, по букве за раз. На каждом шаге вы должны трансформировать слово в другое слово, а не в бессмыслицу. Словесная лестница была изобретена в 1878 году Льюисом Кэрролом - автором Алисы в Стране Чудес.
FOOL
POOL
POLL
POLE
PALE
SALE
SAGE
1) первый вариант создать список слов, потом сравнить их все друг с другом
2) предположим, у нас есть огромное количество корзин, на каждой из которых написано четырёхбуквенное слово, в котором одна буква заменена подчёркиванием. 
_ope
pope
rope
nope
...

p_pe
pope
pipe
pape
...

po_e
pope
pole
pore
...
При обработке каждого слова в списке мы сравниваем его с корзинами, используя _ для произвольной подстановки. 


'''


def buildGraph(wordFile):
    d = {}
    g = Graph()
    wfile = open(wordFile,'r')
    # create buckets of words that differ by one letter
    for line in wfile:
        word = line[:-1]
        for i in range(len(word)):
            bucket = word[:i] + '_' + word[i+1:]
            if bucket in d:
                d[bucket].append(word)
            else:
                d[bucket] = [word]
    # add vertices and edges for words in the same bucket
    for bucket in d.keys():
        for word1 in d[bucket]:
            for word2 in d[bucket]:
                if word1 != word2:
                    g.addEdge(word1,word2)
    return g