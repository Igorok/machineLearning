# -*- coding: utf-8 -*-

'''
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
Воины, в составе сорока человек, стали по кругу и договорились, что каждые два воина будут убивать третьего, пока не погибнут все. Иосиф Флавий, командовавший этим отрядом, якобы быстро рассчитал, где нужно встать ему и его товарищу, чтобы остаться последними, чтобы сдать крепость римлянам.
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


print('iosifFlavius', iosifFlavius(soldiers, num))